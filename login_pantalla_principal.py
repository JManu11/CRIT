import tkinter as tk
from tkinter import messagebox, StringVar
import hashlib
import menu_segunda_pantalla
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



#-----------------------------------------------------


# Función de cierre de sesión
def cerrar_sesion():
    # Limpiar los campos de usuario y contraseña
    user.delete(0, 'end')
    code.delete(0, 'end')

# Función de inicio de sesión
def signin(): #FUNCIONAAAADOOOO CON LA BD
        with conexion.cursor() as cursor:
            # Solicitar al usuario que ingrese el ID de usuario y la contraseña
            usuario = user.get()
            contraseña = code.get()

            #BASEEEEE--------------
            # Consulta SQL para verificar las credenciales del usuario
            consulta = "SELECT * FROM usuario WHERE username = %s AND contraseñaUsuario = %s"
            cursor.execute(consulta, (usuario, contraseña))

            # Obtener el resultado de la consulta
            resultado = cursor.fetchone()
            #-----------------------------

            # Verificar si el usuario y la contraseña son válidos
            if resultado:
                messagebox.showinfo("Ingreso Exitoso", "Bienvenido!")

                # Eliminar elementos de la pantalla de inicio de sesión
                for widget in frame.winfo_children():
                    widget.destroy()

                # Crear instancia de la clase MenuPrincipal y mostrar el menú
                menu_principal = menu_segunda_pantalla.MenuPrincipal(root)
                menu_principal.abrir_menu()

                # Eliminar la imagen y el texto "Trabajo Social"
                img_label.destroy()
                trabajo_social_label.destroy()

            else:
                messagebox.showerror("Error de Ingreso", "Correo electrónico, contraseña o nombre incorrectos.")


# Función para borrar el texto predeterminado en el campo de entrada de usuario
def borrar_texto_usuario(event):
    user.delete(0, 'end')

# Función para borrar el texto predeterminado en el campo de entrada de contraseña
def borrar_texto_contraseña(event):
    code.delete(0, 'end')

# Crear ventana principal
root = tk.Tk()
root.title('Login')
root.geometry('900x500+300+200')
root.configure(bg="#fff")
root.resizable(True, True)

# Imagenes del código...
img = tk.PhotoImage(file='logo_10.png')
img_label = tk.Label(root, image=img, bg='white')
img_label.place(x=50, y=50)
frame = tk.Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

admin_img = tk.PhotoImage(file='capacidad_1.png')
admin_img = admin_img.subsample(2, 2)
tk.Label(frame, image=admin_img, bg='white').place(relx=0.5, rely=0.0004, anchor=tk.N)

heading = tk.Label(frame, text='Administrador', bg='white', font=('Arial', 17, 'bold'), fg='#57a1f8')
heading.place(relx=0.5, rely=0.15, anchor=tk.N)

trabajo_social_label = tk.Label(root, text='Trabajo Social', fg='purple', bg='white', font=('Arial', 25,'bold'))
trabajo_social_label.place(x=50, y=50+img.height()+10)

# Campos de entrada
user_var = StringVar()
code_var = StringVar()

# Campo de entrada de usuario
user = tk.Entry(frame, width=25, textvariable=user_var, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Nombre de Usuario')
user.bind('<FocusIn>', borrar_texto_usuario)

# Campo de entrada de contraseña
code = tk.Entry(frame, width=25, textvariable=code_var, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show='•')
code.place(x=30, y=150)
code.insert(0, 'Contraseña')
code.bind('<FocusIn>', borrar_texto_contraseña)

# Botón de inicio de sesión
tk.Button(frame, width=39, pady=7, text='Ingresar', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

# Función para abrir la ventana de registro
def open_register_window(): #FUNCIONANDO CON LA BD----------------------------------
    register_window = tk.Toplevel(root)
    register_window.title('Registro de Usuario')
    register_window.geometry('700x700') 
    register_window.configure(bg='#fff')
    register_window.resizable(False, False)

    # USERNAME
    v_username=Label(register_window, text='Username:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_username.pack(pady=10)
    username_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    username_entry.pack() 

    # Nombre Completo
    v_nombreUsuario=Label(register_window, text='Nombre Completo:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_nombreUsuario.pack(pady=10)
    full_name_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    full_name_entry.pack() 

    # Apellido Paterno
    v_ApellidoUsuario=Label(register_window, text='Apellido Paterno:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_ApellidoUsuario.pack(pady=10)
    apellido_paterno_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    apellido_paterno_entry.pack() 

    # Apellido Materno
    v_ApellidoMaterno=Label(register_window, text='Apellido Materno:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_ApellidoMaterno.pack(pady=10)
    apellido_materno_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    apellido_materno_entry.pack() 

    # Crear Contraseña
    v_ContraseñaUsuario=Label(register_window, text='Crear Contraseña:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_ContraseñaUsuario.pack(pady=10)
    password_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show='*')
    password_entry.pack()

    # Confirmar Contraseña
    Contraseña1=Label(register_window, text='Confirmar Contraseña:', bg='white', font=('Microsoft YaHei UI Light', 11))
    Contraseña1.pack(pady=10)
    confirm_password_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show='*')
    confirm_password_entry.pack()

    # Correo Electrónico
    v_correoelectronico=Label(register_window, text='Correo Electrónico:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_correoelectronico.pack(pady=10)
    email_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    email_entry.pack()

    # Numero de celular
    v_NumCel=Label(register_window, text='Numero de celular:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_NumCel.pack(pady=10)
    celular_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    celular_entry.pack()

    # Numero de rol
    v_idRol=Label(register_window, text='ingresa numero de rol:', bg='white', font=('Microsoft YaHei UI Light', 11))
    v_idRol.pack(pady=10)
    rol_entry = Entry(register_window, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    rol_entry.pack()



    def InsertarUsuario(): #Funcionandooooooo (Funcion para insetar datos de la Base)
        try:
            v_username = username_entry.get()
            v_nombreUsuario =  full_name_entry.get()
            v_ApellidoUsuario = apellido_paterno_entry.get()
            v_ApellidoMaterno = apellido_materno_entry.get()
            v_ContraseñaUsuario = password_entry.get()
            v_correoelectronico = email_entry.get()
            v_NumCel = celular_entry.get()
            v_idRol = rol_entry.get()
            v_idStatus = 1
            with conexion.cursor() as cursor:
                cursor.callproc("insertar_usuario", args=(v_username,v_nombreUsuario, v_ApellidoUsuario, v_ApellidoMaterno, v_ContraseñaUsuario, v_correoelectronico, v_NumCel, v_idRol, v_idStatus))
            conexion.commit()  # Confirmar la transacción
            messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente.")
        except pymysql.Error as error:
            messagebox.showerror("Error", f"Error al insertar usuario: {error}")
       # finally:
        #    if conexion:
         #       conexion.close()  # Cerrar la conexión después de realizar todas las operaciones
# Crear el botón de guardar fuera de la función InsertarUsuario()
    Button(register_window, text='Guardar', width=10, pady=7, bg='#57a1f8', fg='white', border=0, command=InsertarUsuario).pack(pady=10)

# Botón de registro
sign_up = tk.Button(frame, width=6, text='Registrar', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=open_register_window)
sign_up.place(x=215, y=270)



# MAINLOOP
root.mainloop()