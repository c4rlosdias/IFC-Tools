# IFC Tools

set of Blender AddOn application tools for manipulation of IFC files:

## Quantity Take Off:
    
**Extracts a quantity spreadsheet from an IFC file**
extracts a list of quantities from an IFC file according to measurement rules defined in a JSON file.

The configuration file is defined as follows:
~~~~javascript
    {
        "<measure name>" : {
            "ifc_class"        : "<ifc class>",
            "is_material"      : true | false,
            "property"         : [<list of properties or attributes>] or "<description>",
            "unit"             : "<unit of measure>",
            "quantity"         : ["<list of quantities or numbers to add>"]
        },

        (...)    

    }
~~~~


The values of each key must be populated according to the following rules:

Key   | Value
:----- | :------
ifc_class | IFC class of the element to be measured. e.g. "IfcWall"
is_material | true if quantification is made for each material of the element, otherwise false
property | A list of properties or attributes that will define the description of the service to be measured. In the case of property, the property set name should be written followed by the property name separated by two dots. e.g. "Pset_WallCommon..IsExternal". If the value is a string, then this string will enter as a service description.
unit | unit of measure of the property. e.g. "m²"
quantity | A list of quantities and/or number to sum. the quantity set name should be written followed by the property name separated by a dot. e.g. "Qto_BaseQuantities..NetSideArea"

Download the last version in [Releases](https://github.com/c4rlosdias/IFC-Tools/releases)

Download JSON sample file in [sample.json](https://github.com/c4rlosdias/IFC-Tools/blob/main/settings.json)

## Sectorizes Objects:
    
**Sectorizes objects adding sector names to properties**
populates a given property of a given property set with the name of the space (IfcSpace) that surrounds it. All elements that are inside spaces with the value 'USERDEFINED' in the predefinedtype attribute and 'sector' in the ObjectType attribute will have the given property set created and the property will have as value the concatenated floor with the name of the space.
