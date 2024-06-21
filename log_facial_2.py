import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import pymysql

# Conexión con la base de datos
try:
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='Mendoza1239',
        db='Proyecto_Teleton3'
    )
    print("Conectado")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Error: ", e)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login Facial")
        self.root.geometry('900x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(True, True)
        
        self.label = ctk.CTkLabel(self.root, text="Por favor, ingrese su nombre:", font=('Arial', 16))
        self.label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self.root, width=220, font=('Microsoft YaHei UI Light', 11))
        self.name_entry.pack(pady=5)

        self.capture_button = ctk.CTkButton(self.root, text="Capturar", command=self.open_camera)
        self.capture_button.pack(pady=10)

        self.video_frame = ctk.CTkLabel(self.root)
        self.video_frame.pack()

        self.login_button = ctk.CTkButton(self.root, text="Iniciar Sesión", command=self.prompt_login, state=ctk.DISABLED)
        self.login_button.pack(pady=10)

        self.lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.root.bind('<space>', self.capture_face)
        self.video_capture = None

    def open_camera(self):
        if self.video_capture is None or not self.video_capture.isOpened():
            self.video_capture = cv2.VideoCapture(0)
            self.update_video_feed()

    def capture_face(self, event=None):
        if self.video_capture and self.video_capture.isOpened():
            user_name = self.name_entry.get().strip()
            if not user_name:
                messagebox.showerror("Error", "Por favor, ingrese su nombre.")
                return
            
            ret, frame = self.video_capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) > 0:
                    (x, y, w, h) = faces[0]
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))  # Asegurarse de que el tamaño de la imagen sea consistente
                    user_image_path = f"user_images/{user_name}.jpg"
                    os.makedirs(os.path.dirname(user_image_path), exist_ok=True)
                    cv2.imwrite(user_image_path, face)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    img = ImageTk.PhotoImage(image=img)
                    self.video_frame.configure(image=img)
                    self.video_frame.image = img

                    self.capture_button.config(state=ctk.DISABLED)
                    self.login_button.config(state=ctk.NORMAL)
                    self.train_recognizer(user_image_path)
                    self.close_camera()  # Cerrar la cámara después de capturar la imagen
                else:
                    messagebox.showerror("Error", "No se detectó ningún rostro. Intente nuevamente.")
            else:
                messagebox.showerror("Error", "No se pudo capturar la imagen. Intente nuevamente.")
        else:
            messagebox.showerror("Error", "La cámara no está abierta.")

    def prompt_login(self):
        self.label.config(text="Por favor, ingrese su nombre para iniciar sesión:")
        self.capture_button.config(state=ctk.NORMAL)
        self.login_button.config(state=ctk.DISABLED)
        self.root.bind('<space>', self.verify_face)
    
    def verify_face(self, event=None):
        user_name = self.name_entry.get().strip()
        if not user_name:
            messagebox.showerror("Error", "Por favor, ingrese su nombre.")
            return

        user_image_path = f"user_images/{user_name}.jpg"
        if not os.path.exists(user_image_path):
            messagebox.showerror("Error", f"No hay datos para el usuario {user_name}.")
            return

        self.open_camera()

        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) > 0:
                    (x, y, w, h) = faces[0]
                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))  # Asegurarse de que el tamaño de la imagen sea consistente

                    label, confidence = self.lbph_recognizer.predict(face)
                    print(f"Label: {label}, Confidence: {confidence}")

                    if confidence < 50:  # Ajuste del umbral de confianza
                        messagebox.showinfo("Acceso concedido", "Verificación facial exitosa. Acceso concedido.")
                    else:
                        messagebox.showerror("Acceso denegado", "Verificación facial fallida. Acceso denegado.")

                    self.capture_button.config(state=ctk.NORMAL)
                    self.login_button.config(state=ctk.DISABLED)
                    self.close_camera()  # Cerrar la cámara después de la verificación
                    self.root.unbind('<space>')
                else:
                    messagebox.showerror("Error", "No se detectó ningún rostro. Intente nuevamente.")
            else:
                messagebox.showerror("Error", "No se pudo capturar la imagen. Intente nuevamente.")
        else:
            messagebox.showerror("Error", "La cámara no está abierta.")

    def train_recognizer(self, user_image_path):
        face_image = cv2.imread(user_image_path, cv2.IMREAD_GRAYSCALE)
        self.lbph_recognizer.train([face_image], np.array([0]))

    def close_camera(self):
        if self.video_capture and self.video_capture.isOpened():
            self.video_capture.release()
            self.video_capture = None
            self.video_frame.configure(image=None)
            self.video_frame.image = None

    def update_video_feed(self):
        if self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb = Image.fromarray(frame_rgb)
                frame_rgb = ImageTk.PhotoImage(image=frame_rgb)
                self.video_frame.configure(image=frame_rgb)
                self.video_frame.image = frame_rgb
                self.video_frame.after(10, self.update_video_feed)
            else:
                self.video_frame.configure(image=None)
                self.video_frame.image = None

    def signin(self):
        with conexion.cursor() as cursor:
            usuario = self.name_entry.get()
            contraseña = self.code.get()
            consulta = "SELECT * FROM usuario WHERE username = %s AND contraseñaUsuario = %s"
            cursor.execute(consulta, (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showinfo("Ingreso Exitoso", "Bienvenido!")
                for widget in self.root.winfo_children():
                    widget.destroy()
                menu_principal = menu_segunda_pantalla.MenuPrincipal(self.root)
                menu_principal.abrir_menu()
            else:
                messagebox.showerror("Error de Ingreso", "Correo electrónico, contraseña o nombre incorrectos.")

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
    ctk.CTkLabel(register_window, text='Nombre Completo:', font=('Microsoft YaHei UILight', 11)).pack(pady=10)
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

# Botón de registro
root = ctk.CTk()
app = LoginApp(root)
sign_up = ctk.CTkButton(root, width=100, height=40, text='Registrar', fg_color='#57a1f8', corner_radius=10, command=open_register_window)
sign_up.place(x=125, y=280)

root.mainloop()

