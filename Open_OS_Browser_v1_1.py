import bpy

bl_info = {
    "name": "Open OS Browser",
    "description": "open OS browser from blender browser",
    "author": "1C0D",
    "version": (1, 1, 0),
    "blender": (2, 90, 0),
    "location": "Browser>context_menu",
    "category": "Development",
}

class OPEN_OT_os_browser(bpy.types.Operator):
    bl_idname = "open.os_browser"
    bl_label = "Open OS browser"

    def execute(self, context):
        filepath=context.space_data.params.directory.decode("utf-8")
        bpy.ops.wm.path_open(filepath=filepath)

        return {'FINISHED'}
  
def draw(self, context):

    layout = self.layout
    layout.separator(factor=1.0)
    layout.operator("open.os_browser",
                         text="Open OS Broswer", icon='FILEBROWSER')

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


def unregister():
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)    
    bpy.utils.unregister_class(OPEN_OT_os_browser)
    bpy.types.FILEBROWSER_MT_context_menu.remove(draw)

