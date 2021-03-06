"""
User Interface
"""

import bpy

from bpy.types import (
        Panel,
        )

from .defines import (
        SHOT_TYPE,
        )


# ############################################################
# Toolshelf Viewport
# ############################################################

class ST_VIEW3D_PT_tools_creation(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Creation"
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        shot_type = scene.shot_type

        col = layout.column()
        col.prop(scene, "shot_name")
        col.prop(scene, "shot_type")
        col.separator()

        col.operator("shot_tool.name_scene")
        col.operator("shot_tool.relink_actions" \
                if shot_type == SHOT_TYPE.LIGHTING \
                else "shot_tool.name_actions")
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
    bl_context = 'objectmode'

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
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("shot_tool.set_hair_system_defaults")
        col.operator("shot_tool.set_render_defaults")


class ST_VIEW3D_PT_tools_update(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Update"
    bl_context = 'objectmode'

    @classmethod
    def poll(cls, context):
        return context.scene.shot_type in {
                SHOT_TYPE.ANIMATION,
                SHOT_TYPE.LIGHTING,
                }

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        if context.scene.shot_type == SHOT_TYPE.LIGHTING:
            col.operator("shot_tool.update_bone_constraints_lighting", icon='CONSTRAINT_BONE')
        else: # SHOT_TYPE.ANIMATION
            col.operator("shot_tool.update_bone_constraints_animation", icon='CONSTRAINT_BONE')


class ST_VIEW3D_PT_tools_misc(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Miscellaneous"
    bl_context = 'mesh_edit'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("shot_tool.set_vertex_color", icon='VPAINT_HLT')


class ST_VIEW3D_PT_tools_update_pose(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Shot Tool'
    bl_label = "Update"
    bl_context = 'posemode'

    @classmethod
    def poll(cls, context):
        return context.scene.shot_type in {
                SHOT_TYPE.ANIMATION,
                SHOT_TYPE.LIGHTING,
                }

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        if context.scene.shot_type == SHOT_TYPE.LIGHTING:
            col.operator("shot_tool.update_pose_bone_constraints_lighting", icon='CONSTRAINT_BONE')
        else: # SHOT_TYPE.ANIMATION
            col.operator("shot_tool.update_pose_bone_constraints_animation", icon='CONSTRAINT_BONE')


# ############################################################
# Un/Register
# ############################################################

classes = (
        ST_VIEW3D_PT_tools_creation,
        ST_VIEW3D_PT_tools_cleanup,
        ST_VIEW3D_PT_tools_render,
        ST_VIEW3D_PT_tools_update,
        ST_VIEW3D_PT_tools_update_pose,
        ST_VIEW3D_PT_tools_misc,
        )


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

