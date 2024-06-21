import tkinter as tk
from tkinter import messagebox
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
import cv2
from pyzbar import pyzbar

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
                    dialog = QRInfoDialog(qr_data)
                    dialog.exec_()
                self.close()
            else:
                self.info_label.setText("No se ha detectado ningún código QR")

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

class QRInfoDialog(QDialog):
    def __init__(self, qr_data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Información del Código QR")
        self.qr_data = qr_data

        self.info_label = QLabel(f"Contenido del código QR:\n{self.qr_data}")

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)

        self.setLayout(layout)

def ejecutar_interfaz():
    ventana = tk.Tk()
    ventana.title("Interfaz con Botón")
  
    def on_click():
        dialog = ScanQRDialog()
        dialog.exec_()

    boton = tk.Button(ventana, text="Escáner QR", command=on_click)
    boton.pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ejecutar_interfaz()
    sys.exit(app.exec_())
