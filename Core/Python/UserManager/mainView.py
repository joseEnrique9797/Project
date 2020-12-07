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

class user:
       
    def __init__(self, index, name, password, permits, available):
        self.index = index
        self.name = name
        self.password = password
        self.permits = permits
        self.available = available

    def __str__(self):
     return self.name

    def permitsStr(self):
        if self.permits:
            return "Administrador"
        else:
            return "Simple"
    def availableStr(self):
        if self.available:
            return "Activo"
        else:
            return "Inactivo"
    

"""
    userManagerGUI: Objeto para crear una ventana que muestra las opciones para permitsistrar los usuarios del Programa
"""
class userManagerGUI:

    """
        Constructor para el objeto userManagerGUI
    """
    def __init__(self):
        # llama al metodo que contruye la ventana
        self.window = Tk()
        self.generateUI()

        self.Selected = None

        a = user(1,"Andres","AndZun.123", True, True)
        b = user(2,"Jose","Kamina321", True, False)
        c = user(3,"Kenneth","CodeMaster91", False, False)
        d = user(4,"Alexis","LinuxBitch", False, True)
        
        self.users = [a,b,c,d]

        for cuser in self.users:
            self.dataView.insert("", END, text=str(cuser.index), values=(cuser.name, cuser.availableStr(), cuser.permitsStr()))
       

    def generateUI(self):        
        #Título de la ventana
        self.window.title('Usuarios')

        #Tamaño de la ventana
        self.window.geometry("960x540")

        #Mantiene la ventana fija para evitar que el diseño se vea afectado
        self.window.resizable(False, False)
        
        #estilos para crear titulos
        TitleStyles = tkFont.Font(family="Lucida Grande", size=18)

        #Campo para el TextBox Busqueda
        self.searchValue = StringVar()
        Label(self.window, text='Buscar').place(x=20,y=25)
        Entry(self.window, textvariable=self.searchValue).place(x=70, y=25, width=200)

        #------ Seccion del DataView ------- 
        Button(self.window, text = 'Editar', command = self.edit).place(x=20, y=80, width=150)  
        Button(self.window, text = 'Cambiar Estado', command = self.changeState).place(x=190, y=80, width=150)  
        Button(self.window, text = 'Cambiar Permisos', command = self.changePrivileges).place(x=360, y=80, width=150)  
        
        self.dataView = ttk.Treeview(self.window, columns=("#1","#2","#3"))
        self.dataView.pack()
        self.dataView.heading("#0", text="Indice")
        self.dataView.heading("#1", text="Nombre")
        self.dataView.heading("#2", text="Estado")
        self.dataView.heading("#3", text="Permisos")
        self.dataView.place(x=20, y=120)
        self.dataView.column("#0", width=50)
        self.dataView.column("#2", width=100)
        self.dataView.column("#3", width=150)

        #------ Panel de Creacion de Usuario ------- 

        #Muestra el titulo de la seccion
        Label(self.window, text='Crear un nuevo usuario', font=TitleStyles).place(x=650,y=30)

        Label(self.window, text='Nombre').place(x=650,y=70)
        self.createName = StringVar()
        self.createNameTextBox = Entry(self.window, textvariable=self.createName)
        self.createNameTextBox.place(x=720, y=70, width=200)

        #Campo para el TextBox Contraseña
        Label(self.window, text='Contraseña').place(x=650,y=100)
        self.createPassword = StringVar()
        self.createPasswordTextBox = Entry(self.window, textvariable=self.createPassword)
        self.createPasswordTextBox.place(x=720, y=100, width=200)
        
        #Campo Checkbox para el campo administrador
        self.checkvalue = IntVar()
        self.check = Checkbutton(self.window, text="Permisos de permitsistrador", variable=self.checkvalue)
        self.check.place(x=720, y=130)
        
        # button 1 
        Button(self.window, text = 'Crear Usuario', command = self.newUser).place(x=720, y=160, width=130)     
        
        #Compo para el TextBox Nombre
        Label(self.window, text='Editar campos de usuario', font=TitleStyles).place(x=650,y=250)


        #Compo para el TextBox Nombre
        Label(self.window, text='Nombre').place(x=650,y=300)
        self.editName = StringVar()
        self.editNameTextBox = Entry(self.window, textvariable=self.editName)
        self.editNameTextBox.place(x=720, y=300, width=200)

        #Campo para el TextBox Contraseña
        Label(self.window, text='Contraseña').place(x=650,y=330)
        self.editPassword = StringVar()
        self.editPasswordTextBox = Entry(self.window, textvariable=self.editPassword)
        self.editPasswordTextBox.place(x=720, y=330, width=200)
        
        # button 1 
        Button(self.window, text = 'Guardar Cambios', command = self.saveChanges).place(x=720, y=350, width=130)     

    def changeState(self):
        index = int(self.dataView.item(self.dataView.selection())['text']) -1
        if self.users[index].available:
            self.users[index].available = False
        else:
            self.users[index].available = True

        self.refressDataView()

    def changePrivileges(self):
        index = int(self.dataView.item(self.dataView.selection())['text']) -1
        if self.users[index].permits:
            self.users[index].permits = False
        else:
            self.users[index].permits = True
        
        self.refressDataView()
        
    def refressDataView(self):
        self.dataView.delete(*self.dataView.get_children())
        for item in self.users:
            self.dataView.insert("",END, text=str(item.index), values=(item.name,item.availableStr(), item.permitsStr()))
    
    # metodo que muestro los campos para crear un nuevo usuario
    def newUser(self):
        #Obtener el valor de las variables de TKinter
        userName = self.createName.get()
        password = self.createPassword.get()

        if len(userName) > 3 and len(password) > 3:        
            self.users.append(user(len(self.users) + 1,userName,password, self.checkvalue, True))
            
            self.createNameTextBox.delete(0, 'end')
            self.createPasswordTextBox.delete(0, 'end')

            self.refressDataView()
            messagebox.showinfo("Exito","Nuevo Usuario creado")
        else: 
            messagebox.showinfo("Error","El usuario debe tener un nombre y contraseña mayor a 3 caracteres")

    def edit(self):
        # Note here that Tkinter passes an event object to onselect()
        index = self.dataView.item(self.dataView.selection())['text']
        self.selected = self.users[int(index) - 1]

        if self.selected.available is False:
            messagebox.showinfo("Alerta","El Usuario inactivo se activara para poder editar sus cammpos")
            self.users[int(index) - 1].available = True
            self.refressDataView()

        self.editNameTextBox.delete(0, 'end')
        self.editNameTextBox.insert(0,self.selected.name)
        self.editPasswordTextBox.delete(0, 'end')
        self.editPasswordTextBox.insert(0,self.selected.password)

    def saveChanges(self):

        if self.selected is None:
            messagebox.showinfo("Error","No hay usuario seleccionado")
        else:
            self.users[self.selected.index - 1].name = self.editName.get()
            self.users[self.selected.index - 1].password = self.editPassword.get()
            self.selected = None            
            self.refressDataView()
            messagebox.showinfo("Exito","La informacion se actualizo correctamente")
            self.editNameTextBox.delete(0, 'end')
            self.editPasswordTextBox.delete(0, 'end')



    """
        run: Ejecuta la venta de permitsistracion de usuarios
    """
    def run(self):
        self.window.mainloop()