"""
Operators
"""

import bpy

from bpy.types import (
        Operator,
        )

from bpy.props import (
        FloatVectorProperty,
        )

from .defines import (
        SHOT_TYPE,
        )

TODO = False


# ############################################################
# Utils
# ############################################################

def get_animation_file(context):
    import os
    basedir, basename = os.path.split(bpy.data.filepath)
    anim_file = os.path.join(basedir, "{0}.{1}.blend".format(context.scene.shot_name,
        SHOT_TYPE.suffix.get(SHOT_TYPE.ANIMATION)))
    return anim_file


# ############################################################
# Creation
# ############################################################

class ST_NameSceneOperator(Operator):
    """Sets the scene name to <shot name>.<file type>"""
    bl_idname = "shot_tool.name_scene"
    bl_label = "Name Scene"

    def execute(self, context):
        scene = context.scene
        scene.name = "{0}.{1}".format(
                scene.shot_name,
                SHOT_TYPE.suffix.get(scene.shot_type),
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


class ST_RelinkActionsOperator(Operator):
    """Relink all the actions from the equivalent anim file"""
    bl_idname = "shot_tool.relink_actions"
    bl_label = "Relink Actions"

    def invoke(self, context, events):
        import os
        scene = context.scene

        if scene.shot_type != SHOT_TYPE.LIGHTING:
            self.report({'ERROR'}, "Relinking of actions is only supported in lighting shots")
            return {'CANCELLED'}

        # get the equivalent animation file
        anim_file = get_animation_file(context)

        if not os.path.exists(anim_file):
            self.report({'ERROR'}, "Animation file not found ({0})".format(anim_file))
            return {'CANCELLED'}

        # get all the actions from the current file
        # use the selected objects if possible
        selected_objects = context.selected_objects
        if selected_objects:
            objects = [ob for ob in selected_objects if \
                    ob.animation_data and ob.animation_data.action and \
                    not ob.animation_data.action.library]
            action_names = {ob.animation_data.action.name for ob in objects}
        else:
            objects = [ob for ob in scene.objects if \
                    ob.animation_data and ob.animation_data.action and \
                    not ob.animation_data.action.library]
            action_names = {action.name for action in bpy.data.actions \
                    if not action.library}

        # link all equivalent actions from the other file to populate the lookup table
        with bpy.data.libraries.load(anim_file, link=True, relative=True) as (data_from, data_to):
            data_to.actions = [action for action in data_from.actions if action in action_names]

        lookup_actions = {action.name: action for action in data_to.actions}

        # remap the old actions into the new one
        actions_count = 0
        for ob in objects:
            action_name = ob.animation_data.action.name
            link_action = lookup_actions.get(action_name)

            if not link_action:
                continue

            ob.animation_data.action = link_action
            print("Object \"{0}\" / Action \"{0}\"".format(
                ob.name, action_name))
            actions_count += 1

        if actions_count == 0:
            self.report({'WARNING'}, "No action was relinked")
            return {'CANCELLED'}

        else:
            self.report({'INFO'}, "{0} action{1} relinked".format(
                actions_count, " was" if actions_count == 1 else "s were"))

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
# Update
# ############################################################

class ST_UpdateBoneConstraintsOperator(Operator):
    """Re-syinc bone constraints from animation file"""
    bl_idname = "shot_tool.update_bone_constraints"
    bl_label = "Update Bone Constraints"
    bl_context = 'objectmode'

    def _valid(self, context):
        import os

        # check if file was ever saved
        if not context.blend_data.is_saved:
            self.report({'ERROR'}, "Save the file first")
            return False

        # check if file is lighting
        if not bpy.data.filepath.endswith("{0}.blend".format(SHOT_TYPE.suffix.get(SHOT_TYPE.LIGHTING))):
            self.report({'ERROR'}, "Current file is not a lighting file")
            return False

        # check if there is an anim file
        animfile = get_animation_file(context)
        if not os.path.isfile(animfile):
            self.report({'ERROR'}, "There is no anim file ({0})".format(animfile))
            return False

        return True

    def execute(self, context):
        if not self._valid(context):
            return {'CANCELLED'}

        self.report({'ERROR'}, "Not implemented yet")
        return {'CANCELLED'}


# ############################################################
# Miscellaneous
# ############################################################

class ST_SetVertexColorOperator(Operator):
    """Set vertex color for selected vertices"""
    bl_idname = "shot_tool.set_vertex_color"
    bl_label = "Set Vertex Color"
    bl_context = 'edit_mesh'

    color = FloatVectorProperty(
            name='Color',
            subtype='COLOR',
            default=(1.0, 1.0, 1.0),
            )

    def execute(self, context):
        bpy.ops.ed.undo_push(message=self.bl_idname)

        ob = context.object
        mesh = ob.data

        # go to object mode to get polygon data
        bpy.ops.object.mode_set(mode='OBJECT')

        color_layer = mesh.vertex_colors.active
        if not color_layer:
            color_layer = mesh.vertex_colors.new()

        color = self.color
        selected_vertices = [i for i, v in enumerate(mesh.vertices) if v.select]
        i = 0
        for poly in mesh.polygons:
            for v_id in poly.vertices:
                if v_id in selected_vertices:
                    color_layer.data[i].color = color
                i += 1

        bpy.ops.object.mode_set(mode='VERTEX_PAINT')
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)


# ############################################################
# Un/Register
# ############################################################

classes = (
        ST_NameSceneOperator,
        ST_NameActionsOperator,
        ST_RelinkActionsOperator,
        ST_AssignLayersOperator,
        ST_SetMetadataOperator,
        ST_SetResolutionOperator,
        ST_RemoveSequenceStripsOperator,
        ST_RemoveMarkersOperator,
        ST_SetHairSystemDefaultsOperator,
        ST_SetRenderDefaultsOperator,
        ST_SetVertexColorOperator,
        ST_UpdateBoneConstraintsOperator,
        )


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

