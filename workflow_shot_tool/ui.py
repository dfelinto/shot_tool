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
        scene = context.scene

        col = layout.column()
        col.prop(scene, "shot_name")
        col.prop(scene, "shot_type")
        col.separator()

        col.operator("shot_tool.name_scene")
        col.operator("shot_tool.name_actions")
        col.operator("shot_tool.assign_characters_layers")
        col.operator("shot_tool.set_metadata")
        col.operator("shot_tool.set_resolution")

        col.separator()
        row = col.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        col.prop(scene, "camera")


class ST_VIEW3D_PT_tools_cleanup(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Cleanup"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("shot_tool.remove_sequence_strips")
        col.operator("shot_tool.remove_markers")


class ST_VIEW3D_PT_tools_render(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("shot_tool.set_hair_system_defaults")
        col.operator("shot_tool.set_render_defaults")


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

