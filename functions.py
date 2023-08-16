from blenderbim.bim.ifc import IfcStore
import json
import ifcopenshell.util.element as util
import pandas as pd

def create_quantity(json_file, xlsx_file):
    if xlsx_file != '':
        with open(json_file) as file:
            settings = json.load(file)

        ifc = IfcStore.file
        elements = ifc.by_type('IfcElement')
        ttl = len(elements)

        l_description, l_unit, l_quantity, l_eap = [], [], [], []
        c = 1

        for element in elements:
            p = round((100*c )/ttl, 0)
            print(f'Analyzing elements : {p}%')
            ifc_class = element.is_a()

            # Obtem uma lista com os serviços da classe ifc do elemento
            l_services = [(x , settings[x]) for x in settings if settings[x]['ifc_class'] == ifc_class]
            
            for service in l_services:  
                eap = service[0] 
                service=service[1]

                # Obtem descrição
                desc_group = ''
                if service['is_material']:
                    materials = util.get_materials(element)
                    if materials:
                        for material in materials:
                            desc_group = material.Name
                            # Obtem as quantidades
                            tot_quantity = 0
                            for quant in service['quantity']:
                                prop_quant= quant.split('..')
                                q = util.get_pset(element=element, name=prop_quant[0], prop=prop_quant[1])
                                if q:
                                    tot_quantity += q
                                              
                            if tot_quantity > 0:
                                l_description.append(desc_group.strip())              
                                l_eap.append(eap)
                                l_unit.append(service['unit'])                    
                                l_quantity.append(round(tot_quantity, 2))
                else:
                    # Obtem a lista de propriedades que descrevem o serviço
                    descriptions = service['property'] 
                    # Se não é uma lista e sim uma string, esta será a descrição
                    if type(descriptions) == str:
                        desc_group = descriptions
                    else:                                  
                        for description in descriptions:                            
                            # Verifica se é uma propriedade ou um atributo
                            if '..' in description:                                                      
                                pset_desc = description.split('..')[0] 
                                prop_desc = description.split('..')[1]
                                item = util.get_pset(element=element, name=pset_desc, prop=prop_desc)
                                
                            else:
                                atribs = element.get_info()
                                item = atribs[description] if description in atribs else description
                                
                            # se existe um item, concatena com as outras propriedades da lista
                            if item:
                                desc_group = desc_group+ ' ' + str(item)

                    # Obtem as quantidades
                    tot_quantity = 0
                    for quant in service['quantity']:
                        if type(quant) == float or type(quant) == int:
                            tot_quantity += quant
                        else:
                            prop_quant= quant.split('..')
                            if len(prop_quant) > 1:
                                q = util.get_pset(element=element, name=prop_quant[0], prop=prop_quant[1])
                                if q:
                                    tot_quantity += q

                    # Acrescenta um novo quantitativo à lista de serviços
                    if desc_group != '' and tot_quantity > 0:
                        l_description.append(desc_group.strip())
                        l_eap.append(eap)
                        l_unit.append(service['unit'])
                        l_quantity.append(round(tot_quantity, 2))
            c += 1

        dic = {
            'EAP'          : l_eap,
            'DESCRIPTION'  : l_description,
            'UNIT'         : l_unit,
            'QUANTITY'     : l_quantity
        }

        df = pd.DataFrame(dic)
        dfg = pd.DataFrame(df.groupby(['EAP', 'DESCRIPTION', 'UNIT']).sum())
        dfg.to_excel(xlsx_file , engine='openpyxl')
        return 1
    else:
        return 0