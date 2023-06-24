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
            print(f'Analisando elementos : {p}%')
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
                            quant= service['quantidade'].split('.')
                            quantity = util.get_pset(element=element, name=quant[0], prop=quant[1])                
                            if quantity:
                                l_description.append(desc_group.strip())              
                                l_eap.append(eap)
                                l_unit.append(service['unidade'])                    
                                l_quantity.append(round(quantity, 2))
                else:
                    descriptions = service['prop_descricao']
                    pset_desc = service['pset_descricao']            
                    for description in descriptions:                
                        item = util.get_pset(element=element, name=pset_desc, prop=description)
                        if item:
                            desc_group = desc_group+ ' ' + str(item)

                    # Obtem as quantidades
                    if service['quantidade'] == 'contador':
                        quantity = 1.0
                    else:
                        quant= service['quantidade'].split('.')
                        quantity = util.get_pset(element=element, name=quant[0], prop=quant[1])
                    
                    if desc_group != '' and quantity:
                        l_description.append(desc_group.strip())
                        l_eap.append(eap)
                        l_unit.append(service['unidade'])
                        l_quantity.append(round(quantity, 2))
            c += 1

        dic = {
            'EAP'        : l_eap,
            'DESCRIÇÃO'  : l_description,
            'UNIDADE'    : l_unit,
            'QUANTIDADE' : l_quantity
        }

        df = pd.DataFrame(dic)
        dfg = pd.DataFrame(df.groupby(['EAP', 'DESCRIÇÃO', 'UNIDADE']).sum())
        print (dfg)
        dfg.to_excel(xlsx_file + '.xlsx')
        dfg.to_csv(xlsx_file + '.csv')
        return 1
    else:
        return 0