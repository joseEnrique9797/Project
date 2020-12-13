# -*- coding:utf-8 -*-

"""
    @author: zunigAndres
    @date: 27/11/2020
    @version 1.0
"""

from tkinter import *
from tkinter import messagebox 
from tkinter import ttk 
import tkinter.font as tkFont
from ..MySQLEngine import *

"""
    userManagerGUI: Objeto para crear una ventana que muestra las opciones para permitsistrar los usuarios del Programa
"""
class userManagerGUI:

    """
        Constructor para el objeto userManagerGUI
    """
    def __init__(self,draw=None):
        # llama al metodo que contruye la ventana
        self.drawBack = draw
        self.window = Tk()
        self.generateUI()

        #Cargar todos los usuarios que estan en la base de datos
        self.SQLEngine = MySQLEngine()
        self.refreshDataView()

    def generateUI(self):        
        #Título de la ventana
        self.window.title('Administración de Usuarios')

        #Tamaño de la ventana
        self.window.geometry("960x540")

        #Mantiene la ventana fija para evitar que el diseño se vea afectado
        self.window.resizable(False, False)
        
        #estilos para crear titulos
        TitleStyles = tkFont.Font(family="Lucida Grande", size=18)
        
        #------ Seccion del DataView ------- 
        Button(self.window, text = 'Editar', command = self.edit).place(x=20, y=80, width=150)  
        Button(self.window, text = 'Cambiar Estado', command = self.changeState).place(x=190, y=80, width=150)  
        Button(self.window, text = 'Cambiar Permisos', command = self.changePrivileges).place(x=360, y=80, width=150)  
        
        self.dataView = ttk.Treeview(self.window, columns=("#1","#2","#3"))
        self.dataView.pack()
        self.dataView.heading("#0", text="Indice")
        self.dataView.heading("#1", text="Nombre")
        self.dataView.heading("#2", text="Estado")
        self.dataView.heading("#3", text="Administrador")
        self.dataView.place(x=20, y=120)
        self.dataView.column("#0", width=50)
        self.dataView.column("#2", width=100)
        self.dataView.column("#3", width=150)

        #------ Panel de Creacion de Usuario ------- 

        #Muestra el titulo de la seccion
        Label(self.window, text='Crear un nuevo usuario', font=TitleStyles).place(x=650,y=30)

        Label(self.window, text='Nombre').place(x=635,y=70)
        self.createName = StringVar()
        self.createName = Entry(self.window, textvariable=self.createName)
        self.createName.place(x=720, y=70, width=200)

        #Campo para el TextBox Contraseña
        Label(self.window, text='Contraseña').place(x=635,y=100)
        self.createPassword = StringVar()
        self.createPassword = Entry(self.window, textvariable=self.createPassword)
        self.createPassword.place(x=720, y=100, width=200)
        
        #Campo Checkbox para el campo administrador
        self.checkvalue = BooleanVar()
        self.check = Checkbutton(self.window, text="Permisos de Administrador", variable=self.checkvalue,command=self.toggle)
        self.check.place(x=720, y=130)
        
        # button 1 
        Button(self.window, text = 'Crear Usuario', command = self.newUser).place(x=720, y=160, width=130)     
        
        #Compo para el TextBox Nombre
        Label(self.window, text='Editar campos de usuario', font=TitleStyles).place(x=650,y=250)


        #Compo para el TextBox Nombre
        Label(self.window, text='Nombre').place(x=635,y=300)
        self.editName = StringVar()
        self.editName = Entry(self.window, textvariable=self.editName)
        self.editName.place(x=720, y=300, width=200)

        #Campo para el TextBox Contraseña
        Label(self.window, text='Contraseña').place(x=635,y=330)
        self.editPassword = StringVar()
        self.editPassword = Entry(self.window, textvariable=self.editPassword)
        self.editPassword.place(x=720, y=330, width=200)
        
        # button 1 
        Button(self.window, text = 'Guardar Cambios', command = self.saveChanges).place(x=720, y=360, width=130)     

        Button(self.window, text = 'Volver', command = self.goBack).place(x=50, y=370, width=130)

    def goBack(self):
        self.window.destroy()
        self.drawBack.deiconify()

    def changeState(self):
        
        if len(self.dataView.selection()) > 0:
            index = int(self.dataView.item(self.dataView.selection())['text'])
            
            self.SQLEngine.start()
            self.SQLEngine.callProcedure("userChangeState", index)
            self.SQLEngine.close()            
            self.refreshDataView()
            
            self.dataView.selection_remove(self.dataView.selection())
        else:
            messagebox.showerror("Error","No se ha seleccionado ningún usuario")
        

    def toggle(self):
        if self.checkvalue.get():
            self.checkvalue.set(False)
        else:
            self.checkvalue.set(True)

    def changePrivileges(self):

        if len(self.dataView.selection()) > 0:
            index = int(self.dataView.item(self.dataView.selection())['text'])
            
            self.SQLEngine.start()
            self.SQLEngine.callProcedure("userChangeAdmin", index)
            self.SQLEngine.close()            
            self.refreshDataView()            
            self.dataView.selection_remove(self.dataView.selection())
        else:
            messagebox.showerror("Error","No se ha seleccionado ningún usuario")
        
    def refreshDataView(self):
        self.dataView.delete(*self.dataView.get_children())
        
        self.SQLEngine.start()
        results = self.SQLEngine.select("SELECT * FROM User;")
        self.SQLEngine.close()

        for result in results:
            self.dataView.insert("", END, text=str(result[0]), values =(result[1],result[4],result[3]))

    # metodo que muestro los campos para crear un nuevo usuario
    def newUser(self):

        #Obtener el valor de las variables de TKinter
        userName = self.createName.get()
        password = self.createPassword.get()
        admin = self.checkvalue.get()

        if len(userName) > 3 and len(password) > 3:
            
            self.SQLEngine.start()
            self.SQLEngine.insert("INSERT INTO User (var_userName,var_password,bit_admin) VALUES ('%s','%s',%s);" % (userName,password,admin))
            self.SQLEngine.close()

            self.createName.delete(0, 'end')
            self.createPassword.delete(0, 'end')

            self.refreshDataView()
            messagebox.showinfo("Exito","Nuevo Usuario creado")
        else: 
            messagebox.showinfo("Error","El usuario debe tener un nombre y contraseña mayor a 3 caracteres")

    def edit(self):
        
        if len(self.dataView.selection()) > 0:

            index = self.dataView.item(self.dataView.selection())['text']

            self.SQLEngine.start()

            status =self.SQLEngine.select("SELECT enu_state FROM User WHERE id=%s;" % str(index),fetchOne=True)[0]
            
            if status == 'inactive':
                messagebox.showinfo("Alerta","El Usuario inactivo se activara para poder editar sus campos")
                self.SQLEngine.callProcedure("userChangeState", index)

            username,password = self.SQLEngine.select("SELECT var_userName, var_password FROM User WHERE id = %s;" % str(index))[0]
            self.refreshDataView()
            self.SQLEngine.close()

            self.editName.delete(0,'end')
            self.editName.insert(0,username)
            self.editPassword.delete(0, 'end')
            self.editPassword.insert(0,password)
        else:
            messagebox.showerror("Error","No se ha seleccionado ningún Elemento")


    def saveChanges(self):

        if len(self.dataView.selection()) > 0:
            index = self.dataView.item(self.dataView.selection())['text']
            userName = self.editName.get()
            password = self.editPassword.get()
            
            self.SQLEngine.start()
            self.SQLEngine.callProcedure("userUpdate", index, userName, password)
            self.SQLEngine.close()
         
            self.refreshDataView()
            messagebox.showinfo("Exito","La informacion se actualizo correctamente")
            self.editName.delete(0, 'end')
            self.editName.insert(0,'')
            self.editPassword.delete(0, 'end')
            self.editPassword.insert(0,'')

            self.dataView.selection_remove(self.dataView.selection())

        else:
            messagebox.showerror("Error","No se ha seleccionado ningún Elemento")

    """
        run: Ejecuta la venta de permitsistracion de usuarios
    """
    def run(self):
        self.window.mainloop()