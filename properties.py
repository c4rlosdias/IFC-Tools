from bpy.types import PropertyGroup
from bpy.props import StringProperty, PointerProperty, CollectionProperty



class ListObjects(PropertyGroup):
    name : StringProperty(name="list", default="")
    outro : StringProperty(name="outro", default="")


class MyProperties(PropertyGroup):
    file_settings  : StringProperty(name='', default='')
    file_quantity  : StringProperty(name='', default='')
    list_objects   : CollectionProperty(name='list', type=ListObjects)

