
# # reveal in explorer
# def reveal_in_explorer(path) :
    # #windows
    # if platform.system() == "Windows":
        # #os.startfile(path)
        # #subprocess.Popen(['explorer', path])
        # # subprocess.Popen(r'explorer /select,%s' % path)
        # #subprocess.call("explorer %s" % path, shell=True)
        # subprocess.Popen(r'explorer /select, %s' % path)
    # #mac
    # elif platform.system() == "Darwin":
        # #subprocess.Popen(["open", path])
        # subprocess.Popen(["open", "-a", "Finder", path])
    # #linux
    # else:
        # subprocess.Popen(["xdg-open", os.path.dirname(path)])


import bpy
import os
import subprocess

bl_info = {
    "name": "Open OS Browser",
    "description": "open OS browser from blender browser",
    "author": "1C0D",
    "version": (1, 4, 0),
    "blender": (2, 93, 0),
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
    

# add shortcut to open addons folder to Userpref paths 
class OPEN_OT_folder(bpy.types.Operator):
    bl_idname = "open.folder"
    bl_label = "Open folder"
    bl_options = {"REGISTER", "INTERNAL"}

    fp : bpy.props.StringProperty()

    def execute(self, context):

        if not os.path.exists(self.fp):
            print('Filepath not found', self.fp)
            return {"CANCELLED"}

        subprocess.Popen(fr'explorer "{self.fp}"')

        return {'FINISHED'}     

def draw1(self, context):
    layout = self.layout
    row = layout.row()
    row.label(text='')
    row.label(text='')
    row.operator(OPEN_OT_folder.bl_idname, text='Users addons').fp = bpy.utils.user_resource('SCRIPTS', path = "addons")
    row.operator(OPEN_OT_folder.bl_idname, text='Built-in addons').fp = os.path.join(bpy.utils.resource_path('LOCAL') , 'scripts', 'addons')


addon_keymaps = []

def register():
    bpy.utils.register_class(OPEN_OT_os_browser)
    bpy.utils.register_class(OPEN_OT_folder)
    bpy.types.FILEBROWSER_MT_context_menu.append(draw)
    bpy.types.USERPREF_PT_file_paths_data.prepend(draw1) 
    
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
    bpy.utils.unregister_class(OPEN_OT_folder)
    bpy.types.FILEBROWSER_MT_context_menu.remove(draw)
    bpy.types.USERPREF_PT_file_paths_data.remove(draw1)    

