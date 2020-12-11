# -*- codig:utf8 -*-

"""
    @author: Alexis
    @date: 04/12/2020
    @version 1.0
"""

# Para instalar el conector de mysql en python
# sudo -H pip3 install mysql-connector-python

import mysql.connector
import configparser

"""
    La clase MySQLEngine gestiona las conexiones y las consultas realizadas a la base de datos especificada
    por el archivo config.ini el cual es configurable para establecer conexiones a diferentes bases de datos
    y diferentes usuarios.
"""
class MySQLEngine:

    """ 
        Constructor 
    """
    def __init__(self):
        config = configparser.ConfigParser()

        # Se lee el archivo de configuración config.ini
        config.read('Core/Scripts/config.ini')

        # Se recuperan los valores de configuración desde el objeto config
        self.host = config.get('MariaDB Server','host')
        self.port = config.get('MariaDB Server','port')
        self.user = config.get('MariaDB Server','user')
        self.password = config.get('MariaDB Server','password')
        self.database = config.get('MariaDB Server','database')

    """
        start es la función que comienza o establece la conexión hacia la base de datos especificada en el constructor.
    """
    def start(self):

        try:
            self.conector = mysql.connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
            ) 
            self.link = self.conector.cursor()

            print("Established Connection in: %s" % self.conector)

        except Error as e:
            print("Error Establishing Connection: %s " % e)

    """
        select es la función encargada de realizar las consultas requeridas.
        @param query: Es una consulta SQL.
    """
    def select(self,query,fetchOne=False):
        self.link.execute(query,multi=True)
        
        if fetchOne:
            return self.link.fetchone()
        else:
            return self.link.fetchall()

    def insert(self,query):
        self.link.execute(query,multi=True)
        self.conector.commit()
        print("Data Inserted Successfully")
        return self.link.lastrowid

    def callProcedure(self,name,*args,fetchOne=False)
        self.link.callproc(name,args)

        if fetchOne:
            return self.link.fetchone()
        else:
            return self.link.fetchall()

    """
        close cierra la conexión hacia la base de datos.
    """
    def close(self):
        if self.conector.is_connected():
            self.link.close()
            self.conector.close()
            print("Connection Closed")