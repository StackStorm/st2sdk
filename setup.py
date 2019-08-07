#!/usr/bin/env python
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
import sys
import io

from setuptools import setup, find_packages


PKG_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
PKG_REQ_FILE = '%s/requirements.txt' % PKG_ROOT_DIR
os.chdir(PKG_ROOT_DIR)


def get_version_string():
    version = None
    sys.path.insert(0, PKG_ROOT_DIR)
    from st2sdk import __version__
    version = __version__
    sys.path.pop(0)
    return version


def get_requirements():
    with open(PKG_REQ_FILE) as f:
        required = f.read().splitlines()

    # NOTE: We use latest version under Python 3
    required = [l for l in required if not l.startswith('cmd2')]
    # same as six.PY2, but we can't use six in setup.py  because it isn't
    # garaunteed to be in a fresh virtualenv before installing this package
    if sys.version_info[0] == 2:
        required.append('cmd2>=0.8.9,<0.9')
    else:
        required.append('cmd2>=0.9.i5,<0.10')

    return required


setup(
    name='st2sdk',
    version=get_version_string(),
    description='Various tools and utilities which aid with StackStorm pack development.',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    author='StackStorm',
    author_email='info@stackstorm.com',
    url='http://www.stackstorm.com',
    packages=find_packages(exclude=['tests']),
    package_data={'st2sdk': ['templates/*']},
    install_requires=get_requirements(),
    license='Apache License (2.0)',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    entry_points={
        'console_scripts': [
            'st2sdk = st2sdk.shell:main'
        ]
    },
    scripts=[
        # Common files, not binaries per say (ideally we would eventually install them to some
        # other place)
        'scripts/common.sh',
        'scripts/st2.tests.conf',

        # Scripts
        'scripts/st2-check-validate-yaml-file',
        'scripts/st2-check-validate-json-file',
        'scripts/st2-check-validate-pack-metadata-exists',
        'scripts/st2-check-register-pack-resources',
        'scripts/st2-check-pylint-pack',
        'scripts/st2-check-print-pack-tests-coverage',
        'scripts/st2-check-validate-pack-example-config'
    ]
)
