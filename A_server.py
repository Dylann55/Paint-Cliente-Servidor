from tkinter import  *
import tkinter as tk
from tkinter import  Canvas, Tk, Frame, Button,messagebox, filedialog, Scale, HORIZONTAL,ALL,colorchooser
import PIL.ImageGrab as ImageGrab
import socket
import threading
import pickle
import json
import sys
import ctypes 
import time 


class Mensaje:
    def __init__(self):
        self.px=0
        self.py=0
        self.color_pincel="black"
        self.pintando=False
        self.width=0.0
        self.canvas = False
        self.fondo = "white"
        self.limpiando=False

historialCambios=[]


class servidor(threading.Thread):
    def __init__(self,direccion_ip,puerto):
        threading.Thread.__init__(self)
        self.direccion_ip = direccion_ip
        self.puerto = puerto
        self.clientes_sockets=[]
        self.socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)





    def run(self):
        def handle_client(conn,addr,sockets):
            print(f"[NEW CONNECTION]{addr} connected.")
            def broadcast(data):
                for socket in sockets:
                    if socket is not conn:
                        socket.send(data)
            def actualizarHistorial(mensaje):
                if mensaje.limpiando==True:
                    historialCambios.clear()
                if mensaje.pintando==True or mensaje.canvas==True:
                    historialCambios.append(mensaje)
            def compartirHistorial():
                data_string = pickle.dumps(historialCambios)
                conn.send(data_string)        
            compartirHistorial()
            while True:
                try:
                    data = conn.recv(900000)
                    mensaje = pickle.loads(data)
                    #print(f"[{conn,addr}] enviando")
                    
                    actualizarHistorial(mensaje)
                    broadcast(data)
                except:
                    break
            self.clientes_sockets.remove(conn)
            conn.close()

        def actualizarListados(conexion_socket):
            self.clientes_sockets.append(conexion_socket)
            
        self.socket_server.bind((self.direccion_ip,self.puerto))
        self.socket_server.listen(10)
        while True:            
            conexion_socket, direccion = self.socket_server.accept()
            hilo = threading.Thread(target=handle_client, args=(conexion_socket,direccion,self.clientes_sockets))
            hilo.start()

            print(f"[ACTIVE CONNECTIONS]{threading.activeCount()-1}")

            actualizarListados(conexion_socket)