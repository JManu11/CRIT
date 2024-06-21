from pyzbar import pyzbar
import cv2
import pymysql
from tkinter import messagebox
import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
import re
from pyzbar.pyzbar import decode

class ScanQRDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escaneo de QR")
        self.image_label = QLabel()
        self.info_label = QLabel("Procesando la imagen QR")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
        self.process_image("8799Carlos.png")

    def process_image(self, file_path):
        image = cv2.imread(file_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(convert_to_qt_format)
        self.image_label.setPixmap(pixmap)

        decoded_objs = pyzbar.decode(image)
        if decoded_objs:
            for obj in decoded_objs:
                qr_data = obj.data.decode('utf-8')  # Decodificar datos QR a UTF-8 string

                # Utilizar expresiones regulares para dividir los datos en campos
                fields = re.split(r'\s{4,}', qr_data.strip())

                # Imprimir los campos
                print("Campos del QR:")
                print(fields)

                if len(fields) :
                    
                    expediente = fields[1].strip()  # Número de expediente
                    peso = float(fields[3].strip())  # Peso
                    diagnostico = fields[4].strip()  # Diagnóstico
                    fecha = fields[5].strip()    
                    descripcion = fields[6].strip()  # Descripción
                    cedula_medico = fields[8].strip()  # Cédula del médico


                    descripcion11= descripcion.split('\n')
                    descripcion1 = '\n'.join(descripcion11[1:])

                    print(descripcion1)
                    self.guardar_datos_en_bd(peso, diagnostico, descripcion1, fecha, cedula_medico, expediente)
                else:
                    messagebox.showerror("Error", "Datos del QR no tienen el formato esperado.")
            
            self.close()

    def guardar_datos_en_bd(self, peso, diagnostico, descripcion, fecha, cedula_medico, expediente):
        try:
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='Mendoza1239',
                db='Proyecto_Teleton3'
            )

            with conexion.cursor() as cursor:
                v_idStatus = 1
                cursor.callproc("llenado_receta", 
                                (peso, diagnostico, descripcion, fecha, cedula_medico, expediente, v_idStatus))
                conexion.commit()

            messagebox.showinfo("Registro Exitoso", "Datos insertados exitosamente en la base de datos.")
        
        except pymysql.Error as error:
            messagebox.showerror("Error", f"Error al insertar datos en la base de datos: {error}")

        finally:
            if conexion:
                conexion.close()

    def closeEvent(self, event):
        event.accept()

def ejecutar_interfaz():
    app = QApplication(sys.argv)
    ventana = tk.Tk()
    ventana.title("Interfaz con Botón")
  
    def on_click():
        dialog = ScanQRDialog()
        dialog.exec_()

    boton = tk.Button(ventana, text="Escáner QR", command=on_click)
    boton.pack(pady=20)

    ventana.mainloop()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ejecutar_interfaz()
