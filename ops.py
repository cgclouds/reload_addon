import bpy
from .utils import prefs, reload_addon, default_display


class RAS_OT_list_actions(bpy.types.Operator):
    """Move the selected item up and down"""
    bl_label = 'Move items'
    bl_idname = 'ras.list_action'
    bl_options = {'REGISTER'}

    action : bpy.props.EnumProperty(
        items=(('UP', "Up", ''),
            ('DOWN', "Down", ''),)
            )

    @classmethod
    def poll(cls, context):
        return prefs().modules

    def invoke(self, context, event):
        p = prefs()

        if self.action == 'DOWN' and p.index < len(p.modules) - 1:
            item_next = p.modules[p.index + 1].name
            p.modules.move(p.index, p.index + 1)
            p.index += 1

        elif self.action == 'UP' and p.index >= 1:
            item_prev = p.modules[p.index - 1].name
            p.modules.move(p.index, p.index - 1)
            p.index -= 1

        return {'FINISHED'}


class RAS_OT_reload_addon(bpy.types.Operator):
    """Choose an add-on into the list for reload"""
    bl_label = 'Reload'
    bl_idname = 'ras.reload'
    bl_options = {'REGISTER'}

    def execute(self, context):
        if prefs().addons_display != default_display():
            addon = prefs().addons_display
            reload_addon(addon)
            self.report({'INFO'}, f'{addon}: Reloaded.')
        else:
            self.report({'INFO'}, 'Choose an add-on in Add-on Preferences.')

        return {'FINISHED'}



classes = (
    RAS_OT_list_actions,
    RAS_OT_reload_addon,
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
