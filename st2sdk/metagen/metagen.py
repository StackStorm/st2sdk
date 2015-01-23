import importlib
import inspect
import os
import re
import shutil
import yaml


def parseAdditional(adds):
    add_dict = {}
    for add in adds.split():
        if re.search('=', add):
            k, v = adds.split('=', 1)
            add_dict[k] = v
        else:
            add_dict[add] = None
    return add_dict


def create_pack(pack, empty=True):
    pack_dir = 'output/packs/%s' % pack
    if os.path.isdir(pack_dir):
        shutil.rmtree(pack_dir)
    os.mkdir(pack_dir)
    os.mkdir("%s/rules" % pack_dir)
    os.mkdir("%s/sensors" % pack_dir)
    if empty is False:
        shutil.copytree('actions', pack_dir + "/actions")
    else:
        os.mkdir("%s/actions" % pack_dir)


def create_manifest(pack, args):
    manifest = {}
    manifest['name'] = pack
    manifest['description'] = ""
    manifest['version'] = args.version
    manifest['author'] = args.author
    manifest['email'] = args.email
    fh = open('output/packs/%s/pack.yaml' % pack, 'w')
    fh.write(yaml.dump(manifest, default_flow_style=False))
    fh.close()


def create_md(pack):
    readme = open('output/packs/%s/README.md' % pack, 'w')
    readme.write("%s\n=====" % pack)
    readme.close()

    changes = open('output/packs/%s/CHANGES.md' % pack, 'w')
    changes.write("%s\n=====" % pack)
    changes.close()

    config = open('output/packs/%s/config.yaml' % pack, 'w')
    config.write("---\n")
    config.close()


def get_all(modpath, ignores, add_required, add_optional):
    items = {}
    pattern = re.compile('[^_].*')
    for member in dir(modpath):
        if pattern.match(member) and member not in ignores:
            foo = getattr(modpath, member)
            if inspect.ismethod(foo) is True or inspect.isfunction(foo) is True:
                items[member] = {}
                argspec = inspect.getargspec(foo)
                if argspec.defaults is not None:
                    items[member] = dict(
                        zip(argspec.args[-len(argspec.defaults):], argspec.defaults))
                for arg in argspec.args:
                    if arg not in items[member] and arg not in ['self', 'names']:
                        items[member][arg] = 'required'
                for item in items:
                    for p in items[item]:
                        if isinstance(items[item][p], tuple):
                            items[item][p] = map(list, items[item][p])
                for req in add_required:
                    items[member][req] = 'required'
                for opt in add_optional:
                    if add_optional[opt] is not None:
                        items[member][opt] = add_optional[opt]
                    else:
                        items[member][opt] = None

    return items


def build_action_list(obj, ignores, add_required, add_optional):
    items = get_all(obj, ignores, add_required, add_optional)
    actions = {'items': items}
    actions['module_path'] = obj.__module__
    if inspect.isclass(obj) is True:
        actions['cls'] = obj.__name__
    return actions


def generate_meta(obj, args, ignores, add_required, add_optional):

    actions = build_action_list(obj, ignores, add_required, add_optional)

    class_param = {}
    if 'cls' in actions.keys():
        class_param = {"cls": {"type": "string", "immutable": True, "default": actions['cls']}}
    module_param = {
        "module_path": {"type": "string", "immutable": True, "default": actions['module_path']}}
    for action in actions['items']:
        if args.action_prefix is not None:
            prefix = "%s_" % args.action_prefix
        else:
            prefix = ""

        parameters = {}
        action_meta = {
            "name": "",
            "parameters": {
                "action": {
                    "type": "string",
                    "immutable": True,
                    "default": action}
            },
            "runner_type": "run-python",
            "description": "",
            "enabled": True,
            "entry_point": "run.py"}

        action_meta["name"] = "%s%s" % (prefix, action)
        for parameter in actions['items'][action]:
            parameters[parameter] = {"type": "string"}
            if isinstance(actions['items'][action][parameter], bool):
                parameters[parameter]['type'] = "boolean"
            if actions['items'][action][parameter] is not None:
                if actions['items'][action][parameter] == 'required':
                    parameters[parameter]['required'] = True
                elif isinstance(actions['items'][action][parameter], list):
                    parameters[parameter]['type'] = "array"
                    parameters[parameter]['default'] = actions['items'][action][parameter]
                else:
                    parameters[parameter]['default'] = actions['items'][action][parameter]
        if class_param is not None:
            parameters.update(class_param)
        action_meta['parameters'].update(module_param)
        action_meta['parameters'].update(parameters)

        filename = "output/packs/" + args.pack + "/actions/" + prefix + action + ".yaml"

        if not args.dry_run:
            fh = open(filename, 'w')
            fh.write(yaml.dump(action_meta, default_flow_style=False))
            fh.close()
        else:
            print filename
            print(yaml.dump(action_meta, default_flow_style=False))


def main(args):
    add_required = {}
    add_optional = {}

    if args.module:
        module = importlib.import_module(args.module)
        if args.clss:
            obj = getattr(module, args.clss)
        else:
            obj = module

    if args.ignore:
        ignores = args.ignore.split(',')
    else:
        ignores = []

    if args.required is not None:
        add_required = parseAdditional(args.required)

    if args.optional is not None:
        add_optional = parseAdditional(args.optional)

    # create_pack(args.pack, empty=args.empty)
    # create_manifest(args.pack, args)
    # create_md(args.pack)

    if not args.empty:
        generate_meta(obj, args, ignores, add_required, add_optional)
