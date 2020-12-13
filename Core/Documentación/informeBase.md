# Índice







[**1. Diseño de la base de datos**](#-1.-Diseño-de-la-base-de-datos.)
[**2. Implementacion grafica con Tkinter**](#-2.-Procedimientos-almacenados.)
[**3. Implementacion grafica con Tkinter**](#-2-Implementacion-grafica-con-Tkinter.)

<br>

# 1. Diseño de la base de datos.
![](http://drive.google.com/uc?export=view&id=1WH4bsoH-H4DISCJUIn2AE_WjpWiJCWbV)
Al momento del diseño de la base de datos se implemento un diseño que fuera orientado a las necesidades que se tenian que cumplir, con los siguientes factores:
- Cumplimiento de las reglas de integridad.
- Poder realizar consultas de información eficientes.
- Eliminar la redundancia de datos.
- Aplicación de las normas de normalización para bases de datos.
- Aplicacion de **TRIGGERS** y **procesos almacenados** para aumentar la eficiencia de la base de datos.

## Descripción de las tablas empleadas.

| Tabla                   | Descripción                                                                                                    |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| --User                    |  En esta tabla esta contenida la información  del usuario, atributos básicos  como ser su nombre **(var_userName)**, contraseña **(var_password)**, un campo para determinar si es administrador **(bit_admin)** y un state **(enu_state)** para poder identificar si el usuario esta activo o inactivo. Esta tabla cuenta con un constraint relacionado al campo **var_userName** con el objetivo de lograr que cada usuario tenga un nombre unico.                                          |
| --Draw   | En esta tabla se almacena la data de las imágenes  **(jso_data)** junto con su nombre  **(var_name)**, al igual que la tabla User, esta cuenta con un constraint para el campo name, evitando así  que se repita el mismo nombre n veces para la misma imagen.                            |
| --Library | Para poder vincular varias imágenes a un mismo usuario (en una relación  de uno a muchos), es necesario crear una tabla que contenta el id de usuario **(int_id_user)**, el id de la imagen **(int_id_draw)**. De esta manera se cumple la necesidad de poder realizar consultas a la base de datos donde solo se indique el id de usuario y esta retorne las imagenes pertenecientes a el. La tabla cuenta con tres constraint, dos cumplen la tarea de las reglas de integridad de la base, definiendo llaves foráneas y el tercero se encarga de que el id de ma imagen no se pueda repetir en esta tabla, Ya que si se pudiera repetir, existe el caso en donde se le asigne la misma imagen a n usuarios diferentes.|
|--canvas_config| En esta tabla se guarda la configuración inicial del canvas donde se crean las imagenes, su ibjetivo es inicializar el **var_pen_color** y el **var_fill_color**.                    |
| --Binnacle                    | Aqui se almacenará la información de la bitácora. Esta bitacora registra cuando el usuario inicie sesion, cree una imagen, cargue una imagen, cuando el administrador efectue un cambio o ajustes a otros usuarios etc. Para ello tendremos un id de usuario **(int_id_user_binn)**, un campo que defina la acción echa por el usuario **(action)**. A cada registro se le asignara la fecha actual de esa insercion **(create)**.                                                             | 
Tabla 1.1
# 2. Procedimientos almacenados.
La implementacion de los procedimientos almacenados en nuestro proyectos ocurre en varios puntos de interes. 
En la ventana de login se cuenta con la primera implementacion, se aplica un SELECT para poder verificar los datos que se acaban de ingresar acompañado con la limitador WHERE.
```python
result = SQLEngine.callProcedure("userLog",userName,password,answer)
```
En el siguiente bloque de codigo se hace el llamado a al procedimiento almacenado llamado **callProcedure**, este proceso resive un userName, password y un valor de respuesta. 

# 3. Implementacion grafica con Tkinter.
Para implementar el entorno visual utilizamos un binding de la biblioteca grafica de **TcI/Tk** para lenguajes de programacion **Python**, denominado **Tkinter**.
Esta herramienta se encarga de renderizar toda la parte visual de nuestro programa, dividiendo asi en vistas principales las cuales diseñar:
- ventana de inicio de sesion.  
- Canvas para la administracion de los dibujos.
- Ventana para gestionar los usuarios (la cual solo el administrador puede acceder).
![](http://drive.google.com/uc?export=view&id=1H0tEvgmJQbOxbd0ZIwGOjyR7CVvw67YT)

#### Ejemplo de sintaxis para crear vistas.
La primera funcion es crear los import necesarios para la utilizacion de Tkinter. 

```python
    from tkinter import *
    from tkinter import messagebox 
```
El diseño de las vistas se define en el constructor, es aqui donde se formulan los atributos como **tamaño**, **orientacion**, **padding** y otros parametros de ajustes visuales.
```python
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
```
La funcion centerWindow(), es una funcion definida para poder centrar el contenido en pantalla, no esta definida entre las herramientas de Tkinter, fue definida.
```python
    def centerWindow(self):

        xCoordinate = int(self.app.winfo_screenwidth()/2 - self.appWidth/2)
        yCoordinate = int(self.app.winfo_screenheight()/2 - self.appHeight/2)

        self.app.geometry('%sx%s+%s+%s' % (self.appWidth,self.appHeight,xCoordinate,yCoordinate))

```

#### Validaciones mediante las vistas.
La primer validacion se realiza al momento de ejecutar el programa en la ventana de login, aqui el usuario ingresa su nombre y password y se ejecuta una peticion que compara los datos ingresados con los datos almacenados en la base de datos.

```python
#Si se encuentra un usuario se procede a verificar que la contraseña sea la misma
        if result:
            if result[0][2] == password and result[0][4] == "active":
                self.app.destroy()
                print("Login Executed Successfully.")

                #Se Ejecuta el llamado a la aplicación de Dibujo
                root = tkinter.Tk()  
                drawingApp = DrawingApplication(root,result[0][3],result[0][0])
                drawingApp.run()
            else:
                messagebox.showerror('Error', 'Nombre de Usuario o contraseña no válidas')
        else:
            messagebox.showerror('Error', 'El Usuario no Existe')
```