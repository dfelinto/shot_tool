#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
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
    "author": "Dalai Felinto, Andy Goralczyk",
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

# allow for simple refresh of addon
importlib.reload(operators)
importlib.reload(ui)


from bpy.props import (
        BoolProperty,
        StringProperty,
        )


# ############################################################
# User Preferences
# ############################################################

class ShotToolPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__


# ############################################################
# Un/Register
# ############################################################

def register():
    bpy.utils.register_class(ShotToolPreferences)

    operators.register()
    ui.register()


def unregister():
    bpy.utils.unregister_class(ShotToolPreferences)

    ui.unregister()
    operators.unregister()


if __name__ == "__main__":
    register()
