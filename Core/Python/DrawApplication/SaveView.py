# -*- coding:utf-8 -*-

"""
    @author: zunigAndres
    @date: 07/12/2020
    @version 1.0
"""

from tkinter import *
from tkinter import messagebox 

class SaveWindow:

    """
        Constructor para el objeto userManagerGUI
    """
    def __init__(self):
        # llama al metodo que contruye la ventana
        self.window = Tk()
        self.generateUI()
    
    def generateUI(self):        
        #Título de la ventana
        self.window.title('Guardar Proyecto')

        #Tamaño de la ventana
        self.window.geometry("350x140")

        #Mantiene la ventana fija para evitar que el diseño se vea afectado
        self.window.resizable(False, False)
        

        #TextBox que recolecte el nombre con el que se guardara el proyecto
        Label(self.window, text='Guardar archivo como').place(x=15,y=25)
        self.FileName = StringVar()
        self.FileName = Entry(self.window, textvariable=self.FileName)
        self.FileName.place(x=20, y=60, width=300)

        #------ Seccion del DataView ------- 
        Button(self.window, text = 'Cancelar', command = self.SaveCancell).place(x=80, y=100, width=120)  
        Button(self.window, text = 'Guardar', command = self.SaveFinish).place(x=210, y=100, width=120)  

    def SaveFinish(self):
        if len(self.FileName.get()) > 0:
            value = self.FileName.get()
            self.window.destroy()
            return value
        else:
            messagebox.showwarning("Erro","El archivo debe tener un nombre")

    def SaveCancell(self):
        self.window.destroy()
        return None

    """
        run: Ejecuta la venta de permitsistracion de usuarios
    """
    def run(self):
        self.window.mainloop()