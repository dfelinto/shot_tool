"""
User Interface
"""

import bpy

from bpy.types import (
        Panel,
        )


# ############################################################
# Toolshelf Viewport
# ############################################################

class ST_VIEW3D_PT_tools_creation(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Creation"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Work in progress ...")


class ST_VIEW3D_PT_tools_cleanup(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Cleanup"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Work in progress ...")


class ST_VIEW3D_PT_tools_render(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Work in progress ...")


# ############################################################
# Un/Register
# ############################################################

classes = (
        ST_VIEW3D_PT_tools_creation,
        ST_VIEW3D_PT_tools_cleanup,
        ST_VIEW3D_PT_tools_render,
        )


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

