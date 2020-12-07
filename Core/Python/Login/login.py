# -*- coding:utf-8 -*-

"""
    @author: Alexis
    @date: 27/11/2020
    @version 1.0
"""

from tkinter import *
from tkinter import messagebox 
from Core.Python.DrawApplication.Draw import *
from Core.Python.MySQLEngine import *

"""
    loginGUI: Objeto para crear una ventana de Login
"""
class loginGUI:

    """
        Constructor para el objeto loginGUI
    """
    def __init__(self):
        self.app = Tk()

        #Título de la ventana
        self.app.title('Autenticación')

        #Tamaño de la ventana
        self.appWidth = 400
        self.appHeight = 250

        #Centrar ventana
        self.centerWindow()

        #Contenido
        self.label = Label(self.app, text='Bienvenido a Paint Pirata',font = 'Helvetica 16 bold')
        self.label.pack(pady=30)

        # Variables de Tkinter
        self.TUsernamme = StringVar()
        self.TPassword = StringVar()

        #Campo para el userName
        self.usernameLabel = Label(self.app, text='Nombre de Usuario')
        self.usernameLabel.place(x=30,y=80)

        self.TUsernamme = Entry(self.app, relief=FLAT, textvariable=self.TUsernamme)
        self.TUsernamme.place(x=170, y=80, width=190)

        #Campo para la contraseña
        self.passwordLabel = Label(self.app, text='Contraseña')
        self.passwordLabel.place(x=30,y=120)

        self.TPassword = Entry(self.app, show='*', relief=FLAT, textvariable=self.TPassword)
        self.TPassword.place(x=170, y=120, width=190)

        #Botón de Login
        self.login = Button(self.app, text='Login',pady=5, padx=30, command=self.login)
        self.login.place(x=150, y=170, width=100)

    """
        centerWindow: Centra la ventana en la pantalla
    """    
    def centerWindow(self):

        xCoordinate = int(self.app.winfo_screenwidth()/2 - self.appWidth/2)
        yCoordinate = int(self.app.winfo_screenheight()/2 - self.appHeight/2)

        self.app.geometry('%sx%s+%s+%s' % (self.appWidth,self.appHeight,xCoordinate,yCoordinate))

    """
        login: Obtiene los valores de usuario y contraseña para su posterior uso
    """
    #Nota: Aqui se hace el llamado al objeto que se conecta a la base de datos y verifica si el usuario existe
    def login(self):

        #Obtener el valor de las variables de TKinter
        userName = self.TUsernamme.get()
        password = self.TPassword.get()
        
        SQLEngine = MySQLEngine()
        SQLEngine.start()

        #Consulta SQL para buscar al usuario 
        result = SQLEngine.select("SELECT User.id,User.var_userName, User.var_password,User.bit_admin,User.enu_state FROM User WHERE User.var_userName LIKE '%s';" % userName)

        #Se cierra la conexión con la base de datos
        SQLEngine.close()

        #Si se encuentra un usuario se procede a verificar que la contraseña sea la misma
        if result:
            if result[0][2] == password and result[0][4] == "active":
                self.app.destroy()
                print("Login Executed Successfully.")

                #Se Ejecuta el llamado a la aplicación de Dibujo
                root = tkinter.Tk()  
                drawingApp = DrawingApplication(root,result[0][3])
                drawingApp.run()
            else:
                messagebox.showerror('Error', 'Nombre de Usuario o contraseña no válidas')
        else:
            messagebox.showerror('Error', 'El Usuario no Existe')

    """
        run: Ejecuta la venta de Login
    """
    def run(self):
        self.app.mainloop()