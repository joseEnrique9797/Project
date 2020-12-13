# -*- coding: utf8 -*-

"""
    @author: Alexis
    @date: 11/12/2020
    @version: 1.0
"""

import sys
import zlib, json, base64

"""
    La clase jsonCompress sirve para comprimir una cadena en forma de JSON y devuelve un JSON comprimido.
"""
class jsonCompress:

    """
        Constructor
    """
    def __init__(self,fileName,userId):
        self.fileName = fileName
        self.userId = userId

    """
        jsonZip comprime una JSON en formato de cadena.
        @param jsonString: JSON en forma de cadena.
        @return jsonString: Objeto JSON comprimido.
    """
    def jsonZip(self,jsonString):
        jsonString = {
            "User": self.userId,
            "FileName": self.fileName,
            "Draw": "%s" % base64.b64encode(zlib.compress(
                    json.dumps(jsonString).encode('utf-8')
                )
            ).decode('ascii')
        }
        return json.dumps(jsonString)


    """
        jsonUnzip descomprime un objeto JSON comprimido por la función jsonZip.
        @param j: Objeto JSON Comprimido.
        @param insist: Este flag (opcional) permite suprimir el error de Runtime en caso de ser False.
        @return j: Devuelve un objeto JSON descomprimido.
    """
    def jsonUnzip(self,j, insist=True):
        try:
            assert (j[self.fileName])
            assert (set(j.keys()) == {self.fileName})
        except:
            if insist:
                raise RuntimeError("JSON not in the expected format {" + str(self.fileName) + ": zipstring}")
            else:
                return j
        try:
            j = zlib.decompress(base64.b64decode(j[self.fileName]))
        except:
            raise RuntimeError("Couldn't decode/unzip the contents")

        try:
            j = json.loads(j)
        except:
            raise RuntimeError("Couldn't interpret the unzipped contents")
        return j