import bpy

from .utils import module_name, items_addons_display, update_addons_display, default_display, update_ui_panel, update_space_type


class RAS_UL_list_modules(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, 'name', text = '', icon = item.module_icon, emboss = False, translate = False)

    def draw_filter(self, context, layout):
        layout.prop(self, 'filter_name', text = '')


class RAS_modules(bpy.types.PropertyGroup):
    module :  bpy.props.StringProperty(
        )
    module_icon : bpy.props.StringProperty(
        )


class RAS_addon_prefences(bpy.types.AddonPreferences):
    bl_idname = module_name()

    addons_display : bpy.props.EnumProperty(
        items = items_addons_display,
        name = '',
        description = 'List of enabled add-ons',
        default = 0,
        update = update_addons_display,
        )
    current_addon : bpy.props.StringProperty(
        )
    modules : bpy.props.CollectionProperty(
        type = RAS_modules
        )
    index : bpy.props.IntProperty(
        name = '',
        )
    automatic_sort : bpy.props.BoolProperty(
        description = 'Enabled: When reload automatically sort.\nDisabled: When reload if modules are added they will be added to the end of the list',
        default = True,
        )
    show_modules : bpy.props.BoolProperty(
        name = 'Show modules',
        )
    active_panel : bpy.props.BoolProperty(
        update = update_ui_panel,
        )
    space_type : bpy.props.EnumProperty(
        items = [
            ('VIEW_3D', 'VIEW_3D', '', 0),
            ('TEXT_EDITOR', 'TEXT_EDITOR', '', 1),
            ('IMAGE_EDITOR', 'IMAGE_EDITOR', '', 2),
            ('NODE_EDITOR', 'NODE_EDITOR', '', 3),
            ('SEQUENCE_EDITOR', 'SEQUENCE_EDITOR', '', 4),
            ],
        name = '',
        description = 'Choose where the UI-Panel will appear.',
        update = update_space_type,
        )

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        factor = 0.58

        box = layout.box()

        row = box.row()

        row.label(text = 'Add-on to reload:')

        row = box.row()

        row.scale_y = 1.1
        row.prop(self, 'addons_display')

        row = box.row()

        #--Reload
        row.enabled = True if self.addons_display != default_display() else False
        row.scale_y = 1.1
        row.operator('ras.reload', )

        row = box.row()

        #--Shortcut key
        kc = bpy.context.window_manager.keyconfigs.user
        km = kc.keymaps.get('Window')
        kmi = None
        for km_item in km.keymap_items:
            if km_item.idname == 'ras.reload':
                kmi = km_item
                break
        row.scale_y = 1.1
        split = row.split(factor = factor)
        split.label(text = 'Set shortcut key:')
        split.prop(kmi, 'type', text = '', full_event = True)

        row = box.row()

        #Space_type
        s = row.split(factor = factor)
        s.prop(self, 'active_panel', text = 'UI-Panel')
        if self.active_panel:
            s.prop(self, 'space_type')

        #--Modules
        row = box.row()

        row.alignment = 'LEFT'
        row.prop(self, 'show_modules', icon_only = True, icon="DISCLOSURE_TRI_DOWN" if self.show_modules else "DISCLOSURE_TRI_RIGHT", emboss = False)
        row.label(text = 'List of modules')

        if self.show_modules:

            row = box.row()

            split = row.split(factor = 0.37)
            c = split.column()
            c.prop(self, 'automatic_sort', text = 'Automatic sort', toggle = False)
            s = split.split()
            r = s.row()
            r.template_list('RAS_UL_list_modules', '', self, 'modules', self, 'index', rows = 5)
            c = r.column(align = True)
            c.scale_x = 1.75
            c.operator('ras.list_action', icon = 'TRIA_UP', text = '').action = 'UP'
            c.operator('ras.list_action', icon = 'TRIA_DOWN', text = '').action = 'DOWN'
            c.separator()

        row = box.row()



addon_keymaps = []
def registerKeymaps():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('ras.reload', 'R', 'PRESS', shift=True, alt=True, ctrl=False)
    addon_keymaps.append((km, kmi))


def unregisterKeymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = (
    RAS_modules,
    RAS_UL_list_modules,
    RAS_addon_prefences,
    )


def register():
    registerKeymaps()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregisterKeymaps()
