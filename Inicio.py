from tkinter import *
import tkinter as tk
from tkinter import  Canvas, Tk, Frame, Button,messagebox, filedialog, Scale, HORIZONTAL,ALL,colorchooser
from A_server import servidor
from B_client import client
import sys


def Iniciar_cliente():
    direccion = direccion_variable.get()
    puerto = puerto_variable.get()
    nick = nick_variable.get()

    if direccion!=''and puerto!=0 and nick!='':
        cliente = client(direccion,puerto,nick)

def Iniciar_server():
    direccion = direccion_variable.get()
    puerto = puerto_variable.get()
    if direccion!=''and puerto!=0:
        servidorP=servidor(direccion_ip=direccion,puerto=puerto)
        servidorP.start()
def Salir():
    sys.exit(0)


fondo='#5690F8'
texto='#FFFFFF'
fuente = ("arial",15,"bold")

root = Tk()
root.state(newstate = "normal")
root.geometry("500x400")
root.resizable(0, 0)
root.config(bg=fondo)
root.title("Inicio")




etiqueta_nombre = tk.Label(root,text="Paint",bg=fondo)
etiqueta_nombre.config(font=('Segoe UI Black',36,'normal'), bg=fondo, foreground=texto)
etiqueta_nombre.place(x=190, y=80)
etiqueta_direccion = tk.Label(root,text="Direccion Ip:",bg=fondo)
etiqueta_direccion.config(font=('Segoe UI Black',10,'normal'), bg=fondo, foreground=texto)
etiqueta_direccion.place(x=100, y=180)

direccion_variable = tk.StringVar()
direccion_variable.set('localhost')
direccion_text = tk.Entry(root, width=36,textvariable=direccion_variable)
direccion_text.place(x=187, y=183)


etiqueta_direccion = tk.Label(root,text="Puerto:",bg=fondo)
etiqueta_direccion.config(font=('Segoe UI Black',10,'normal'), bg=fondo, foreground=texto)
etiqueta_direccion.place(x=100, y=202)
puerto_variable = tk.IntVar()
puerto_variable.set(1234)
puerto_text = tk.Entry(root, width=36,textvariable=puerto_variable)
puerto_text.place(x=187, y=205)


etiqueta_nick = tk.Label(root,text="Nick:",bg=fondo)
etiqueta_nick.config(font=('Segoe UI Black',10,'normal'), bg=fondo, foreground=texto)
etiqueta_nick.place(x=100, y=230)
nick_variable = tk.StringVar()
nick_text = tk.Entry(root, width=36,textvariable=nick_variable)
nick_text.place(x=187, y=230)


abrircliente = Button(root, text="Cliente", font= ("Times New Roman", 12), command=Iniciar_cliente)
abrircliente.place(x=100, y=270, height=50 ,width=150)

abrirserver = Button(root, text="Servidor", font= ("Times New Roman", 12), command=Iniciar_server)
abrirserver.place(x=260, y=270, height=50 ,width=150)


Salir_boton = Button(root, text="Salir", font= ("Times New Roman", 12), command=Salir)
Salir_boton.place(x=100, y=325, height=50 ,width=310)

root.mainloop()