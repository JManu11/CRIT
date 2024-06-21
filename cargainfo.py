from pyzbar import pyzbar
import cv2
import pymysql
from tkinter import messagebox
import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import re
from pyzbar.pyzbar import decode

class ScanQRDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Escaneo de QR")
        self.image_label = QLabel()
        self.info_label = QLabel("Apunte la cámara hacia un código QR")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)

        self.setLayout(layout)

        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            self.image_label.setPixmap(pixmap)

            decoded_objs = pyzbar.decode(frame)
            if decoded_objs:
                for obj in decoded_objs:
                    qr_data = obj.data.decode('utf-8')  

                    #Indico que busco datos cada 4 espacios
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

                        self.guardar_datos_en_bd(peso, diagnostico, descripcion1, fecha, cedula_medico, expediente)
                    else:
                        messagebox.showerror("Error", "Datos del QR no tienen el formato esperado.")
            
                self.close()


    def guardar_datos_en_bd(self,peso, diagnostico, descripcion, fecha, cedula_medico,expediente):
        try:
            conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='CRIT'
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
        self.camera.release()
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
