import bpy
import os
import subprocess

bl_info = {
    "name": "Open OS Browser",
    "description": "open OS browser from blender browser",
    "author": "1C0D",
    "version": (1, 3, 0),
    "blender": (2, 90, 0),
    "location": "Browser>context_menu",
    "category": "Development",
}

class OPEN_OT_os_browser(bpy.types.Operator):
    bl_idname = "open.os_browser"
    bl_label = "Open OS browser"
    
    On : bpy.props.BoolProperty(default=False)

    def execute(self, context):
        filename=context.space_data.params.filename
        dirpath=context.space_data.params.directory.decode("utf-8")
        filepath = os.path.abspath(os.path.join(dirpath, filename))

#        bpy.ops.wm.path_open(filepath=dirpath)
        if filename:
            if self.On:
                subprocess.Popen(fr'explorer /select,{filepath}')
            else:
                subprocess.Popen(fr'explorer /open, {filepath}')

        else:
            subprocess.Popen(fr'explorer "{dirpath}"')

        return {'FINISHED'}
  
def draw(self, context):

    layout = self.layout
    layout.separator(factor=1.0)
    op=layout.operator("open.os_browser",
                         text="Open OS Broswer", icon='FILEBROWSER')
    op.On = True
    op1=layout.operator("open.os_browser",
                         text="Open file in OS", icon='FILE')
    op1.On = False

addon_keymaps = []

def register():
    bpy.utils.register_class(OPEN_OT_os_browser)
    bpy.types.FILEBROWSER_MT_context_menu.append(draw)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        km = kc.keymaps.new(name='File Browser', space_type='FILE_BROWSER')
        kmi = km.keymap_items.new(
            "open.os_browser", "O", "PRESS", ctrl=True)
        kmi.properties.On = True
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(
            "open.os_browser", "O", "PRESS", ctrl=True,shift=True)
        kmi.properties.On = False
        addon_keymaps.append((km, kmi))

def unregister():
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(OPEN_OT_os_browser)
    bpy.types.FILEBROWSER_MT_context_menu.remove(draw)

