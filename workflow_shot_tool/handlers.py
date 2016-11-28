"""
Handlers

Functions called on system events (onLoad, ...)
"""

import bpy

from bpy.app.handlers import persistent


# ############################################################
# Handlers
# ############################################################

@persistent
def load_post(context):
    import os
    scene = bpy.context.scene
    if scene.shot_name == "":
        basedir, basename = os.path.split(bpy.data.filepath)
        scene.shot_name = basename[:7]


# ############################################################
# Placeholders
# ############################################################

"""
bpy.app.handlers.frame_change_post
on frame change for playback and rendering (after)

bpy.app.handlers.frame_change_pre
on frame change for playback and rendering (before)

bpy.app.handlers.game_post
on ending the game engine

bpy.app.handlers.game_pre
on starting the game engine

bpy.app.handlers.load_post
on loading a new blend file (after)

bpy.app.handlers.load_pre
on loading a new blend file (before)

bpy.app.handlers.render_cancel
on canceling a render job

bpy.app.handlers.render_complete
on completion of render job

bpy.app.handlers.render_init
on initialization of a render job

bpy.app.handlers.render_post
on render (after)

bpy.app.handlers.render_pre
on render (before)

bpy.app.handlers.render_stats
on printing render statistics

bpy.app.handlers.render_write
on writing a render frame (directly after the frame is written)

bpy.app.handlers.save_post
on saving a blend file (after)

bpy.app.handlers.save_pre
on saving a blend file (before)

bpy.app.handlers.scene_update_post
on updating the scenes data (after)

bpy.app.handlers.scene_update_pre
on updating the scenes data (before)

bpy.app.handlers.version_update
on ending the versioning code

bpy.app.handlers.persistent
Function decorator for callback functions not to be removed when loading new files
"""

# ############################################################
# Un/Register
# ############################################################

def register():
    bpy.app.handlers.load_post.append(load_post)


def unregister():
    bpy.app.handlers.load_post.remove(load_post)

