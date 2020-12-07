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

    def __init__(self): 
        #self.xmlFilename = "recovered"+jsonFilename.replace('.json', '.xml')
        #carga el documento JSON como un diccionario
        #self.jsonFile = json.load(open(jsonFilename,encoding="utf8"))
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

    def createXML(self,data): 
        dictionary = json.loads(data)
        for i in range(0, len(dictionary) ): 

            self.root.append( 
                    self.processJSON( dictionary[str(i)] ) 
                )
        
        #objeto (xml.etree.ElementTree) con todos los nodos del documento XML final
        tree = xmlTree.ElementTree(self.root)
        tree = tree.getroot()
        #Crea el archivo XML en memoria
        """
        with open(self.xmlFilename, "wb") as files: 
            tree.write(files)
        """
        xmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n"+xmlTree.tostring(tree).decode()
        xmlString = xmlString.replace("<GraphicsCommands>","<GraphicsCommands>\n")
        xmlString = xmlString.replace("</Command>","</Command>\n")
        xmlString = xmlString.replace("<Command","    <Command")

        return xmlString