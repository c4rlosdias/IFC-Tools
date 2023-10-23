from bpy.types import PropertyGroup
from bpy.props import StringProperty, PointerProperty, CollectionProperty



class ListObjects(PropertyGroup):
    name : StringProperty(name="list", default="")
    outro : StringProperty(name="outro", default="")


class MyProperties(PropertyGroup):
    file_settings  : StringProperty(name='', default='')
    file_quantity  : StringProperty(name='', default='')
    pset_name      : StringProperty(name="")
    prop_name      : StringProperty(name="")
    domain         : StringProperty(name="")

