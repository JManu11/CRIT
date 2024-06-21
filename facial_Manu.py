import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login Facial")

        self.label = tk.Label(self.root, text="Por favor, ingrese su nombre:")
        self.label.pack(pady=10)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.capture_button = tk.Button(self.root, text="Capturar", command=self.open_camera)
        self.capture_button.pack(pady=10)

        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()

        self.login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.prompt_login, state=tk.DISABLED)
        self.login_button.pack(pady=10)

        self.lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.root.bind('<space>', self.capture_face)
        self.video_capture = None

    def open_camera(self):
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

                    self.capture_button.config(state=tk.DISABLED)
                    self.login_button.config(state=tk.NORMAL)
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
        self.capture_button.config(state=tk.NORMAL)
        self.login_button.config(state=tk.DISABLED)
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

                    self.capture_button.config(state=tk.NORMAL)
                    self.login_button.config(state=tk.DISABLED)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
