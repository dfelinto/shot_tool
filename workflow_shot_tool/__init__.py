#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================

bl_info = {
    "name": "Shot Tool",
    "author": "Dalai Felinto, Andy Goralczyk, Pablo Vazquez",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "Tool Shelf",
    "description": "Tools for shot setup",
    "warning": "",
    "wiki_url": "",
    "category": "Workflow",
    }


import bpy
import importlib

from . import operators
from . import ui

from .defines import (
        SHOT_TYPE,
        )

from bpy.props import (
        EnumProperty,
        StringProperty,
        )

# allow for simple refresh of addon
importlib.reload(operators)
importlib.reload(ui)


# ############################################################
# User Preferences
# ############################################################

class ShotToolPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__


# ############################################################
# Un/Register
# ############################################################

classes = (
        ShotToolPreferences,
        )


def register():
    bpy.types.Scene.shot_name = StringProperty (
            name="Shot Name",
            default="",
            options={'HIDDEN'},
            )

    bpy.types.Scene.shot_type = EnumProperty (
            name="Shot Type",
            items=(
                (SHOT_TYPE.LAYOUT, "Layout", ""),
                (SHOT_TYPE.ANIMATION, "Animation", ""),
                (SHOT_TYPE.LIGHTING, "Lighting", ""),
                ),
            default=SHOT_TYPE.LAYOUT,
            options={'HIDDEN'},
            )

    for c in classes:
        bpy.utils.register_class(c)

    operators.register()
    ui.register()


def unregister():
    del bpy.types.Scene.shot_name
    del bpy.types.Scene.shot_type

    for c in classes:
        bpy.utils.unregister_class(c)

    ui.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
