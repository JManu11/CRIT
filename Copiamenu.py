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
#import   Analisis2


#---------------Conexion con la BD-----------------------------------
try:
    conexion=pymysql.connect(host='localhost',
                             user='root',
                             password='Mendoza1239',
                             db='Proyecto_Teleton'
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


    def ayuda(self):
        self.root.destroy()  # Cierra la ventana principal
        self.registro_instance.main()  # Abre la ventana de registro


  #  def ayuda2(self):
   #     Analisis2.main()    
        
    def abrir_receta(self):
        self.contador_recetas += 1
        receta = tk.Toplevel(self.root)
        receta.title(f"Receta {self.contador_recetas}")
        receta.geometry("600x600")
        receta.configure(bg='white')
        receta.resizable(False, False)
        receta.configure(bg='#A116CF')

        titulo_receta = tk.Label(receta, text="Sistema Infantil Teleton", font=('calisto MT', 16, 'bold'), bg='#A116CF')
        titulo_receta.pack(pady=5)

        frame_izquierdo = tk.Frame(receta, bg='#A116CF')
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame_derecho = tk.Frame(receta, bg='#A116CF')
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        campos = ['Nombre del paciente: ', 'Expediente: ', 'Edad: ', 'Peso(kg): ', 'Diagnóstico: ',
                'Fecha de nacimiento: ', 'Domicilio: ', 'Nombre del doctor: ',
                'Cédula profesional: ', 'Especialidad: ', 'Egresado de: ']
        self.entradas = {campo: tk.Entry(frame_izquierdo) for campo in campos}
        for campo, entrada in self.entradas.items():
            tk.Label(frame_izquierdo, text=campo, bg='#A116CF').pack()
            entrada.pack()

        self.especificaciones_text = Text(frame_derecho, height=20, width=50)
        self.especificaciones_text.pack()

        self.area_var = tk.IntVar()
        areas = {
            1: 'AREA 1',
            2: 'AREA 2',
            3: 'AREA 3',
            4: 'AREA 4'
        }
        for valor, area in areas.items():
            Radiobutton(frame_derecho, text=area, variable=self.area_var, value=valor,bg='#A116CF').pack()

        boton_qr = Button(frame_derecho, text="Generar Código QR",bg='yellow',
                        command=self.generar_y_mostrar_qr)
        boton_qr.pack()

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?")
        if respuesta:
            print("Cerrando sesión...")
            self.root.destroy()

    def generar_qr(self, data):
        color = {1: 'red', 2: 'blue', 3: 'green', 4: 'orange'}.get(self.area_var.get(), 'black')
        data += f"\nÁrea seleccionada: {self.area_var.get()}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color="white")
        img_nombre = f"receta_qr{self.contador_recetas}.png"
        img.save(img_nombre)
        ventana_qr = tk.Toplevel(self.root)
        ventana_qr.title("QR Code")
        qr_image = ImageTk.PhotoImage(img)
        qr_label = tk.Label(ventana_qr, image=qr_image)
        qr_label.image = qr_image
        qr_label.pack()
        boton_imprimir = Button(ventana_qr, text="Imprimir", command=lambda: self.imprimir_qr(img, ventana_qr))
        boton_imprimir.pack()

    def imprimir_qr(self, img, ventana_qr):
        img_nombre = f"receta_qr{self.contador_recetas}.png"
        img.save(img_nombre)
        messagebox.showinfo("Imprimir", "La imagen se ha guardado y está lista para imprimir.")
        ventana_qr.destroy()

    def generar_y_mostrar_qr(self):
        self.contador_recetas += 1
        datos_receta = '\\n'.join(f'{campo}: {entrada.get()}' for campo, entrada in self.entradas.items())
        datos_receta += '\\nEspecificaciones:\\n' + self.especificaciones_text.get("1.0", tk.END).strip()
        self.generar_qr(datos_receta)

    def mostrar_info_receta(self, receta_info):
        ventana_info = tk.Toplevel(self.root)
        ventana_info.title("Información de la Receta")
        ventana_info.geometry("400x400")
        ventana_info.configure(bg='#A116CF')
        receta_info_formateada = receta_info.replace('\\n', '\n').encode('ascii', 'ignore').decode('ascii')
        info_text = tk.Text(ventana_info, height=20, width=50)
        info_text.insert(tk.END, receta_info_formateada)
        info_text.pack()

    def abrir_ventana_registro(self):#FUNCIONANDOOOOOOOO CON LA BD-------------------------------------
        def registrar_datos_niño(numeroexpediente,full_name, apellido_paterno, apellido_materno, edad, nombre_tutor, apellido_paterno_tutor, apellido_materno_tutor, numero_contacto, ventana_registro):
            if numeroexpediente==''or full_name == '' or apellido_paterno == '' or apellido_materno == '' or edad == '' or nombre_tutor == '' or apellido_paterno_tutor == '' or apellido_materno_tutor == '' or numero_contacto == '':
                messagebox.showwarning("Información incorrecta", "Por favor, completa todos los campos antes de registrar.")
            else:
                v_idStatus = 1
                with conexion.cursor() as cursor:
                    cursor.callproc("insertar_pacientes", args=(numeroexpediente, full_name, apellido_paterno,apellido_materno,edad, nombre_tutor, apellido_paterno_tutor, apellido_materno_tutor,numero_contacto, v_idStatus))
                conexion.commit()
                
                messagebox.showinfo("Registro Exitoso", "Los datos del niño han sido registrados correctamente.")
                ventana_registro.destroy()

        register_window = tk.Toplevel(self.root)
        register_window.title('Registro de Paciente')
        register_window.geometry('800x800')
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

        tk.Label(register_window, text='Edad:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        edad_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        edad_entry.pack()

        tk.Label(register_window, text='Nombre del Tutor:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        nombre_tutor_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        nombre_tutor_entry.pack()

        tk.Label(register_window, text='Apellido Paterno del Tutor:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        apellido_paterno_tutor_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        apellido_paterno_tutor_entry.pack()

        tk.Label(register_window, text='Apellido Materno del Tutor:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        apellido_materno_tutor_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        apellido_materno_tutor_entry.pack()

        tk.Label(register_window, text='Número de Contacto:', bg='#A116CF', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
        numero_contacto_entry = tk.Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        numero_contacto_entry.pack()

        def on_register_button_click():
            numero_expediente= numero_expediente_entry.get()
            full_name = full_name_entry.get()
            apellido_paterno = apellido_paterno_entry.get()
            apellido_materno = apellido_materno_entry.get()
            edad = edad_entry.get()
            nombre_tutor = nombre_tutor_entry.get()
            apellido_paterno_tutor = apellido_paterno_tutor_entry.get()
            apellido_materno_tutor = apellido_materno_tutor_entry.get()
            numero_contacto = numero_contacto_entry.get()

            if numero_expediente=='' or full_name == '' or apellido_paterno == '' or apellido_materno == '' or edad == '' or nombre_tutor == '' or apellido_paterno_tutor == '' or apellido_materno_tutor == '' or numero_contacto == '':
                messagebox.showwarning("Información incorrecta", "Por favor, completa todos los campos antes de registrar.")
            else:
                registrar_datos_niño(numero_expediente,full_name, apellido_paterno, apellido_materno, edad, nombre_tutor, apellido_paterno_tutor, apellido_materno_tutor, numero_contacto, register_window)
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