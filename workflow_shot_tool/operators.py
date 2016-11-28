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
    """Sets the scene name to <shot name>.<file type>"""
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
    """Names all proxy object actions across the scene according to <shot name>"""
    bl_idname = "shot_tool.name_actions"
    bl_label = "Name Actions"

    def execute(self, context):
        lookup = {
                'Agent_high_proxy': 'agent',
                'Boris_high_proxy': 'boris',
                'Barber_high_proxy': 'barber',
                'picture_frame_appel_imitation_proxy': 'picture_frame_painting',
                'books_proxy': 'books',
                'bust_proxy': 'bust',
                'barbershop_interior_proxy': 'barbershop_interior',
                'chair_barbershop1_proxy': 'chair_barbershop1',
                'chair_barbershop2_proxy': 'chair_barbershop2',
                'chair_barbershop3_proxy': 'chair_barbershop3',
                }

        scene = context.scene
        shot_name = scene.shot_name

        for ob in context.scene.objects:
            if ob.animation_data and ob.animation_data.action:
                ob_name = ob.name
                action = ob.animation_data.action
                action_name = lookup.get(ob_name)

                if not action_name:
                    if ob_name.endswith('_proxy'):
                        action_name = ob_name[:-6]
                    else:
                        action_name = ob_name

                action.name = "{0}.{1}".format(
                        shot_name,
                        action_name,
                )

        return {'FINISHED'}


class ST_AssignLayersOperator(Operator):
    """This puts the character group instances and their proxies on layers, depending on the file type"""
    bl_idname = "shot_tool.assign_characters_layers"
    bl_label = "Assign Characters Layers"

    @classmethod
    def poll(cls, context):
        return context.scene.shot_type in {
                SHOT_TYPE.ANIMATION,
                SHOT_TYPE.LIGHTING,
                }

    def execute(self, context):
        lookup = {
                SHOT_TYPE.ANIMATION: {
                'Agent_high_proxy': 0,
                'Agent_high': 10,
                'Boris_high_proxy': 1,
                'Boris_high': 11,
                'Barber_high_proxy': 2,
                'Barber_high': 12,
                },
                SHOT_TYPE.LIGHTING: {
                'Agent_high_proxy': 12,
                'Agent_high': 2,
                'Boris_high_proxy': 13,
                'Boris_high': 3,
                'Barber_high_proxy': 14,
                'Barber_high': 4,
                },
                }

        scene = context.scene
        objects = scene.objects
        for name, layer in lookup.get(scene.shot_type).items():
            ob = objects.get(name)

            if not ob:
                continue

            ob.layers = [(i == layer) for i in range(20)]

        return {'FINISHED'}


class ST_SetMetadataOperator(Operator):
    """Sets output metadata (stamp) according to file type"""
    bl_idname = "shot_tool.set_metadata"
    bl_label = "Set Metadata"

    def execute(self, context):
        scene = context.scene
        render = scene.render
        shot_type = scene.shot_type


        if shot_type == SHOT_TYPE.LAYOUT:
            render.use_stamp = True

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
            render.use_stamp = False
            render.use_stamp_render_time = True
            render.use_stamp_memory = True

        return {'FINISHED'}


class ST_SetResolutionOperator(Operator):
    bl_idname = "shot_tool.set_resolution"
    bl_label = "Set Resolution"

    def execute(self, context):
        render = context.scene.render
        render.field_order = 'EVEN_FIRST'
        render.fps = 24
        render.fps_base = 1.0
        render.pixel_aspect_x = 1.0
        render.pixel_aspect_y = 1.0
        render.resolution_percentage = 100
        render.resolution_x = 2048
        render.resolution_y = 858
        render.use_fields = False
        render.use_fields_still = False
        return {'FINISHED'}


# ############################################################
# Cleanup
# ############################################################

class ST_RemoveSequenceStripsOperator(Operator):
    """Cleans up all strip data from the sequencer"""
    bl_idname = "shot_tool.remove_sequence_strips"
    bl_label = "Remove Sequence Strips"

    def execute(self, context):
        context.scene.sequence_editor_clear()
        return {'FINISHED'}


class ST_RemoveMarkersOperator(Operator):
    """Cleans up all markers globally"""
    bl_idname = "shot_tool.remove_markers"
    bl_label = "Remove Markers"

    def execute(self, context):
        for scene in bpy.data.scenes:
            scene.timeline_markers.clear()
        return {'FINISHED'}


# ############################################################
# Render
# ############################################################

class ST_SetHairSystemDefaultsOperator(Operator):
    bl_idname = "shot_tool.set_hair_system_defaults"
    bl_label = "Set Hair System Defaults"

    def execute(self, context):
        cycles_curves = context.scene.cycles_curves
        cycles_curves.primitive = 'LINE_SEGMENTS'
        cycles_curves.shape = 'RIBBONS'
        return {'FINISHED'}


class ST_SetRenderDefaultsOperator(Operator):
    bl_idname = "shot_tool.set_render_defaults"
    bl_label = "Set Render Defaults"

    def execute(self, context):
        cycles = context.scene.cycles
        cycles.max_bounces = 2
        cycles.min_bounces = 2
        cycles.diffuse_bounces = 2
        cycles.glossy_bounces = 2
        cycles.transmission_bounces = 2
        cycles.volume_bounces = 0
        cycles.transparent_min_bounces = 32
        cycles.transparent_max_bounces = 32
        cycles.use_transparent_shadows = True
        cycles.caustics_reflective = False
        cycles.caustics_refractive = False
        cycles.blur_glossy = 2.0

        cycles.samples = 800
        cycles.preview_samples = 0
        cycles.aa_samples = 4
        cycles.preview_aa_samples = 4
        cycles.diffuse_samples = 1
        cycles.glossy_samples = 1
        cycles.transmission_samples = 1
        cycles.ao_samples = 1
        cycles.mesh_light_samples = 1
        cycles.subsurface_samples = 1
        cycles.volume_samples = 1
        cycles.use_square_samples = False
        cycles.progressive = 'PATH'
        cycles.seed = 0
        cycles.use_animated_seed = True
        cycles.sample_clamp_direct = 0.0
        cycles.sample_clamp_indirect = 2.0
        cycles.sample_all_lights_direct = True
        cycles.sample_all_lights_indirect = True

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

