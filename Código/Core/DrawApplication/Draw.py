# The imports include turtle graphics and tkinter modules. 
# The colorchooser and filedialog modules let the user
# pick a color and a filename.
import turtle
import tkinter
import tkinter.colorchooser
import tkinter.filedialog
import xml.dom.minidom
from Core.DrawApplication.XMLtoJSON import *
from Core.DrawApplication.JSONtoXML import *
from ..MySQLEngine import *
from ..UserManager.mainView import *
from ..Compress.compress import *
from Core.DrawApplication.load import *
from tkinter.simpledialog import askstring

# The following classes define the different commands that 
# are supported by the drawing application. 
class GoToCommand:
    def __init__(self,x,y,width=1,color="black"):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
        
    # The draw method for each command draws the command
    # using the given turtle
    def draw(self,turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x,self.y)
        
    # The __str__ method is a special method that is called
    # when a command is converted to a string. The string
    # version of the command is how it appears in the graphics
    # file format. 
    def __str__(self):
        return '<Command x=\"' + str(self.x) + '\" y=\"' + str(self.y) + \
               '\" width=\"' + str(self.width) \
               + '\" color=\"' + self.color + '\">GoTo</Command>' 
        
class CircleCommand:
    def __init__(self,radius, width=1,color="black"):
        self.radius = radius
        self.width = width
        self.color = color
        
    def draw(self,turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)
        
    def __str__(self):
        return '<Command radius=\"' + str(self.radius) + '\" width=\"' + \
               str(self.width) + '\" color=\"' + self.color + '\">Circle</Command>'
        
class BeginFillCommand:
    def __init__(self,color):
        self.color = color
        
    def draw(self,turtle):
        turtle.fillcolor(self.color)
        turtle.begin_fill()
        
    def __str__(self):
        return '<Command color=\"' + self.color + '\">BeginFill</Command>'
        
class EndFillCommand:
    def __init__(self):
        pass
    
    def draw(self,turtle):
        turtle.end_fill()
        
    def __str__(self):
        return "<Command>EndFill</Command>"
        
class PenUpCommand:
    def __init__(self):
        pass
    
    def draw(self,turtle):
        turtle.penup()
        
    def __str__(self):
        return "<Command>PenUp</Command>"
        
class PenDownCommand:
    def __init__(self):
        pass
    
    def draw(self,turtle):
        turtle.pendown()
        
    def __str__(self):
        return "<Command>PenDown</Command>"

# This is the container class for a graphics sequence. It is meant
# to hold the graphics commands sequence. 
class GraphicsSequence: #La secuencia de acciones (al dibujar) realizadas por el usuario se almacena en este arreglo gcList
    def __init__(self):
        self.gcList = []
        
    # The append method is used to add commands to the sequence.
    def append(self,item):
        self.gcList = self.gcList + [item]
        
    # This method is used by the undo function. It slices the sequence
    # to remove the last item
    def removeLast(self):
        self.gcList = self.gcList[:-1]
       
    # This special method is called when iterating over the sequence.
    # Each time yield is called another element of the sequence is returned
    # to the iterator (i.e. the for loop that called this.)
    def __iter__(self):
        for c in self.gcList:
            yield c
    
    # This is called when the len function is called on the sequence.        
    def __len__(self):
        return len(self.gcList)
        
    # The write method writes an XML file to the given filename

    #Aqui se escribe el dibujo en xml, pero en vez de eso se convertira a JSON y se enviará a la base de datos
    def write(self,filename,userId):
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n<GraphicsCommands>\n"

        for cmd in self:
            xml += '    '+str(cmd)+"\n"
        xml += '</GraphicsCommands>\n'
 
        converter = XMLtoJSON()
        json = converter.process(xml)
        print(json)

        #Objeto json Comprimido
        compressor = jsonCompress(filename,userId)
        jsonCompressed = compressor.jsonZip(json)

        #Queries
        SQLEngine = MySQLEngine()
        SQLEngine.start()

        #Se guarda el dibujo, y se obtiene el id del registro agregado
        drawId = 0
        result = SQLEngine.callProcedure("newDraw", userId, filename, json, drawId)
        drawId = result[-1]
        #Se inserta la referencia en la Libreria del Usuario
        SQLEngine.insert("INSERT INTO Library(int_id_user,int_id_draw) VALUES (%s,%s);" % (userId,drawId))
        SQLEngine.close()

        #Backup Query
        SQLEngine = MySQLEngine(configFile="backupConfig.ini")
        SQLEngine.start()

        SQLEngine.insert("INSERT INTO DrawBackup(jso_compressedDraw) VALUES ('%s');" % (jsonCompressed))

        SQLEngine.close()


    # The parse method adds the contents of an XML file to this sequence
    def parse(self,data):
        convert = JSONtoXML()
        xmlString = convert.createXML(data)
        
        xmldoc = xml.dom.minidom.parseString(xmlString)
        
        graphicsCommandsElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]
        
        graphicsCommands = graphicsCommandsElement.getElementsByTagName("Command")
        
        for commandElement in graphicsCommands:
            print(type(commandElement))
            command = commandElement.firstChild.data.strip()
            attr = commandElement.attributes
            if command == "GoTo":
                x = float(attr["x"].value)
                y = float(attr["y"].value)
                width = float(attr["width"].value)
                color = attr["color"].value.strip()
                cmd = GoToCommand(x,y,width,color)
    
            elif command == "Circle":
                radius = float(attr["radius"].value)
                width = int(attr["width"].value)
                color = attr["color"].value.strip()
                cmd = CircleCommand(radius,width,color)
    
            elif command == "BeginFill":
                color = attr["color"].value.strip()
                cmd = BeginFillCommand(color)
    
            elif command == "EndFill":
                cmd = EndFillCommand()
                
            elif command == "PenUp":
                cmd = PenUpCommand()
                
            elif command == "PenDown":
                cmd = PenDownCommand()
            else:
                raise RuntimeError("Unknown Command: " + command) 
    
            self.append(cmd)
            
        
