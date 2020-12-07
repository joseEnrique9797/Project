"""
@author Kenneth Cruz
@date 2020-28-11
@version 1.0
"""

from XMLtoJSON import XMLtoJSON
from JSONtoXML import JSONtoXML

if __name__ == "__main__":
    #path del archivo .json
    jsonFilename = 'recoveredtest_fill.json'
    (JSONtoXML(jsonFilename=jsonFilename)).createXML()

    #path del archivo .xml
    xmlFilename = 'test_fill.xml'
    #(XMLtoJSON(xmlFilename=xmlFilename)).createJSON()