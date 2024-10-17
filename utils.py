import bpy
import inspect
import os
import importlib
import sys


def module_name(module = None):
    return module.__name__.split('.')[0] if module else __name__.split('.')[0]


def path_addons():
    return os.path.dirname(os.path.dirname(__file__))


def prefs():
    return bpy.context.preferences.addons[module_name()].preferences


def is_addon_enable(file):
    module = sys.modules.get(remove_extension(file))
    return module.__addon_enabled__ if inspect.ismodule(module) else False


def remove_extension(file):
    return file if os.path.isdir(file) else file.split('.')[0]


def default_display():
    return 'Choose an addon...'


def items_from_list(list):
    return ((list[i], list[i], '', i + 1) for i in range(len(list))) if list else None


def items_addons_display(self, context):
    list = [(default_display(), default_display(), 'CHoose an add-on for reload it', 0)]
    addons_name = sorted(remove_extension(name) for name in os.listdir(path_addons())
        if (is_addon_enable(name) or name == prefs().current_addon) and name != module_name())
    list += items_from_list(addons_name)
    return list


def update_addons_display(self, context):
    addon_display = self.addons_display
    p = prefs()
    p.current_addon = addon_display
    if addon_display == default_display():
        p.modules.clear()
    else:
        update_modules(find_modules_list(addon_display))
        p.index = 0


def update_ui_panel(self, context):
    from . import panel
    if self.active_panel:
        try:
            panel.register()
        except:
            pass
    else:
        try:
            panel.unregister()
        except:
            pass


def update_space_type(self, context):
    from . import panel
    panel.unregister()
    panel.RAS_PT_main_panel.bl_space_type = self.space_type
    panel.register()


def icon_module(module):
    names = module.split('.')
    path = path_addons()
    for name in names:
        path = os.path.join(path, name)
    return 'FILE_FOLDER' if os.path.isdir(path) else 'FILE_BLANK'


def new_modules(addon_name):
    p = prefs()
    current_modules = current_modules_list()
    find_modules = find_modules_list(addon_name)
    new_modules = list(set(current_modules).symmetric_difference(find_modules))
    if p.automatic_sort:
        update_modules(find_modules)
    else:
        news = len(new_modules)
        for mod in new_modules:
            news -= 1
            if mod in find_modules:
                add_modules(mod)
                p.index = len(find_modules) - news - 1
            if mod in current_modules:
                for i in range(len(current_modules)):
                    if p.modules[i].module == mod:
                        index = i
                        break
                p.modules.remove(index)
                p.index = min(max(0, p.index - 1), len(current_modules) - 1) if p.index >= index else p.index


def add_modules(module):
    m = prefs().modules.add()
    m.name = module.split('.')[-1]
    m.module = module
    m.module_icon = icon_module(module)


def update_modules(modules):
    prefs().modules.clear()
    for module in modules:
        add_modules(module)


def find_modules_list(addon_name):
    path_addon = os.path.join(path_addons(), addon_name)

    modules = []

    def find_modules(path, module_name):
        file_list = []
        for file in os.listdir(path):
            name = file.split('.')
            name[0] = file if file.startswith('.') else name[0]
            new_path = os.path.join(path, name[0])
            new_module_name = module_name + '.' + name[0]
            if len(name) > 1 and name[1] == 'py' and name[0] != '__init__':
                file_list.append(new_module_name)
            elif os.path.isdir(new_path) and inspect.ismodule(sys.modules.get(new_module_name)) and name[0] != '__pycache__':
                find_modules(new_path, new_module_name)
                modules.append(new_module_name)

        modules.extend(file_list)
        file_list.clear()

    if os.path.isdir(path_addon):
        find_modules(path_addon, addon_name)

    modules.append(addon_name)

    return modules


def current_modules_list():
    modules = prefs().modules
    return list(modules[i].module for i in range(len(modules)))


def reload_addon(addon_name):
    path_addon = os.path.join(path_addons(), addon_name)

    mod = __import__(addon_name)

    if not inspect.ismodule(sys.modules.get(addon_name)):
        mod.unregister()
        bpy.ops.preferences.addon_enable(module = addon_name)

    bpy.ops.preferences.addon_disable(module = addon_name)

    new_modules(addon_name)

    modules = prefs().modules
    for i in range(len(modules)):
        mod = modules[i].module

        if not inspect.ismodule(sys.modules.get(mod)):
            __import__(mod)

        importlib.reload(sys.modules.get(mod))
        # print('/----------------- ' + mod)

    bpy.ops.preferences.addon_enable(module = addon_name)
