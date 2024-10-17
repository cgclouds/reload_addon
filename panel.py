import bpy
from .utils import prefs, default_display


class RAS_PT_main_panel(bpy.types.Panel):
    bl_label = 'Reload Addon'
    bl_idname = 'RAS_PT_main_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Reload Addon'

    def draw(self, context):
        layout = self.layout
        p = prefs()

        row = layout.row()

        row.prop(p, 'addons_display')

        row = layout.row()

        row.enabled = True if p.addons_display != default_display() else False
        row.scale_y = 1.1
        row.operator('ras.reload', )

        row = layout.row()
        row = layout.row()

        row.label(text = 'List of modules:')

        row = layout.row()

        row.template_list('RAS_UL_list_modules', '', p, 'modules', p, 'index', rows = 5)

        row = layout.row()

        r = row.row(align = True)
        r.alignment = 'CENTER'
        r.scale_x = 2.05
        r.operator('ras.list_action', text = '', icon = 'TRIA_UP').action = 'UP'
        r.operator('ras.list_action', text = '', icon = 'TRIA_DOWN').action = 'DOWN'

        row = layout.row()
        row = layout.row()

        row.prop(p, 'automatic_sort', text = 'Automatic sort')



def register():
    bpy.utils.register_class(RAS_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(RAS_PT_main_panel)
