# Breve Explicación de los Archivos

**En este apartado se detalla el funcionamiento de cada uno de los componentes del sistema y como se debe ejecutar el proyecto**

## 1. La Carpeta Core/Scripts

La carpeta Scripts contiene todas las definiciones necesarias para crear la base de datos **ProjectBD1**, sus procedimientos almacenados, sus Triggers e Inserciones, de igual manera la base de datos **ProjectBD1_Backup** y sus procedimientos almacenados.

**Por defecto la base de datos ProjectBD1 contiene un usuario administrador:**

* Nombre de Usuario: **admin**
* Contraseña: **admin**

Los documentos **config.ini** y **backupConfig.ini** contienen los parámetros para establecer la conexión hacia las bases de datos antes descritas los cuales deben ser modificados de acuerdo a la configuración del usuario final.

## 2. La Carpeta Core/Python

Dentro de esta carpeta se encuentran todos los documentos necesarios para ejecutar el programa.

### Login

* login.py
  
        Este archivo contiene las funciones necesarias para ejecutar la ventana de Login de usuario y el proceso de autenticación.

        El usuario debe ingresar un nombre de usuario y contraseña válidos para poder acceder a la aplicación de Dibujo.

    ![](https://drive.google.com/uc?export=view&id=1m3G9BJ3nLUBAsDLQvqxenQw5PTNcedho)


### DrawApplication

* Draw.py

        En esta clase se definen todas las funcionalidades de la aplicación de dibujo junto con su interfaz gráfica.

    ![](https://drive.google.com/uc?export=view&id=1YLBemxk4dHqfhZY8GLt0MkR4RSe-2QOs)

* load.py

        Se definen los componentes para la ventana de selección de archivo a cargar, la cual está restringido por usuario.

* XMLtoJSON.py

        Esta clase provee la funcionalidad de convertir una cadena con formato XML a un objeto JSON.

* JSONtoXML.py

        Esta clase provee la funcionalidad de convertir un objeto JSON a su equivalente en XML.

### UserManager

* mainView.py 

        Dentro de este archivo python se encuentran las clases y funciones para ejecutar la ventana de administración de usuarios. 

    ![](https://drive.google.com/uc?export=view&id=11-qtt1rjEQR_1gO8Wi4ryTk1n05_fVpl)

### Compress

* compress.py

        Dentro de este archivo se encuentra el código que provee la funcionalidad de comprimir cadenas con formato de JSON.

### MySQLEngine.py

Aquí se encuentra el "motor" que provee las funciones de:

* Realizar conexiones a una base de datos con los parámetros especificados en los archivos de config.ini y backupConfig.ini
* Realizar consultas (queries) de selección e inserción hacia la base de datos.
* Realizar llamados a procedimientos almacenados en la base de datos.

# Base de Datos

## **ProjectBD1**

Al momento del diseño de la base de datos se implemento un diseño que fuera orientado a las necesidades que se tenian que cumplir, con los siguientes factores:
- Cumplimiento de las reglas de integridad.
- Poder realizar consultas de información eficientes.
- Eliminar la redundancia de datos.
- Aplicación de las normas de normalización para bases de datos.
- Aplicacion de **TRIGGERS** y **procesos almacenados** para aumentar la eficiencia de la base de datos.

## Descripción de las tablas empleadas.

| Tabla                   | Descripción                                                                                                    |
|---------------------------|----------------------------------------------------------------------------------------------------------------|
| User                    |  En esta tabla esta contenida la información  del usuario, atributos básicos  como ser su nombre **(var_userName)**, contraseña **(var_password)**, un campo para determinar si es administrador **(bit_admin)** y un state **(enu_state)** para poder identificar si el usuario esta activo o inactivo. Esta tabla cuenta con un constraint relacionado al campo **var_userName** con el objetivo de lograr que cada usuario tenga un nombre unico.                                          |
| Draw   | En esta tabla se almacena la data de las imágenes  **(jso_data)** junto con su nombre  **(var_name)**, al igual que la tabla User, esta cuenta con un constraint para el campo name, evitando así  que se repita el mismo nombre n veces para la misma imagen.                            |
| Library | Para poder vincular varias imágenes a un mismo usuario (en una relación  de uno a muchos), es necesario crear una tabla que contenta el id de usuario **(int_id_user)**, el id de la imagen **(int_id_draw)**. De esta manera se cumple la necesidad de poder realizar consultas a la base de datos donde solo se indique el id de usuario y esta retorne las imagenes pertenecientes a el. La tabla cuenta con tres constraint, dos cumplen la tarea de las reglas de integridad de la base, definiendo llaves foráneas y el tercero se encarga de que el id de ma imagen no se pueda repetir en esta tabla, Ya que si se pudiera repetir, existe el caso en donde se le asigne la misma imagen a n usuarios diferentes.|
|canvas_config| En esta tabla se guarda la configuración inicial del canvas donde se crean las imagenes, su ibjetivo es inicializar el **var_pen_color** y el **var_fill_color**.                    |
| Binnacle                    | Aqui se almacenará la información de la bitácora. Esta bitacora registra cuando el usuario inicie sesion, cree una imagen, cargue una imagen, cuando el administrador efectue un cambio o ajustes a otros usuarios etc. Para ello tendremos un id de usuario **(int_id_user_binn)**, un campo que defina la acción echa por el usuario **(action)**. A cada registro se le asignara la fecha actual de esa insercion **(create)**.                           

### Modelado de la Base de Datos

![](https://drive.google.com/uc?export=view&id=1WH4bsoH-H4DISCJUIn2AE_WjpWiJCWbV) 

### Diagramado de la Base de Datos

        Aquí va el diagramado de la base de datos.

## **ProjectBD1_Backup**

Esta base de datos almacena una versión compresa de cada imagen guardada por los usuarios, esta versión se almacena en forma de JSON según las especificaciones del ptoyecto.

### **Modelado de la Base de Datos**

![](https://drive.google.com/uc?export=view&id=1nx7XhrfGj04BmkEftidL8Qs-o-aWetSD)

* **id**: Es la llave primaria de la tabla DrawBackup.
* **jso_draw**: Es el json que contiene la versión equivalente comprimida de cada dibujo de los usuarios. El JSON contiene metadata (Id de Usuario y Nombre de la Imagen) que servirá para identificarla al momento de su descarga a través de un procedimiento almacenado.

### **Diagramado de la Base de Datos**

![](https://drive.google.com/uc?export=view&id=1EQZAps7kxdKCIZyDKOEnDsex2S-fHju5)

---

# Explicación sobre algunas Clases y Funciones

## **Clase MySQLEngine**

La clase MySQLEngine es una ampliación de la vista en clase ya que esta no contenía todas las funciones necesarias para la ejecución de este proyecto.

### **Constructor**

```python
def __init__(self,configFile='config.ini'):
        config = configparser.ConfigParser()

        # Se lee el archivo de configuración config.ini
        config.read('Core/Scripts/%s' % configFile)

        # Se recuperan los valores de configuración desde el objeto config
        self.host = config.get('MariaDB Server','host')
        self.port = config.get('MariaDB Server','port')
        self.user = config.get('MariaDB Server','user')
        self.password = config.get('MariaDB Server','password')
        self.database = config.get('MariaDB Server','database')
```

En el constructor se asignan los valores para establecer la conexión hacia la base de datos, extraidos de los archivos de config.ini y backupConfig.ini.

El constructor posee un flag opcional para decidir el archivo de donde se leeran dichos valores.

Además se hace uso de configparser para parsear los valores en los archivos .ini.

### **Función start**

```python
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
```

La función start establece la conexión hacia la base de datos a través del objeto mysql.connector que recibe como parámetros los valores definidos en el constructor.

En esta función también se define el cursor (self.link) que será utilizado para realizar consultas(queries) posteriormente.

### **Función select**

```python
def select(self,query,fetchOne=False):
        self.link.execute(query,multi=True)
        
        if fetchOne:
            return self.link.fetchone()
        else:
            return self.link.fetchall()
```
La función select permite realizar consultas que no requieren una modificación en la base de datos, recibe como parámetros la query (consulta) en forma de cadena y contiene un flag fetchOne para decidir si ir a buscar todos (fetchall) o ir a buscar un solo (fetchone) registros.

El flag multi en el método execute del cursor permite utilizar el mismo cursor para hacer múltiples consultas.

### **Función insert**

```python
def insert(self,query):
        self.link.execute(query,multi=True)
        self.conector.commit()
        print("Data Inserted Successfully")
        return self.link.lastrowid
```

La función insert, que a pesar de su nombre no solo sirve para insertar datos a una base de datos, sino  también para realizar cualquier consulta que modifique la base de datos.

Luego de haber ejecutado una consulta que modifique la base de datos es necesario realizar un commit (o comprometer) los datos insertados o modificados.

### **Función callProcedure**

```python
def callProcedure(self,name,*args):
        print(args)
        return self.link.callproc(name,args)
```
La función callProcedure como su nombre lo indica realiza el llamado a un procedimiento almacenado en la base de datos. Recibe como parámetros el nombre del procedimiento almacenado y una tupla *args (arguments) que contiene todas las variables o parámetros necesarios por los procedimientos.

Esta función devuelve como resultado una tupla con la misma longitud de elementos que args con los resultados obtenidos por el procedimiento almacenado.

### **Función close**

```python 
def close(self):
        if self.conector.is_connected():
            self.link.close()
            self.conector.close()
            print("Connection Closed")
```
La función close cierra o termina la conexión con la base de datos.

## **Clase compress**

### **Importaciones**
```python
import zlib, json, base64
```
* **zlib**: Esta librería contiene algoritmos de compresión y descompresión.
* **json**: Contiene funciones para trabajar con objetos de tipo json, como por ejemplo json.dumps() la cual convierte un objeto JSON a cadena de texto.
* **base64**: Contiene funciones para convertir bytes que tienen datos binarios o de texto en caracteres ASCII.

### **Constructor**
```python
def __init__(self,fileName,userId):
        self.fileName = fileName
        self.userId = userId
```
En el constructor se definen el nombre del archivo a guardar y el id del usuario los cuales serán guardados como metadata en el JSON para poder identificar los dibujos de cada usuario utilizando un procedimiento almacenado.

### **Función jsonZip**
```python
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
```

La función jsonZip recibe como parámetro un JSON, se crea un nuevo json con las llaves de User, FileName y Draw, en donde se almacenarán los datos correspondientes. Dentro de Draw se covertirá el objeto JSON a cadena, luego se comprimirá la cadena y finalmente se convertirá a base 64.

Este JSON se retorna como una cadena con formato de JSON para ser almacenada en la base de datos de respaldo.

### **Función jsonUnzip**
```python
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
```

La función jsonUnzip se utiliza para descomprimir un JSON comprimido por la función jsonZip, recibe una cadena de Texto con formato de JSON y un flag insist el cual es utilizado para suprimir los errores en tiempo de ejecución (Runtime Error) que puedan ocurrir. 