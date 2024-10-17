bl_info = {
    'name': 'Reload Addon',
    'description': 'Reload all modules of selected add-on (shift + alt + R).',
    'location': 'Set in add-on preferences.',
    'doc_url': '',
    'author': 'CG Clouds',
    'version': (1, 0, 0),
    'blender': (3, 0, 0),
    'warning': '',
    'category': 'Development'
    }


import bpy

from . import utils
from . import ops
from . import prefs
from . import panel



def register():
    ops.register()
    prefs.register()
    p = utils.prefs()
    if p.active_panel:
        panel.RAS_PT_main_panel.bl_space_type = p.space_type
        panel.register()


def unregister():
    if utils.prefs().active_panel:
        panel.unregister()
    prefs.unregister()
    ops.unregister()
