import customtkinter as ctk
from tkinter import messagebox, StringVar
import pymysql
from PIL import Image
import menu_segunda_pantalla
import face_recognition
import cv2
import numpy as np

# Conexión con la base de datos
try:
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='CRIT'
    )
    print("Conectado")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Error: ", e)


# Función de cierre de sesión
def cerrar_sesion():
    user.delete(0, 'end')
    code.delete(0, 'end')


# Función de inicio de sesión
def signin():
    with conexion.cursor() as cursor:
        usuario = user.get()
        contraseña = code.get()
        consulta = "SELECT * FROM usuario WHERE username = %s AND contraseñaUsuario = %s"
        cursor.execute(consulta, (usuario, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            messagebox.showinfo("Ingreso Exitoso", "Bienvenido!")
            for widget in frame.winfo_children():
                widget.destroy()
            menu_principal = menu_segunda_pantalla.MenuPrincipal(root)
            menu_principal.abrir_menu()
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
root = ctk.CTk()
root.title('Login')
root.geometry('900x500+300+200')
root.configure(bg="#fff")
root.resizable(True, True)

# Imagenes del código...
img = Image.open('C:/Users/catal/OneDrive/Desktop/prototipo_interfaz_1/prototipo_interfaz_1/logo_10.png')
img = ctk.CTkImage(img, size=(350, 350))
img_label = ctk.CTkLabel(root, image=img)
img_label.place(x=50, y=50)

frame = ctk.CTkFrame(root, width=350, height=350)
frame.place(x=480, y=70)

admin_img = Image.open('C:/Users/catal/OneDrive/Desktop/prototipo_interfaz_1/prototipo_interfaz_1/capacidad_1.png')
admin_img = ctk.CTkImage(admin_img, size=(150, 150))
ctk.CTkLabel(frame, image=admin_img).place(relx=0.5, rely=0.0, anchor=ctk.N)

heading = ctk.CTkLabel(frame, text='Administrador', font=('Arial', 17, 'bold'), text_color='#57a1f8')
heading.place(relx=0.2, rely=0.9, anchor=ctk.N)

trabajo_social_label = ctk.CTkLabel(root, text='Trabajo Social', text_color='purple', font=('Arial', 25, 'bold'))
trabajo_social_label.place(x=100, y=410)

# Campos de entrada
user_var = StringVar()
code_var = StringVar()

# Campo de entrada de usuario
user = ctk.CTkEntry(frame, width=220, textvariable=user_var, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
user.place(x=65, y=100)
user.insert(0, 'Nombre de Usuario')
user.bind('<FocusIn>', borrar_texto_usuario)

# Campo de entrada de contraseña
code = ctk.CTkEntry(frame, width=220, textvariable=code_var, corner_radius=10, font=('Microsoft YaHei UI Light', 11), show='*')
code.place(x=65, y=160)
code.insert(0, 'Contraseña')
code.bind('<FocusIn>', borrar_texto_contraseña)

# Botón de inicio de sesión
ctk.CTkButton(frame, width=220, height=40, text='Ingresar', fg_color='#57a1f8', corner_radius=10, command=signin).place(x=65, y=220)

# Función para abrir la ventana de registro
def open_register_window():
    register_window = ctk.CTkToplevel(root)
    register_window.title('Registro de Usuario')
    register_window.geometry('700x750')
    register_window.configure(bg='#fff')
    register_window.resizable(False, False)

    # USERNAME
    ctk.CTkLabel(register_window, text='Username:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    username_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    username_entry.pack()

    # Nombre Completo
    ctk.CTkLabel(register_window, text='Nombre Completo:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    full_name_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    full_name_entry.pack()

    # Apellido Paterno
    ctk.CTkLabel(register_window, text='Apellido Paterno:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    apellido_paterno_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    apellido_paterno_entry.pack()

    # Apellido Materno
    ctk.CTkLabel(register_window, text='Apellido Materno:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    apellido_materno_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    apellido_materno_entry.pack()

    # Crear Contraseña
    ctk.CTkLabel(register_window, text='Crear Contraseña:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    password_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11), show='*')
    password_entry.pack()

    # Confirmar Contraseña
    ctk.CTkLabel(register_window, text='Confirmar Contraseña:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    confirm_password_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11), show='*')
    confirm_password_entry.pack()

    # Correo Electrónico
    ctk.CTkLabel(register_window, text='Correo Electrónico:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    email_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    email_entry.pack()

    # Numero de celular
    ctk.CTkLabel(register_window, text='Numero de celular:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    celular_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    celular_entry.pack()

    # Numero de rol
    ctk.CTkLabel(register_window, text='ingresa numero de rol:', font=('Microsoft YaHei UI Light', 11)).pack(pady=10)
    rol_entry = ctk.CTkEntry(register_window, width=220, corner_radius=10, font=('Microsoft YaHei UI Light', 11))
    rol_entry.pack()

    def InsertarUsuario():
        try:
            v_username = username_entry.get()
            v_nombreUsuario = full_name_entry.get()
            v_ApellidoUsuario = apellido_paterno_entry.get()
            v_ApellidoMaterno = apellido_materno_entry.get()
            v_ContraseñaUsuario = password_entry.get()
            v_correoelectronico = email_entry.get()
            v_NumCel = celular_entry.get()
            v_idRol = rol_entry.get()
            v_idStatus = 1
            with conexion.cursor() as cursor:
                cursor.callproc("insertar_usuario", args=(v_username, v_nombreUsuario, v_ApellidoUsuario, v_ApellidoMaterno, v_ContraseñaUsuario, v_correoelectronico, v_NumCel, v_idRol, v_idStatus))
            conexion.commit()
            messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente.")
        except pymysql.Error as error:
            messagebox.showerror("Error", f"Error al insertar usuario: {error}")

    ctk.CTkButton(register_window, text='Guardar', width=100, height=40, fg_color='#57a1f8', corner_radius=10, command=InsertarUsuario).pack(pady=20)


def registro_facial():

    def register_face():

        video_capture = cv2.VideoCapture(0)
        print("Por favor, coloca tu cara frente a la cámara y presiona 'q' para capturar la imagen.")

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Video', frame)

            # Presiona 'q' para capturar la imagen y registrar la cara
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("registered_face.jpg", frame)
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Cargar la imagen y codificar la cara
        registered_image = face_recognition.load_image_file("registered_face.jpg")
        registered_face_encoding = face_recognition.face_encodings(registered_image)[0]

        # Guardar la codificación de la cara registrada
        np.save("registered_face_encoding.npy", registered_face_encoding)
        print("Registro completo. La codificación de la cara ha sido guardada.")

    def verify_face():
        # Cargar la codificación de la cara registrada
        registered_face_encoding = np.load("registered_face_encoding.npy")

        # Inicializar la captura de video
        video_capture = cv2.VideoCapture(0)
        print("Por favor, coloca tu cara frente a la cámara para verificar tu identidad.")

        while True:
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]

            # Encontrar todas las caras en el frame actual
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([registered_face_encoding], face_encoding)
                if True in matches:
                    print("Acceso Concedido")
                else:
                    print("Acceso Denegado")

            cv2.imshow('Video', frame)

            # Presiona 'q' para salir del loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    # Registrar la cara (comentar esta línea si ya has registrado la cara)
    register_face()

    # Verificar la cara para el login
    verify_face()



# Botón de registro
sign_up = ctk.CTkButton(frame, width=100, height=40, text='Registrar', fg_color='#57a1f8', corner_radius=10, command=open_register_window)
sign_up.place(x=125, y=280)

registro_facial = ctk.CTkButton(frame, width=100, height=40, text='Registro Facial', fg_color='#57a1f8', corner_radius=10, command=registro_facial)
sign_up.place(x=130, y=280)

# MAINLOOP
root.mainloop()
