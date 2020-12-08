# -*- coding:utf-8 -*-

"""
    @author: Barrientos
    @date: 7/12/2020
    @version 1.0
"""

from tkinter import *
from tkinter import ttk
#import tkinter as tk
from tkinter import messagebox 
#from Draw import *
from  Core.Python.MySQLEngine import * 
import json

"""
    loginGUI: Objeto para crear una ventana de Login
"""
class loadGUI:

    """
        Constructor para el objeto loginGUI
    """
    def __init__(self,user_id):
        self.app = Tk()
        self.data = None

        #Título de la ventana
        self.app.title('Load')

        #Tamaño de la ventana
        self.appWidth = 450
        self.appHeight = 250
        self.centerWindow()
        #Titulo
        self.label = Label(self.app, text='Seleccione la imagen que desea cargar',font = 'Helvetica 16 bold')
        self.label.pack(pady=20)

        #Contenido
        self.combo = ttk.Combobox(self.app,width=17)
       
        self.combo.place(x=144,y=80)
        options = []
        
        #Botón de Load , command=self.login
        self.login = Button(self.app, command=self.load, text='Load',pady=5, padx=30)
        self.login.place(x=100, y=170, width=100)

        #Botón de Cancel , command=self.login
        self.login = Button(self.app, command=self.close_window ,text='Cancel',pady=5, padx=30)
        self.login.place(x=250, y=170, width=100)


        SQLEngine = MySQLEngine()
        SQLEngine.start()
        #Consulta SQL para buscar al usuario 
        _id = user_id
        result = SQLEngine.select("SELECT Draw.var_name as 'nombre' FROM Library JOIN Draw ON Library.int_id_draw = Draw.id WHERE int_id_user = %s;" % _id)
        print('------------------------------------',result)
        
        for rec in result:
            options.append(rec)
        self.combo['values']=options
        
        SQLEngine.close()
    
    def centerWindow(self):

        xCoordinate = int(self.app.winfo_screenwidth()/2 - self.appWidth/2)
        yCoordinate = int(self.app.winfo_screenheight()/2 - self.appHeight/2)

        self.app.geometry('%sx%s+%s+%s' % (self.appWidth,self.appHeight,xCoordinate,yCoordinate))

    
    def close_window(self):
        self.app.destroy() 
        self.app.quit()
    
    def load(self):
        imageName = self.combo.get()
        if not imageName:
            messagebox.showerror('Error', 'Seleccione una imagen de la lista, si la lista esta vacia oprima Cancel')
        else:
            SQLEngine = MySQLEngine()
            SQLEngine.start()
            self.data = SQLEngine.select("SELECT jso_data FROM Draw WHERE var_name = '%s';" % imageName,fetchOne=True)[0]
            SQLEngine.close()
            self.close_window()
    
    def run(self):
        self.app.mainloop()
  