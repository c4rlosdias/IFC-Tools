import bpy
from bpy.types import Panel
from . operators import *

class Panel_Quantity(Panel):
    bl_label        = "Quantity Take Off"
    bl_idname       = "VIEW3D_PT_quantity_takeoff"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "IFC Tools"
    
    
    def draw(self, context):
        
        props = context.scene.my_props
        layout = self.layout        
        layout.label(text="Choose the configuration file (.json):")
        row = layout.row(align=True)
        row.prop(props, 'file_settings')
        row.operator(Operator_Import.bl_idname, text='',  icon='FILE_FOLDER')

        layout.label(text="Choose the output file (.xlsx):")
        row = layout.row(align=True)
        row.prop(props, 'file_quantity')
        row.operator(Operator_Export.bl_idname, text='',  icon='FILE_FOLDER')

        row = layout.row(align=True)
        row.operator(Operator_Quantity.bl_idname, text='Generate', icon='TEXT')    