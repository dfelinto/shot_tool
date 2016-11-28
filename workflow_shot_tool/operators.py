"""
Operators
"""

import bpy

from bpy.types import (
        Operator,
        )

from .defines import (
        SHOT_TYPE,
        )

TODO = False

# ############################################################
# Creation
# ############################################################

class ST_NameSceneOperator(Operator):
    bl_idname = "shot_tool.name_scene"
    bl_label = "Name Scene"

    def execute(self, context):
        names = {
                SHOT_TYPE.LAYOUT: 'layout',
                SHOT_TYPE.ANIMATION: 'anim',
                SHOT_TYPE.LIGHTING: 'lighting',
                }

        scene = context.scene
        scene.name = "{0}.{1}".format(
                scene.shot_name,
                names.get(scene.shot_type),
                )
        return {'FINISHED'}


class ST_NameActionsOperator(Operator):
    bl_idname = "shot_tool.name_actions"
    bl_label = "Name Actions"

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_AssignLayersOperator(Operator):
    bl_idname = "shot_tool.assign_characters_layers"
    bl_label = "Assign Characters Layers"

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_SetMetadataOperator(Operator):
    bl_idname = "shot_tool.set_metadata"
    bl_label = "Set Metadata"

    def execute(self, context):
        scene = context.scene
        render = scene.render
        shot_type = scene.shot_type


        if shot_type == SHOT_TYPE.LAYOUT:
            render.use_stamp = False

        elif shot_type == SHOT_TYPE.ANIMATION:
            render.use_stamp = True
            render.stamp_font_size = 20
            render.use_stamp_labels = True
            render.use_stamp_frame = True
            render.use_stamp_scene = True
            render.use_stamp_lens = True
            render.use_stamp_time = False
            render.use_stamp_date = False
            render.use_stamp_camera = False
            render.use_stamp_render_time = False

        elif shot_type == SHOT_TYPE.LIGHTING:
            render.use_stamp = True
            render.use_stamp_render_time = True
            render.use_stamp_memory = True

        return {'FINISHED'}


class ST_SetResolutionOperator(Operator):
    bl_idname = "shot_tool.set_resolution"
    bl_label = "Set Resolution"

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        TODO
        return {'FINISHED'}


# ############################################################
# Cleanup
# ############################################################

class ST_RemoveSequenceStripsOperator(Operator):
    bl_idname = "shot_tool.remove_sequence_strips"
    bl_label = "Remove Sequence Strips"

    def execute(self, context):
        context.scene.sequence_editor_clear()
        return {'FINISHED'}


class ST_RemoveMarkersOperator(Operator):
    bl_idname = "shot_tool.remove_markers"
    bl_label = "Remove Markers"

    def execute(self, context):
        context.scene.timeline_markers.clear()
        return {'FINISHED'}


# ############################################################
# Render
# ############################################################

class ST_SetHairSystemDefaultsOperator(Operator):
    bl_idname = "shot_tool.set_hair_system_defaults"
    bl_label = "Set Hair System Defaults"

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_SetRenderDefaultsOperator(Operator):
    bl_idname = "shot_tool.set_render_defaults"
    bl_label = "Set Render Defaults"

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        TODO
        return {'FINISHED'}


# ############################################################
# Un/Register
# ############################################################

classes = (
        ST_NameSceneOperator,
        ST_NameActionsOperator,
        ST_AssignLayersOperator,
        ST_SetMetadataOperator,
        ST_SetResolutionOperator,
        ST_RemoveSequenceStripsOperator,
        ST_RemoveMarkersOperator,
        ST_SetHairSystemDefaultsOperator,
        ST_SetRenderDefaultsOperator,
        )


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

