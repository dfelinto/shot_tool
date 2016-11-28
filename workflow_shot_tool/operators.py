"""
Operators
"""

import bpy

from bpy.types import (
        Operator,
        )

TODO = False

# ############################################################
# Creation
# ############################################################

class ST_NameActionsOperator(Operator):
    bl_idname = "shot_tool.name_actions"
    bl_label = "Name Actions"

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_NameSceneOperator(Operator):
    bl_idname = "shot_tool.name_scene"
    bl_label = "Name Scene"

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_SetStampsOperator(Operator):
    bl_idname = "shot_tool.set_stamps"
    bl_label = "Set Stamps"

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_SetResolutionOperator(Operator):
    bl_idname = "shot_tool.set_resolution"
    bl_label = "Set Resolution"

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_OutputSettingsOperator(Operator):
    bl_idname = "shot_tool.output_settings"
    bl_label = "Output Settings"

    def execute(self, context):
        TODO
        return {'FINISHED'}


# ############################################################
# Cleanup
# ############################################################

class ST_CleanSequencerOperator(Operator):
    bl_idname = "shot_tool.clean_sequencer"
    bl_label = "Clean Sequencer"

    def execute(self, context):
        TODO
        return {'FINISHED'}


class ST_RemoveMarkersOperator(Operator):
    bl_idname = "shot_tool.remove_markers"
    bl_label = "Remove Markers"

    def execute(self, context):
        TODO
        return {'FINISHED'}


# ############################################################
# Render
# ############################################################

class ST_HairSystemDefaultsOperator(Operator):
    bl_idname = "shot_tool.hair_system_defaults"
    bl_label = "Hair System Defaults"

    def execute(self, context):
        TODO
        return {'FINISHED'}


# ############################################################
# Un/Register
# ############################################################

classes = (
        ST_NameActionsOperator,
        ST_NameSceneOperator,
        ST_SetStampsOperator,
        ST_SetResolutionOperator,
        ST_OutputSettingsOperator,
        ST_CleanSequencerOperator,
        ST_RemoveMarkersOperator,
        ST_HairSystemDefaultsOperator,
        )


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

