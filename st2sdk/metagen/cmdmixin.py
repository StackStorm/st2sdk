import six


from cmd2 import options, make_option
from st2sdk import metagen
from st2sdk.metagen.metagen import main as metagen_main

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
                          help='Run in an interactive mode'),
              make_option('-c', '--class', action='store', type='string', dest='clss',
                          help=''),
              make_option('-g', '--ignore', action='store', type='string', dest='ignore',
                          help=''),
              make_option('--dry_run', action='store_true',
                          help=''),
              make_option('--prefix', action='store', type='string', dest='prefix',
                          help=''),
              make_option('-v', '--version', action='store', type='string', dest='version',
                          help=''),
              make_option('--required', action='store', type='string', dest='required',
                          help=''),
              make_option('--optional', action='store', type='string', dest='optional',
                          help=''),
              make_option('--author', action='store', type='string', dest='author',
                          help=''),
              make_option('--email', action='store', type='string', dest='email',
                          help='')])
    def do_metagen(self, arg, opts=None):
        args = arg.split()
        pack = args[0] if args else None
        module = args[1] if args else None
        if opts.interactive:
            data = self._gather_input_metagen(pack, module, opts)
        else:
            data = Data()
            setattr(data, 'pack', pack)
            setattr(data, 'module', module)
            setattr(data, 'clss', opts.clss)
            setattr(data, 'ignore', opts.ignore)
            setattr(data, 'dry_run', opts.dry_run)
            setattr(data, 'action_prefix', opts.prefix)
            setattr(data, 'author', opts.author)
            setattr(data, 'email', opts.email)
            setattr(data, 'version', opts.version)
            setattr(data, 'required', opts.required)
            setattr(data, 'optional', opts.optional)

        self.do_bootstrap(getattr(data, 'pack'))
        metagen_main(data)

    def help_metagen(self):
        help_string = COMMAND_HELP['metagen']
        help_string = '\n'.join(help_string)
        print(help_string)

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
