import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from . functions import *

class Operator_Import(Operator):
    """O arquivo de configuração é um arquivo no formato .JSON
    com as regras estabelecidas para a medição dos quantitativos"""
    bl_idname = "cd.operator_import"
    bl_label = "Import configuration file"
    bl_options = {"REGISTER", "UNDO"}

    filepath     : StringProperty(subtype="FILE_PATH")
    filter_glob  : StringProperty(default='*.json', options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.my_props
        props.file_settings = self.filepath
        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}   


class Operator_Quantity(Operator):
    """Tooltip"""
    bl_idname = "cd.operator_select_requirements"
    bl_label = "Generate spreadsheet file"
    bl_options = {"REGISTER", "UNDO"}

    filepath     : StringProperty(subtype="FILE_PATH")
    filter_glob  : StringProperty(default='*.xlsx', options={'HIDDEN'})

    def execute(self, context):
        try:
            props = context.scene.my_props
            props.file_quantity = self.filepath
            result = create_quantity(props.file_settings, props.file_quantity)
            if result == 1:
                self.report({"INFO"}, 'Operation completed!')
            else:
                self.report({"ERROR"}, 'Could not write output file!')

        except ValueError as ve:
            self.report({"ERROR"}, 'Something went wrong: ', ve)

        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"} 