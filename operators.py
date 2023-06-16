import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from . functions import *

class Operator_Import(Operator):
    """O arquivo de configuração é um arquivo no formato .JSON
    com as regras estabelecidas para a medição dos quantitativos"""
    bl_idname = "cd.operator_import"
    bl_label = "Importa arquivo de Configuração"
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

class Operator_Export(Operator):
    """O arquivo de configuração é um arquivo no formato .JSON
    com as regras estabelecidas para a medição dos quantitativos"""
    bl_idname = "cd.operator_export"
    bl_label = "OK"
    bl_options = {"REGISTER", "UNDO"}

    filepath     : StringProperty(subtype="FILE_PATH")
    filter_glob  : StringProperty(default='*.xlsx', options={'HIDDEN'})

    def execute(self, context):
        props = context.scene.my_props
        props.file_quantity = self.filepath
        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}   

class Operator_Quantity(Operator):
    """Tooltip"""
    bl_idname = "cd.operator_select_requirements"
    bl_label = "Seleciona arquivo de requisitos"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            props = context.scene.my_props
            result = create_quantity(props.file_settings, props.file_quantity)
            if result == 1:
                self.report({"INFO"}, 'Operação concluída!')
            else:
                self.report({"ERROR"}, 'Não foi possível criar o arquivo de saída!:')

        except ValueError as ve:
            self.report({"ERROR"}, 'Algo deu errado : ', ve)

        return {"FINISHED"}