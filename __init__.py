# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Ifc Tools",
    "author" : "Carlos Dias",
    "description" : "Toolset for manipulating IFC files",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
import os
import sys
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))

from . operators import *
from . panels import *
from . properties import MyProperties

    
classes = [
    Panel_Quantity,
    Operator_Import,
    Operator_Export,
    Operator_Quantity,
    MyProperties
]

def register():
    for cls in classes:
        register_class(cls)
    Scene.my_props = PointerProperty(type=MyProperties)

def unregister():
    del Scene.my_props
    for cls in classes:
        unregister_class(cls)
