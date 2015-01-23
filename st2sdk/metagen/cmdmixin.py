import argparse
import six

from cmd2 import options, make_option
from st2sdk.metagen import metagen

COMMAND_HELP = {
    'metagen': [
        'metagen [pack name] [module name]',
        'Create initial directory structure for the provided pack. Inspect module and autogenerate'
        'action metadata.'
    ]
}


class Data(object):

    def __setattr__(self, name, value):
        super(Data, self).__setattr__(name, value)

    def __getattr__(self, name):
        return super(Data, self).__getattr__(name)

    def __delattr__(self, name):
        super(Data, self).__delattr__(name)


class MetagenCmdMixin(object):

    @options([make_option('-i', '--interactive', action='store_true',
                          help='Run in an interactive mode')])
    def do_metagen(self, args, opts=None):
        if opts.interactive:
            data = self._gather_input_metagen()
        else:
            args = args.split()
            data = self._get_args_parser_metagen().parse_args(args)
        self.do_bootstrap(getattr(data, 'pack'))
        metagen.main(data)

    def help_metagen(self):
        help_string = COMMAND_HELP['metagen']
        help_string = '\n'.join(help_string)
        print(help_string)
        parser = self._get_args_parser_metagen()
        parser.print_help()

    def _gather_input_metagen(self, pack=None, module=None, opts=None):
        data = Data()
        if not pack:
            pack = six.moves.input('Pack name: ')
        setattr(data, 'pack', pack)

        if not module:
            module = six.moves.input('Module name: ')
        setattr(data, 'module', module)

        clss = opts.clss
        if not clss:
            clss = six.moves.input('Class name: ')
        setattr(data, 'clss', clss)

        ignore = opts.ignore
        if not ignore:
            ignore = six.moves.input('Ignore list (csv): ')
        setattr(data, 'ignore', ignore)

        dry_run = opts.dry_run
        if not dry_run:
            dry_run = six.moves.input('dry_run[y/n]: ')
            dry_run = 'y' == dry_run
        setattr(data, 'dry_run', dry_run)

        prefix = opts.prefix
        if not prefix:
            prefix = six.moves.input('Action prefix: ')
        setattr(data, 'action_prefix', prefix)

        author = opts.author
        if not author:
            author = six.moves.input('Author: ')
        setattr(data, 'author', author)

        email = opts.email
        if not email:
            email = six.moves.input('Email: ')
        setattr(data, 'email', email)

        version = opts.version
        if not version:
            version = six.moves.input('Version: ')
        setattr(data, 'version', version)

        required = opts.required
        if not required:
            required = six.moves.input('Required: ')
        setattr(data, 'required', required)

        optional = opts.optional
        if not optional:
            optional = six.moves.input('Optional: ')
        setattr(data, 'optional', optional)

        return data

    def _get_args_parser_metagen(self):
        parser = argparse.ArgumentParser(
            description='StackStorm Action Metadata Generator for Python modules')
        parser.add_argument('--pack', action="store", dest="pack", required=True)
        parser.add_argument('--module', action="store", dest="module", default=None)
        parser.add_argument('--class', action="store", dest="clss")
        parser.add_argument('--ignore', action="store", dest="ignore")
        parser.add_argument('--dry_run', action="store_true", dest="dry_run")
        parser.add_argument('--prefix', action="store", dest="action_prefix", default=None)
        parser.add_argument('--author', action="store", dest="author", default="Estee Tew")
        parser.add_argument('--email', action="store", dest="email", default="")
        parser.add_argument('--version', action="store", dest="version", default="0.1")
        parser.add_argument('--required', action="store", dest='required', default=None)
        parser.add_argument('--optional', action="store", dest='optional', default=None)
        return parser