# This class defines the drawing application. The following line says that
# the DrawingApplication class inherits from the Frame class. This means
class DrawingApplication(tkinter.Frame):

    def __init__(self, master=None, userType=0,userId=None):
        super().__init__(master)
        self.userType = userType
        self.userId = userId
        self.loadedImageName = None
        self.pack()
        self.buildWindow()    
        self.graphicsCommands = GraphicsSequence()
        
    # This method is called to create all the widgets, place them in the GUI,
    # and define the event handlers for the application.
    def buildWindow(self):
        
        # The master is the root window. The title is set as below. 
        self.master.title("Draw")
        
        # Here is how to create a menu bar. The tearoff=0 means that menus
        # can't be separated from the window which is a feature of tkinter.
        bar = tkinter.Menu(self.master)
        fileMenu = tkinter.Menu(bar,tearoff=0)
        
        # This code is called by the "New" menu item below when it is selected.
        # The same applies for loadFile, addToFile, and saveFile below. The 
        # "Exit" menu item below calls quit on the "master" or root window. 
        def newWindow():
            # This sets up the turtle to be ready for a new picture to be 
            # drawn. It also sets the sequence back to empty. It is necessary
            # for the graphicsCommands sequence to be in the object (i.e. 
            # self.graphicsCommands) because otherwise the statement:
            # graphicsCommands = GraphicsSequence()
            # would make this variable a local variable in the newWindow 
            # method. If it were local, it would not be set anymore once the
            # newWindow method returned.
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()  
            screen.update()
            screen.listen()
            self.graphicsCommands = GraphicsSequence()
            
        fileMenu.add_command(label="New",command=newWindow)
            
        def loadFile():
            
            newWindow()
            
            load = loadGUI(self.userId)
            load.run()

            # This re-initializes the sequence for the new picture. 
            # calling parse will read the graphics commands from the file.
            self.graphicsCommands = GraphicsSequence()

            #Aqui se debe realizar el query para obtener el json y luego mandarlo al parser
            self.graphicsCommands.parse(load.data)
            self.loadedImageName = load.fileName
               
            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
                
            # This line is necessary to update the window after the picture is drawn.
            screen.update()
            
            
        fileMenu.add_command(label="Load...",command=loadFile)
        
        def addToFile():
            filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")
            
            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()
            theTurtle.pencolor("#000000")
            theTurtle.fillcolor("#000000")
            cmd = PenUpCommand()
            self.graphicsCommands.append(cmd)
            cmd = GoToCommand(0,0,1,"#000000")
            self.graphicsCommands.append(cmd)
            cmd = PenDownCommand()
            self.graphicsCommands.append(cmd)
            screen.update()
            self.graphicsCommands.parse(filename)
               
            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)
                
            screen.update() 

        def adminUsers():
            self.master.withdraw()
            adminUserGUI = userManagerGUI(draw=self.master)
            adminUserGUI.run()

        # Aqui se de debe ingresar la función que hará el llamado a la ventana de administración de Usuarios
        fileMenu.add_command(label="Configure",command=adminUsers)

        # Si el usuario no es Administrador entonces se deshabilita el menu de configuración
        if self.userType == 0:
            fileMenu.entryconfig(2,state="disabled")
        
        def saveFile():
            filename = simpledialog.askstring(title = "Save As...",prompt = "Guardar archivo como: ")
            self.graphicsCommands.write(filename,self.userId)
            
        fileMenu.add_command(label="Save As...",command=saveFile)
        
        def download():
            # Obtener la ruta en la que se desea descargar el archivo
            savePath = tkinter.filedialog.asksaveasfilename(initialfile=self.loadedImageName,title="Descargar Archivo en: ")
            savePath = "%s.json" % savePath

            # Se inicia el motor SQL para llamar al procedimiento almacenado que devolvera el archivo
            # comprimido en la base de datos de respaldo
            SQLEngine = MySQLEngine("backupConfig.ini")
            SQLEngine.start()
            result = ""
            answer = SQLEngine.callProcedure("sp_download",self.userId,self.loadedImageName,result)
            SQLEngine.close()

            # Se escribe el contenido en la ruta seleccionada
            f = open(savePath, "w")
            f.write("%s" % answer[2])
            f.close()

        #Aquí se debe aregregar el comando para descargar el dibujo desde la base de datos de Backup.
        fileMenu.add_command(label="Download",command=download)

        fileMenu.add_command(label="Exit",command=self.master.quit)
        
        bar.add_cascade(label="File",menu=fileMenu)
        
        # This tells the root window to display the newly created menu bar.
        self.master.config(menu=bar)    
        
        # Here several widgets are created. The canvas is the drawing area on 
        # the left side of the window. 
        canvas = tkinter.Canvas(self,width=600,height=600)
        canvas.pack(side=tkinter.LEFT)
        
        # By creating a RawTurtle, we can have the turtle draw on this canvas. 
        # Otherwise, a RawTurtle and a Turtle are exactly the same.
        theTurtle = turtle.RawTurtle(canvas)
        
        # This makes the shape of the turtle a circle. 
        theTurtle.shape("circle")
        screen = theTurtle.getscreen()
        
        # This causes the application to not update the screen unless 
        # screen.update() is called. This is necessary for the ondrag event
        # handler below. Without it, the program bombs after dragging the 
        # turtle around for a while.
        screen.tracer(0)
    
        # This is the area on the right side of the window where all the 
        # buttons, labels, and entry boxes are located. The pad creates some empty 
        # space around the side. The side puts the sideBar on the right side of the 
        # this frame. The fill tells it to fill in all space available on the right
        # side. 
        sideBar = tkinter.Frame(self,padx=5,pady=5)
        sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
        
        # This is a label widget. Packing it puts it at the top of the sidebar.
        pointLabel = tkinter.Label(sideBar,text="Width")
        pointLabel.pack()
        
        # This entry widget allows the user to pick a width for their lines. 
        # With the widthSize variable below you can write widthSize.get() to get
        # the contents of the entry widget and widthSize.set(val) to set the value
        # of the entry widget to val. Initially the widthSize is set to 1. str(1) is 
        # needed because the entry widget must be given a string. 
        widthSize = tkinter.StringVar()
        widthEntry = tkinter.Entry(sideBar,textvariable=widthSize)
        widthEntry.pack()
        widthSize.set(str(1))
        
        radiusLabel = tkinter.Label(sideBar,text="Radius")
        radiusLabel.pack()
        radiusSize = tkinter.StringVar()
        radiusEntry = tkinter.Entry(sideBar,textvariable=radiusSize)
        radiusSize.set(str(10))
        radiusEntry.pack()
        
        # A button widget calls an event handler when it is pressed. The circleHandler
        # function below is the event handler when the Draw Circle button is pressed. 
        def circleHandler():
            # When drawing, a command is created and then the command is drawn by calling
            # the draw method. Adding the command to the graphicsCommands sequence means the
            # application will remember the picture. 
            cmd = CircleCommand(int(radiusSize.get()), int(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            
            # These two lines are needed to update the screen and to put the focus back
            # in the drawing canvas. This is necessary because when pressing "u" to undo,
            # the screen must have focus to receive the key press. 
            screen.update()
            screen.listen()
        
        # This creates the button widget in the sideBar. The fill=tkinter.BOTH causes the button
        # to expand to fill the entire width of the sideBar.
        circleButton = tkinter.Button(sideBar, text = "Draw Circle", command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)             

        # The color mode 255 below allows colors to be specified in RGB form (i.e. Red/
        # Green/Blue). The mode allows the Red value to be set by a two digit hexadecimal
        # number ranging from 00-FF. The same applies for Blue and Green values. The 
        # color choosers below return a string representing the selected color and a slice
        # is taken to extract the #RRGGBB hexadecimal string that the color choosers return.
        screen.colormode(255)
        penLabel = tkinter.Label(sideBar,text="Pen Color")
        penLabel.pack()
        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sideBar,textvariable=penColor)
        penEntry.pack()
        
        # Obtener el valor por defecto desde la base de datos.
        SQLEngine = MySQLEngine()
        SQLEngine.start()
        pen = ""
        fill = ""
        result = SQLEngine.callProcedure("getCanvasConfig",pen,fill)
        pen = result[0]
        fill = result[1]
        SQLEngine.close()

        penColor.set(pen)  
        
        def getPenColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:
                penColor.set(str(color)[-9:-2])
            
        penColorButton = tkinter.Button(sideBar, text = "Pick Pen Color", command=getPenColor)
        penColorButton.pack(fill=tkinter.BOTH)           
            
        fillLabel = tkinter.Label(sideBar,text="Fill Color")
        fillLabel.pack()
        fillColor = tkinter.StringVar()
        fillEntry = tkinter.Entry(sideBar,textvariable=fillColor)
        fillEntry.pack()
        fillColor.set(fill)     
        
        def getFillColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:    
                fillColor.set(str(color)[-9:-2])       
   
        fillColorButton = \
            tkinter.Button(sideBar, text = "Pick Fill Color", command=getFillColor)
        fillColorButton.pack(fill=tkinter.BOTH) 


        def beginFillHandler():
            cmd = BeginFillCommand(fillColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            
        beginFillButton = tkinter.Button(sideBar, text = "Begin Fill", command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH) 
        
        def endFillHandler():
            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            
        endFillButton = tkinter.Button(sideBar, text = "End Fill", command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH) 
 
        penLabel = tkinter.Label(sideBar,text="Pen Is Down")
        penLabel.pack()
        
        def penUpHandler():
            cmd = PenUpCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Up")
            self.graphicsCommands.append(cmd)

        penUpButton = tkinter.Button(sideBar, text = "Pen Up", command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH) 
       
        def penDownHandler():
            cmd = PenDownCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Down")
            self.graphicsCommands.append(cmd)

        penDownButton = tkinter.Button(sideBar, text = "Pen Down", command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)

        def canvasColorConfig():
            pen = penColor.get()
            fill = fillColor.get()
            SQLEngine = MySQLEngine()
            SQLEngine.start()
            SQLEngine.callProcedure("changeCanvasConfig", self.userId, pen, fill)
            SQLEngine.close()


        # Aqui se de debe ingresar la función que hará el llamado a la ventana de administración de Usuarios
        colorConfig = tkinter.Button(sideBar, text = "Set Default Colors", command=canvasColorConfig)
        colorConfig.pack(fill=tkinter.BOTH)

        # Si el usuario no es Administrador entonces se deshabilita el menu de configuración
        if self.userType == 0:
            colorConfig['state']= tkinter.DISABLED
            #fileMenu.entryconfig(2,state="disabled")          

        # Here is another event handler. This one handles mouse clicks on the screen.
        def clickHandler(x,y): 
            # When a mouse click occurs, get the widthSize entry value and set the width of the 
            # pen to the widthSize value. The int(widthSize.get()) is needed because
            # the width is an integer, but the entry widget stores it as a string.
            cmd = GoToCommand(x,y,int(widthSize.get()),penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)          
            screen.update()
            screen.listen()
           
        # Here is how we tie the clickHandler to mouse clicks.
        screen.onclick(clickHandler)  
        
        def dragHandler(x,y):
            cmd = GoToCommand(x,y,int(widthSize.get()),penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)  
            screen.update()
            screen.listen()
            
        theTurtle.ondrag(dragHandler)
        
        # the undoHandler undoes the last command by removing it from the 
        # sequence and then redrawing the entire picture. 
        def undoHandler():
            if len(self.graphicsCommands) > 0:
                self.graphicsCommands.removeLast()
                theTurtle.clear()
                theTurtle.penup()
                theTurtle.goto(0,0)
                theTurtle.pendown()
                for cmd in self.graphicsCommands:
                    cmd.draw(theTurtle)
                screen.update()
                screen.listen()
                
        screen.onkeypress(undoHandler, "u")
        screen.listen()
   
    # The run function in our GUI program is very simple. It creates the 
    # root window. Then it creates the DrawingApplication frame which creates 
    # all the widgets and has the logic for the event handlers. Calling mainloop
    # on the frames makes it start listening for events. The mainloop function will 
    # return when the application is exited. 
    def run(self):  
        self.master.mainloop()
        print("Drawing App Executed Successfully.")