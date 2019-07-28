# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import argparse
import logging
import logging.config

import six
import cmd2
from cmd2 import Cmd
from jinja2 import Environment, FileSystemLoader

__all__ = [
    'SDKApp'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
LOG = logging.getLogger(__name__)

COMMAND_HELP = {
    'bootstrap': [
        'bootstrap [pack name]',
        'Create initial directory structure for the provided pack.'
    ]
}

DIRECTORY_STRUCTURE = [
    'sensors/',
    'actions/',
]

FILE_TEMPLATES = [
    {
        'name': 'README.md',
        'path': 'README.md'
    },
    {
        'name': 'pack.yaml',
        'path': 'pack.yaml'
    },
    {
        'name': 'config.yaml',
        'path': 'config.yaml'
    }
]


bootstrap_parser = argparse.ArgumentParser()
bootstrap_parser.add_argument('pack_name', help='Pack name')
bootstrap_parser.add_argument('-i', '--interactive',
                              action='store_true',
                              default=False,
                              help='Run in an interactive mode')


class SDKApp(Cmd):
    into = 'Welcome to st2sdk'
    prompt = '(st2sdk): '

    @cmd2.with_argparser(bootstrap_parser)
    def do_bootstrap(self, args):
        pack_name = args.pack_name
        self._setup_logging()

        if args.interactive:
            data = self._gather_input(pack_name=pack_name)
        else:
            data = {
                'pack_name': pack_name,
                'author_name': 'John Doe',
                'author_email': 'john.doe@example.com'
            }

        if not data['pack_name']:
            raise ValueError('Pack name is required')

        self._handle_bootstrap(data=data)

    def help_bootstrap(self):
        help_string = COMMAND_HELP['bootstrap']
        help_string = '\n'.join(help_string)
        print(help_string)

    def _gather_input(self, pack_name=None):
        """
        :rtype: ``dict``
        """
        if not pack_name:
            pack_name = six.moves.input('Pack name: ')

        author_name = six.moves.input('Author name: ')
        author_email = six.moves.input('Author email: ')

        data = {
            'pack_name': pack_name,
            'author_name': author_name,
            'author_email': author_email
        }
        return data

    def _get_template_context(self):
        """
        :rtype: ``dict``
        """
        context = {}
        return context

    def _handle_bootstrap(self, data):
        cwd = os.getcwd()
        pack_name = data['pack_name']
        pack_path = os.path.join(cwd, pack_name)

        if os.path.isdir(pack_path):
            raise ValueError('Pack directory "%s" already exists' %
                             (pack_path))

        # 1. Create directory structure
        pack_path = self._create_directory_structure(pack_path=pack_path)

        # 2. Copy over and render the file templates
        context = data
        self._render_and_write_templates(pack_path=pack_path, context=context)

        LOG.info('Pack "%s" created in %s' % (pack_name, pack_path))

    def _create_directory_structure(self, pack_path):
        LOG.debug('Creating directory: %s' % (pack_path))
        os.makedirs(pack_path)

        for directory in DIRECTORY_STRUCTURE:
            full_path = os.path.join(pack_path, directory)
            LOG.debug('Creating directory: %s' % (full_path))
            os.makedirs(full_path)

        return pack_path

    def _render_and_write_templates(self, pack_path, context):
        """
        :param context: Template render context.
        :type context: ``dict``
        """
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

        for template_dict in FILE_TEMPLATES:
            template_name = template_dict['name']
            render_path = template_dict['path']

            template = env.get_template(template_name)
            rendered = template.render(**context)

            full_render_path = os.path.join(pack_path, render_path)
            with open(full_render_path, 'w') as fp:
                LOG.debug('Writing template file: %s' % (full_render_path))
                fp.write(rendered)

    def _setup_logging(self):
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '%(asctime)s %(levelname)s %(message)s'
                },
            },
            'handlers': {
                'console': {
                    '()': logging.StreamHandler,
                    'formatter': 'default'
                }
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        }
        logging.config.dictConfig(logging_config)
