"""
@author Kenneth Cruz
@date 2020-28-11
@version 1.0
-------------------
<Command x="-196.0" y="117.0" width="1" color="#000000">GoTo</Command>
{command:"GoTo", x:"-196.0", y:"117.0", width:"1", color"#000000"}
"""

import re 
import json

class XMLtoJSON: 
    def __init__(self, xmlFilename):
        self.jsonFilename = "recovered"+xmlFilename.replace('.xml', '.json')
        self.xmlFilename = xmlFilename

        self.process()

    #split de los atributos de la etiqueta
    def attributeProcess(self, tag, tagname): 
        return re.split(r'>%s</Command>'%(tagname), tag)[0].split(" ")[1:] 

    #Prepara (limpia) la cadena para luego ser transformada en un arreglo
    def stringProcess(self, string): 
        return (string.replace("=", " ")).replace("\"", "").split(" ")

    #genera un arreglo a partir de una cadena
    def getArray(self, process, tagname): 
        array = [ self.stringProcess(x) for x in  process]
        array.insert(0, ["command", tagname])

        return array 

    #convierte el arreglo en un diccionario
    def getDictionary(self, array): 
        return { array[i][0]: array[i][1] for i in range(0, len(array)) }

    #Extrae el texto contenido en la etiqueta
    def tagname(self, tag): 
        match = re.search(r'>[a-zA-Z]+<', tag).group()
        return (match.replace(">", "")).replace("<", "")

    #Arreglo con todas las etiquetas del archivo XML
    def tags(self): 
        f = open(self.xmlFilename, 'r')

        tags = f.read().split("\n")
        tags = tags[2:len(tags)-2]

        f.close()
        return tags

    #Genera un objeto JSON a partir de un diccionario llamado xml
    def process(self): 
        xml = {}
        tags = self.tags()
        for i in range(len( tags )): 
            tag = tags[i].strip()
            if tag != "":
                name = self.tagname(tag) 
                process = self.attributeProcess(tag, name)
                array = self.getArray(process, name)

                xml[i] = self.getDictionary(array)
        
        self.obj = json.dumps(xml, sort_keys=True)

    def createJSON(self): 
        f = open(self.jsonFilename, 'w')
        f.write( self.obj )
        f.close()