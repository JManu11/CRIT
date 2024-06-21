import tkinter as tk
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
from pyzbar import pyzbar
from PIL import Image, ImageDraw, ImageFont

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
                    dialog = QRInfoDialog(qr_data, "Receta.png", self)
                    dialog.exec_()
                self.hide()
            else:
                self.info_label.setText("No se ha detectado ningún código QR")

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

class QRInfoDialog(QDialog):
    def __init__(self, qr_data, template_path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Información del Código QR")
        self.qr_data = qr_data
        self.template_path = template_path

        # Load template image
        self.template_image = Image.open(self.template_path)

        # Add QR data to template image
        draw = ImageDraw.Draw(self.template_image)
        font = ImageFont.truetype("arial.ttf", 20)  # You may need to change the font path
        draw.text((20, 20), f"{self.qr_data}", fill="black", font=font)

        # Convert PIL image to QPixmap for displaying in QLabel
        img_data = self.template_image.convert("RGBA").tobytes("raw", "RGBA")
        q_image = QImage(img_data, self.template_image.size[0], self.template_image.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)

        self.info_label = QLabel("Contenido del código QR:")
        self.template_label = QLabel()
        self.template_label.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.template_label)

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
