from bpy.types import Operator
from bpy.props import StringProperty
from bpy.path import ensure_ext
from . functions import *

import multiprocessing
import random
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
from blenderbim.bim.ifc import IfcStore
import blenderbim.tool as tool

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

    filename_ext = '.xlsx'
    filepath     : StringProperty(subtype="FILE_PATH")
    #filter_glob  : StringProperty(default='*.xlsx', options={'HIDDEN'}, )

    def execute(self, context):
        try:
            self.filepath = ensure_ext(self.filepath, '.xlsx')
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
        self.filepath = ensure_ext(self.filepath, '.xlsx')
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"} 
    
class Operator_Setorize(Operator):
    """Tooltip"""
    bl_idname = "cd.operator_setorize"
    bl_label = "Setorize objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            props = context.scene.my_props
            ifc_file = IfcStore.file
            tree = ifcopenshell.geom.tree()
            settings = ifcopenshell.geom.settings()
            iterator = ifcopenshell.geom.iterator(settings, ifc_file, multiprocessing.cpu_count())
            
            if iterator.initialize():
                while True:
                    tree.add_element(iterator.get_native())
                    if not iterator.next():
                        break
            
            spaces=ifc_file.by_type('IfcSpace')
            r =random.random
            
            for space in spaces:
                colored = False
                setor = space.Name
                print("space name " + setor)               
                if space.PredefinedType == "USERDEFINED" and space.ObjectType.upper() == "SETOR": 
                    c = 0                   
                    elements = tree.select(space, completely_within=False)
                    r = random.randint(0,255)/255
                    g = random.randint(0,255)/255
                    b = random.randint(0,255)/255
                    
                    print(f"Processing elements of {space.Name}...")
                    for element in elements:                        
                        storey = ifcopenshell.util.element.get_container(element)                        
                        if storey and not element.is_a('IfcSpace'):
                            sector_name = storey.Name + '_' + setor
                            pset = ifcopenshell.api.run("pset.add_pset", ifc_file, product=element, name=props.pset_name)
                            ifcopenshell.api.run("pset.edit_pset", ifc_file, pset=pset, properties={props.prop_name : sector_name})                            
                            obj = tool.Ifc.get_object(element)
                            obj.color = (r,g,b, 1)
                            colored = True
                            c += 1
                    print(f'{c} elements processed...')
            if colored:
                area = next(area for area in context.screen.areas if area.type == "VIEW_3D")
                area.spaces[0].shading.color_type = "OBJECT"                             
                                        
            self.report({"INFO"}, 'Operation completed!')
            print('Operation completed!')

        except ValueError as ve:
            self.report({"ERROR"}, 'Something went wrong: ', ve)

        return {"FINISHED"}  
