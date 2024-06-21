import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QDate, Qt
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cuadro de Mando Hospitalario")
        self.setGeometry(100, 100, 1200, 800)

        self.presupuesto_dos_meses_anteriores = 7000
        self.presupuesto_mensual_anterior = 8000
        self.presupuesto_mensual_actual = 10000

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap('C:/Users/tere_/OneDrive/Escritorio/logo-CRIT-Hidalgo-removebg-preview.png')
        logo_pixmap = pixmap.scaledToWidth(200)
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        hbox = QHBoxLayout()

        self.label_presupuesto_dos_meses_anteriores = QLabel(f"Presupuesto Dos Meses Anteriores: ${self.presupuesto_dos_meses_anteriores}")
        self.label_presupuesto_dos_meses_anteriores.setFont(QFont('Arial', 13))

        self.label_presupuesto_anterior = QLabel(f"Presupuesto Mensual Anterior: ${self.presupuesto_mensual_anterior}")
        self.label_presupuesto_anterior.setFont(QFont('Arial', 15))

        self.label_presupuesto_actual = QLabel(f"Presupuesto Mensual Actual: ${self.presupuesto_mensual_actual}")
        self.label_presupuesto_actual.setFont(QFont('Arial', 19))

        layout.addWidget(self.label_presupuesto_dos_meses_anteriores)
        layout.addWidget(self.label_presupuesto_anterior)
        layout.addWidget(self.label_presupuesto_actual)

        hbox_presupuestos = QHBoxLayout()
        hbox_presupuestos.addStretch(1)
        vbox_presupuestos = QVBoxLayout()
        vbox_presupuestos.addWidget(self.label_presupuesto_dos_meses_anteriores)
        vbox_presupuestos.addWidget(self.label_presupuesto_anterior)
        vbox_presupuestos.addWidget(self.label_presupuesto_actual)
        hbox_presupuestos.addLayout(vbox_presupuestos)
        hbox_presupuestos.addStretch(1)

        layout.addLayout(hbox)

        self.entry_presupuesto_dos_meses_anteriores = QLineEdit(str(self.presupuesto_dos_meses_anteriores))
        layout.addWidget(self.entry_presupuesto_dos_meses_anteriores)

        self.entry_presupuesto_anterior = QLineEdit(str(self.presupuesto_mensual_anterior))
        layout.addWidget(self.entry_presupuesto_anterior)

        self.entry_presupuesto_actual = QLineEdit(str(self.presupuesto_mensual_actual))
        layout.addWidget(self.entry_presupuesto_actual)

        hbox = QHBoxLayout()
        self.btn_modificar_presupuestos = QPushButton("Modificar Presupuestos")
        self.btn_modificar_presupuestos.clicked.connect(self.modificar_presupuestos)
        self.stylize_button(self.btn_modificar_presupuestos)
        hbox.addWidget(self.btn_modificar_presupuestos)
        hbox.addStretch(1)
        layout.addLayout(hbox)

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(9)

        self.entry_carnet = QLineEdit()
        self.entry_carnet.setPlaceholderText("Número de Carnet")
        form_layout.addWidget(QLabel("Número de Carnet:"), 0, 0)
        form_layout.addWidget(self.entry_carnet, 0, 1)

        self.entry_nombre = QLineEdit()
        self.entry_nombre.setPlaceholderText("Nombre(s)")
        form_layout.addWidget(QLabel("Nombre(s):"), 0, 2)
        form_layout.addWidget(self.entry_nombre, 0, 3)

        self.entry_apellido_materno = QLineEdit()
        self.entry_apellido_materno.setPlaceholderText("Apellido Materno")
        form_layout.addWidget(QLabel("Apellido Materno:"), 1, 0)
        form_layout.addWidget(self.entry_apellido_materno, 1, 1)

        self.entry_apellido_paterno = QLineEdit()
        self.entry_apellido_paterno.setPlaceholderText("Apellido Paterno")
        form_layout.addWidget(QLabel("Apellido Paterno:"), 1, 2)
        form_layout.addWidget(self.entry_apellido_paterno, 1, 3)

        self.combo_sexo = QComboBox()
        self.combo_sexo.addItems(["Masculino", "Femenino", "Otro"])
        self.stylize_combobox(self.combo_sexo)
        form_layout.addWidget(QLabel("Sexo:"), 2, 0)
        form_layout.addWidget(self.combo_sexo, 2, 1)

        self.entry_edad = QLineEdit()
        self.entry_edad.setPlaceholderText("Edad")
        form_layout.addWidget(QLabel("Edad:"), 2, 2)
        form_layout.addWidget(self.entry_edad, 2, 3)

        self.combo_tipo_apoyo = QComboBox()
        self.combo_tipo_apoyo.addItems(["Servicio Médico", "Medicamentos", "Ortesis y Prótesis", "Diversos Especie", "Terapia Asistida con Animales", "Otros"])
        self.stylize_combobox(self.combo_tipo_apoyo)
        form_layout.addWidget(QLabel("Tipo de Apoyo:"), 2, 4)
        form_layout.addWidget(self.combo_tipo_apoyo, 2, 5)

        self.entry_descripcion_apoyo = QLineEdit()
        self.entry_descripcion_apoyo.setPlaceholderText("Descripción de Apoyo")
        form_layout.addWidget(QLabel("Descripción de Apoyo:"), 3, 0)
        form_layout.addWidget(self.entry_descripcion_apoyo, 3, 1)

        self.entry_monto_economico = QLineEdit()
        self.entry_monto_economico.setPlaceholderText("Monto Económico")
        form_layout.addWidget(QLabel("Monto Económico:"), 3, 2)
        form_layout.addWidget(self.entry_monto_economico, 3, 3)

        self.date_edit_solicitud = QDateEdit()
        self.date_edit_solicitud.setCalendarPopup(True)
        self.date_edit_solicitud.setDate(QDate.currentDate())
        form_layout.addWidget(QLabel("Fecha de solicitud de Apoyo :"), 4, 0)
        form_layout.addWidget(self.date_edit_solicitud, 4, 1)

        self.date_edit_resolucion = QDateEdit()
        self.date_edit_resolucion.setCalendarPopup(True)
        self.date_edit_resolucion.setDate(QDate.currentDate())
        form_layout.addWidget(QLabel("Fecha de resolución de Apoyo :"), 4, 2)
        form_layout.addWidget(self.date_edit_resolucion, 4, 3)

        self.entry_entidad_federativa = QLineEdit()
        self.entry_entidad_federativa.setPlaceholderText("Entidad Federativa")
        form_layout.addWidget(QLabel("Entidad Federativa:"), 4, 4)
        form_layout.addWidget(self.entry_entidad_federativa, 4, 5)

        self.entry_costo = QLineEdit()
        self.entry_costo.setPlaceholderText("Costo de Apoyo Médico Aproximado")
        form_layout.addWidget(QLabel("Costo de Apoyo Médico Aproximado:"), 5, 0)
        form_layout.addWidget(self.entry_costo, 5, 1)

        self.entry_requisicion = QLineEdit()
        self.entry_requisicion.setPlaceholderText("Número de Requisición")
        form_layout.addWidget(QLabel("Número de Requisición:"), 5, 2)
        form_layout.addWidget(self.entry_requisicion, 5, 3)

        self.entry_factura = QLineEdit()
        self.entry_factura.setPlaceholderText("Número de Factura Médica")
        form_layout.addWidget(QLabel("Número de Factura Médica:"), 6, 0)
        form_layout.addWidget(self.entry_factura, 6, 1)

        self.entry_cobertura = QLineEdit()
        self.entry_cobertura.setPlaceholderText("Observaciones ")
        form_layout.addWidget(QLabel("Observaciones:"), 6, 2)
        form_layout.addWidget(self.entry_cobertura, 6, 3, 1, 2)

        self.btn_añadir_apoyo_medico = QPushButton("Añadir Apoyo Médico")
        self.btn_añadir_apoyo_medico.clicked.connect(self.aniadir_apoyo_medico)
        self.stylize_button(self.btn_añadir_apoyo_medico)
        form_layout.addWidget(self.btn_añadir_apoyo_medico, 7, 0, 1, 2)

        self.btn_modificar_en_excel = QPushButton("Modificar en Excel")
        self.stylize_button(self.btn_modificar_en_excel)
        self.btn_modificar_en_excel.clicked.connect(self.modificar_en_excel)
        form_layout.addWidget(self.btn_modificar_en_excel, 7, 2, 1, 2)

        self.table = QTableWidget()
        self.table.setColumnCount(15)
        self.table.setHorizontalHeaderLabels(["Número de Carnet", "Nombre(s)", "Apellido Materno", "Apellido Paterno", "Sexo", "Edad", "Tipo de Apoyo", "Descripción de Apoyo", "Monto Económico", "Fecha de solicitud de Apoyo", "Fecha de resolución de Apoyo", "Entidad Federativa", "Costo de Apoyo Médico Aproximado", "Número de Requisición", "Número de Factura Médica"])
        self.table.horizontalHeader().setDefaultSectionSize(200)

        self.load_data_from_excel()

        hbox = QHBoxLayout()
        self.btn_imprimir_tabla_pdf = QPushButton("Imprimir Tabla en PDF")
        self.btn_imprimir_tabla_pdf.clicked.connect(self.imprimir_tabla_pdf)
        self.stylize_button(self.btn_imprimir_tabla_pdf)
        hbox.addWidget(self.btn_imprimir_tabla_pdf)

        self.btn_mostrar_grafica = QPushButton("Mostrar Gráfica")
        self.btn_mostrar_grafica.clicked.connect(self.mostrar_grafica)
        self.stylize_button(self.btn_mostrar_grafica)
        hbox.addWidget(self.btn_mostrar_grafica)
        
        # Barra de búsqueda
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar en la tabla")
        self.search_bar.textChanged.connect(self.filter_table)
        form_layout.addWidget(QLabel("Buscar:"), 7, 4)
        form_layout.addWidget(self.search_bar, 7, 5)
        
        # Botón de búsqueda
        self.btn_buscar = QPushButton("Buscar")
        self.stylize_button(self.btn_buscar)
        self.btn_buscar.clicked.connect(self.filter_table)
        form_layout.addWidget(self.btn_buscar, 7,4,1,1)

        layout.addLayout(form_layout)
        layout.addWidget(self.table)
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def stylize_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: purple;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: Yellow;
            }
        """)

    def stylize_combobox(self, combobox):
        combobox.setStyleSheet("""
            QComboBox {
                background-color: purple;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                background-color: darkviolet;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: purple;
                selection-color: white;
            }
        """)

    def load_data_from_excel(self):
        excel_path = 'C:/Users/tere_/OneDrive/Documentos/datos.xlsx'
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
            self.table.setRowCount(len(df))
            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            QMessageBox.warning(self, "Error", f"El archivo {excel_path} no existe.")

    def modificar_presupuestos(self):
        try:
            self.presupuesto_dos_meses_anteriores = float(self.entry_presupuesto_dos_meses_anteriores.text())
            self.presupuesto_mensual_anterior = float(self.entry_presupuesto_anterior.text())
            self.presupuesto_mensual_actual = float(self.entry_presupuesto_actual.text())

            self.label_presupuesto_dos_meses_anteriores.setText(f"Presupuesto Dos Meses Anteriores: ${self.presupuesto_dos_meses_anteriores}")
            self.label_presupuesto_anterior.setText(f"Presupuesto Mensual Anterior: ${self.presupuesto_mensual_anterior}")
            self.label_presupuesto_actual.setText(f"Presupuesto Mensual Actual: ${self.presupuesto_mensual_actual}")

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores numéricos válidos para los presupuestos.")

    def aniadir_apoyo_medico(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition, 0, QTableWidgetItem(self.entry_carnet.text()))
        self.table.setItem(rowPosition, 1, QTableWidgetItem(self.entry_nombre.text()))
        self.table.setItem(rowPosition, 2, QTableWidgetItem(self.entry_apellido_materno.text()))
        self.table.setItem(rowPosition, 3, QTableWidgetItem(self.entry_apellido_paterno.text()))
        self.table.setItem(rowPosition, 4, QTableWidgetItem(self.combo_sexo.currentText()))
        self.table.setItem(rowPosition, 5, QTableWidgetItem(self.entry_edad.text()))
        self.table.setItem(rowPosition, 6, QTableWidgetItem(self.combo_tipo_apoyo.currentText()))
        self.table.setItem(rowPosition, 7, QTableWidgetItem(self.entry_descripcion_apoyo.text()))
        self.table.setItem(rowPosition, 8, QTableWidgetItem(self.entry_monto_economico.text()))
        self.table.setItem(rowPosition, 9, QTableWidgetItem(self.date_edit_solicitud.date().toString(Qt.ISODate)))
        self.table.setItem(rowPosition, 10, QTableWidgetItem(self.date_edit_resolucion.date().toString(Qt.ISODate)))
        self.table.setItem(rowPosition, 11, QTableWidgetItem(self.entry_entidad_federativa.text()))
        self.table.setItem(rowPosition, 12, QTableWidgetItem(self.entry_costo.text()))
        self.table.setItem(rowPosition, 13, QTableWidgetItem(self.entry_requisicion.text()))
        self.table.setItem(rowPosition, 14, QTableWidgetItem(self.entry_factura.text()))
        self.save_data_to_excel()

    def save_data_to_excel(self):
        rowCount = self.table.rowCount()
        colCount = self.table.columnCount()
        df = pd.DataFrame()
        for row in range(rowCount):
            for col in range(colCount):
                df.at[row, col] = self.table.item(row, col).text() if self.table.item(row, col) is not None else ""
        df.columns = ["Número de Carnet", "Nombre(s)", "Apellido Materno", "Apellido Paterno", "Sexo", "Edad", "Tipo de Apoyo", "Descripción de Apoyo", "Monto Económico", "Fecha de solicitud de Apoyo", "Fecha de resolución de Apoyo", "Entidad Federativa", "Costo de Apoyo Médico Aproximado", "Número de Requisición", "Número de Factura Médica"]
        df.to_excel('C:/Users/tere_/OneDrive/Documentos/datos.xlsx', index=False)

    def modificar_en_excel(self):
        self.save_data_to_excel()
        os.startfile('C:/Users/tere_/OneDrive/Documentos/datos.xlsx')

    def filter_table(self):
        filter_text = self.search_bar.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def imprimir_tabla_pdf(self):
        try:
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    pdf.cell(40, 10, item.text() if item else "", border=1)
                pdf.ln()

            pdf.output("tabla.pdf")
            QMessageBox.information(self, "Éxito", "La tabla ha sido exportada a PDF con éxito.")
        except ImportError:
            QMessageBox.warning(self, "Error", "No se pudo importar la biblioteca fpdf. Por favor, instálala primero.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Se produjo un error al exportar la tabla a PDF: {str(e)}")

    def mostrar_grafica(self):
        import matplotlib.pyplot as plt

        montos = []
        tipos_apoyo = []

        for row in range(self.table.rowCount()):
            item_monto = self.table.item(row, 8)
            item_tipo = self.table.item(row, 6)
            if item_monto and item_tipo:
                montos.append(float(item_monto.text()))
                tipos_apoyo.append(item_tipo.text())

        plt.bar(tipos_apoyo, montos)
        plt.xlabel('Tipo de Apoyo')
        plt.ylabel('Monto Económico')
        plt.title('Montos Económicos por Tipo de Apoyo')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
