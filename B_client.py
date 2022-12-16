from tkinter import  *
import tkinter as tk
from tkinter import  Canvas, Tk, Frame, Button,messagebox, filedialog, Scale, HORIZONTAL,ALL,colorchooser
import PIL.ImageGrab as ImageGrab
from PIL import ImageTk, Image
import socket
import threading
import pickle
import json
import sys


class Mensaje:
    def __init__(self,nick):
        self.px=0
        self.py=0
        self.color_pincel="black"
        self.pintando=False
        self.width=0.0
        self.canvas = False
        self.fondo = "white"
        self.limpiando=False
        self.nick=nick
        


class client():
    def __init__(self,direccion,puerto,nick):
        def enviarMensaje():
            data_string = pickle.dumps(self.infoLocal)
            self.socket_cliente.send(data_string) 
            self.infoLocal.pintando = False
            self.infoLocal.limpiando = False
            self.infoLocal.canvas = False
        def PintarHilo(x,y,color_pincel,width):
            self.canvas_colores.create_oval(x-2,y-2,x+2,y+2, fill= color_pincel,outline= color_pincel, width=width)
        def recvMessage():
            while True:
                enviarMensaje()
                try:
                    data=self.socket_cliente.recv(900000)
                    data_variable = pickle.loads(data)
                    if type(data_variable)!=list:
                        self.infoRemoto=data_variable

                        
                        if self.infoRemoto.pintando==True:
                            PintarHilo(self.infoRemoto.px,self.infoRemoto.py,self.infoRemoto.color_pincel,self.infoRemoto.width)
                            self.nick_text.config(text= self.infoRemoto.nick)
                            self.nick_text.place(x=self.infoRemoto.px, y=self.infoRemoto.py+125)
                        if self.infoRemoto.limpiando==True:
                            self.canvas_colores.delete(ALL)
                        if self.infoRemoto.canvas==True:
                            self.canvas_colores.configure(bg=self.infoRemoto.fondo)
                    else:
                        for cambio in data_variable:
                            if cambio.pintando:
                                PintarHilo(cambio.px,cambio.py,cambio.color_pincel,cambio.width)
                            if cambio.limpiando:
                                self.canvas_colores.delete(ALL)
                            if cambio.canvas:
                                self.canvas_colores.configure(bg=cambio.fondo)
                    
                except:
                    break
            self.socket_cliente.close()
            sys.exit()


        self.root=tk.Tk()
        self.root.state("zoomed")
        self.root.title("Paint_1.0")
        #-----------------------------------Variables Iniciales----------------------------------------
        self.fuente = ("arial",15,"bold")
        self.color_borrador = "white"
        self.color_pincel = 'black'
        #-----------------------------------Canvas----------------------------------------
        self.canvas_colores = Canvas(self.root, bg='white',bd=5,relief=GROOVE, width=1335,height=600)
        self.canvas_colores.place(x=10,y=130)
        self.canvas_colores.bind("<B1-Motion>",self.Pintar)

        #-----------------------------------Frame----------------------------------------
        #Paleta de Colores
        self.color_frame = LabelFrame(self.root,text="Color",relief=RIDGE,bg="white",width=500,font=self.fuente)
        self.color_frame.place(x=10,y=10,width=425,height=75)
        #Herramientas
        self.tool_frame = LabelFrame(self.root,text="Herramientas",relief=RIDGE,bg="white",width=500,font=self.fuente)
        self.tool_frame.place(x=435,y=10,width=280,height=75)
        #Tamaño de Pincel
        self.pen_frame = LabelFrame(self.root,text="Tamaño",relief=RIDGE,bg="white",width=500,font=self.fuente)
        self.pen_frame.place(x=715,y=10,width=220,height=75)                

        #-----------------------------------Color----------------------------------------
        self.colors = ["#FF4533","#3377FF","#FFF433","#33F0FF","#71FF33","#FFA833","#F833FF","#FF3399","#000000","#FFFFFF","#AD00FF","#1D92FF"]
      
        #-----------------------------------Botones----------------------------------------
        #Botones de Colores
        self.i=self.j=0
        for color in self.colors:
            Button(self.color_frame,bd=3,bg=color,relief=RIDGE,width=3,command=lambda color = color:self.seleccionar_color(color)).grid(row=self.j,column=self.i,padx=1)
            self.i=self.i+1

        #Botones de Herramientas
        self.bt_guardar = Button(self.tool_frame, text ='Guardar',bd=4, bg='white',relief=RIDGE, command = self.Guardar)
        self.bt_guardar.grid(column=0, row=0,padx=2)

        self.bt_borrar = Button(self.tool_frame, text ='Borrar',bd=4, bg='white',relief=RIDGE, command = self.Borrador)
        self.bt_borrar.grid(column=1, row=0,padx=2)

        self.bt_limpiar = Button(self.tool_frame, text ='Limpiar',bd=4, bg='white',relief=RIDGE, command = self.Limpiar)
        self.bt_limpiar.grid(column=2, row=0,padx=2)

        self.bt_canvas = Button(self.tool_frame, text ='Canvas',bd=4, bg='white',relief=RIDGE, command = self.Canvas_color)
        self.bt_canvas.grid(column=3, row=0,padx=2)

        self.bt_salir = Button(self.tool_frame, text ='Salir',bd=4, bg='white',relief=RIDGE, command = self.Salir)
        self.bt_salir.grid(column=4, row=0,padx=2)

        #Tamaño del Pincel
        self.tam_pincel = Scale(self.pen_frame,orient= HORIZONTAL, from_ = 0, to=50, length=200)
        self.tam_pincel.set(1)
        self.tam_pincel.grid(column=0, row=0, pady=1, padx=2)
        #-----------------------------------Cursor----------------------------------------
        self.nick_text = tk.Label(self.root,text="paint")
        self.nick=""

        #-----------------------------------Init----------------------------------------
        self.socket_cliente=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.infoLocal = Mensaje(nick)
        self.infoLocal.nick=nick
        self.infoRemoto = Mensaje("Remoto")
        self.direccion_ip = direccion
        self.puerto = puerto
        self.socket_cliente.connect((self.direccion_ip,self.puerto))
        recvThread =threading.Thread(target=recvMessage)    
        recvThread.daemon=True
        recvThread.start() 

        self.root.mainloop()


    def Pintar(self,event):
        x1,y1 = (event.x-2),(event.y-2)
        x2,y2 = (event.x+2),(event.y+2)

        self.infoLocal.px=event.x
        self.infoLocal.py=event.y
        self.infoLocal.color_pincel=self.color_pincel
        self.infoLocal.pintando=True
        self.infoLocal.width=self.tam_pincel.get()

        self.canvas_colores.create_oval(x1,y1,x2,y2, fill= self.color_pincel,outline= self.color_pincel, width=self.tam_pincel.get())

    def seleccionar_color(self,color):
        self.color_pincel = color

    def Canvas_color(self):
        color = colorchooser.askcolor()
        self.canvas_colores.configure(bg=color[1])
        self.color_borrador = color[1]
    
        self.infoLocal.fondo = color[1]
        self.infoLocal.canvas = True
        self.Borrador()

    def Borrador(self):
        self.color_pincel = self.color_borrador

    def Limpiar(self):
        self.infoLocal.limpiando = True
        self.canvas_colores.delete(ALL)

    def Salir(self):
        self.root.destroy()


    def Guardar(self):
        try: 
            filename = filedialog.asksaveasfilename(defaultextension='.png')

            x = self.winfo_rootx() + self.canvas_colores.winfo_x()
            y = self.winfo_rooty() + self.canvas_colores.winfo_y()

            x1 = x + self.canvas_colores.winfo_width()
            y1 = y + self.canvas_colores.winfo_height()

            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
            messagebox.showinfo('Guardar Dibujo','Imagen guardada en: ' + str(filename) )
        except:
            messagebox.showerror('Guardar Dibujo', 'Imagen no guardada\n Error')
