from bpy.types import PropertyGroup
from bpy.props import StringProperty

class MyProperties(PropertyGroup):
    file_settings  : StringProperty(name='', default='')
    file_quantity  : StringProperty(name='', default='')