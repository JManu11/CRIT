import tkinter as tk
from tkinter import messagebox, Text, Radiobutton, Button
from PIL import ImageTk
from tkinter import Toplevel
import qrcode
#Funcionando el registro
#Funcionando el Login pero sin usar procedimiento
from tkinter import *
from tkinter import messagebox
import pymysql
from tkinter import *
from tkinter import Tk, Button, Label, Entry, Frame, Scrollbar, Listbox, END
from PIL import Image, ImageTk
from fpdf import FPDF
import os
from typing import Any, Optional
import tkinter as tk
from tkinter import simpledialog, messagebox, Text, Radiobutton, Button, filedialog
import qrcode
from PIL import Image, ImageTk
import registro_pacientes #Importa el codigo
import tkinter as tk
#import   Analisis2
import Receta2
from Receta2 import receta
import cargainfo


#---------------Conexion con la BD-----------------------------------
try:
    conexion=pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='CRIT'
                            )
    print("Conectado")
except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
    print("Error: ", e)



class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.contador_recetas = 0
        self.registro_instance = registro_pacientes  # Instancia de la clase registro
     #   self.analisis_instance = Analisis2
        self.receta_instance = Receta2


    def ayuda(self):
        self.root.destroy()  # Cierra la ventana principal
        self.registro_instance.main()  # Abre la ventana de registro


  #  def ayuda2(self):
   #     Analisis2.main()    
        
    def abrir_receta(self):
        self.root.destroy()
        receta()

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            print("Cerrando sesión...")
            self.root.destroy()

    

    def abrir_ventana_registro(self):#FUNCIONANDOOOOOOOO CON LA BD-------------------------------------
        def registrar_datos_niño(numeroexpediente,full_name, apellido_paterno, apellido_materno, fecha_nacimiento,  ventana_registro):
            if numeroexpediente==''or full_name == '' or apellido_paterno == '' or apellido_materno == '' or fecha_nacimiento == '':
                messagebox.showwarning("Información incorrecta", "Por favor, completa todos los campos antes de registrar.")
            else:
                v_idStatus = 1
                with conexion.cursor() as cursor:
                    cursor.callproc("insertar_pacientes", args=(numeroexpediente, full_name, apellido_paterno,apellido_materno,fecha_nacimiento, v_idStatus))
                conexion.commit()
                
                messagebox.showinfo("Registro Exitoso", "Los datos del niño han sido registrados correctamente.")
                ventana_registro.destroy()

        register_window = tk.Toplevel(self.root)
        register_window.title('Registro de Paciente')
        register_window.geometry('400x400')
        register_window.configure(bg='#A116CF')
        register_window.resizable(False, False)

        tk.Label(register_window, text='Numero Expediente:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        numero_expediente_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        numero_expediente_entry.pack()

        tk.Label(register_window, text='Nombre Completo:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        full_name_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        full_name_entry.pack()

        tk.Label(register_window, text='Apellido Paterno:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        apellido_paterno_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        apellido_paterno_entry.pack()

        tk.Label(register_window, text='Apellido Materno:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        apellido_materno_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        apellido_materno_entry.pack()

        tk.Label(register_window, text='Fecha de Nacimiento:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        edad_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        edad_entry.pack()

        def on_register_button_click():
            numero_expediente= numero_expediente_entry.get()
            full_name = full_name_entry.get()
            apellido_paterno = apellido_paterno_entry.get()
            apellido_materno = apellido_materno_entry.get()
            fecha_nacimiento = edad_entry.get()


            if numero_expediente=='' or full_name == '' or apellido_paterno == '' or apellido_materno == '' or fecha_nacimiento == '':
                messagebox.showwarning("Información incorrecta", "Por favor, completa todos los campos antes de registrar.")
            else:
                registrar_datos_niño(numero_expediente,full_name, apellido_paterno, apellido_materno, fecha_nacimiento, register_window)
                register_window.destroy()

        btn_registrar = tk.Button(register_window, text="Registrar", command=on_register_button_click,
                                width=20, height=2, bg='yellow', fg='black', font=('Microsoft YaHei UI Light', 12, 'bold'))
        btn_registrar.pack(pady=10)

    def abrir_menu(self):
        self.root.title("Menú Principal")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        titulo = tk.Label(self.root, text="Menú", bg='white', fg='#6a0dad', font=('Microsoft YaHei UI Light', 20, 'bold'))
        titulo.pack(pady=20)

        btn_ayuda = tk.Button(self.root, text="Pacientes", command=self.ayuda,
                            width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12,'bold'))
        btn_ayuda.pack(pady=5)

        btn_receta = tk.Button(self.root, text="Receta", command=self.abrir_receta,
                            width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12,'bold'))
        btn_receta.pack(pady=5)

        btn_registro = tk.Button(self.root, text="Registrar Niño", command=self.abrir_ventana_registro,
                                width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12,'bold'))
        btn_registro.pack(pady=5)
        
        btn_registro = tk.Button(self.root, text="Escanear Receta", command=self.ejecutar_interfaz,
                                width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12,'bold'))
        btn_registro.pack(pady=5)

    #    btn_ayuda2 = tk.Button(self.root, text="Control Financiero", command=self.ayuda2,
     #                           width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12,'bold'))
      #  btn_ayuda2.pack(pady=5)

        btn_cerrar_sesion = tk.Button(self.root, text="Cerrar Sesión", command=self.cerrar_sesion,
                                    width=20, height=2, bg='#6a0dad', fg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        btn_cerrar_sesion.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    menu_principal = MenuPrincipal(root)
    menu_principal.abrir_menu()
    root.mainloop()