"""
@author Kenneth Cruz
@date 2020-29-11
@version 1.0

-------------------
{command:"GoTo", x:"-196.0", y:"117.0", width:"1", color"#000000"}
<Command x="-196.0" y="117.0" width="1" color="#000000">GoTo</Command>
"""

import xml.etree.ElementTree as xmlTree
import json
import re 

class JSONtoXML: 

    def __init__(self, jsonFilename): 
        self.xmlFilename = "recovered"+jsonFilename.replace('.json', '.xml')
        #carga el documento JSON como un diccionario
        self.jsonFile = json.load(open(jsonFilename,encoding="utf8"))
        # Crea un árbol de la estructura xml
        self.root = xmlTree.Element('GraphicsCommands')     

    #Convierte un diccionario en una etiqueta XML con sus atributos
    def processJSON(self, dictionary):
        command = xmlTree.Element('Command')    
        tag = ""

        for key, value in dictionary.items():
            if re.search(r"([A-Z][a-z]+)+", value):
                tag = value
            else:  
                command.set(key, value)
        command.text = tag
        return command

    def createXML(self): 
        for i in range(0, len( self.jsonFile) ): 

            self.root.append( 
                    self.processJSON( self.jsonFile[str(i)] ) 
                )
        
        #objeto (xml.etree.ElementTree) con todos los nodos del documento XML final
        tree = xmlTree.ElementTree(self.root)

        #Crea el archivo XML en memoria
        with open(self.xmlFilename, "wb") as files: 
            tree.write(files)