import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import qrcode
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pymysql
import datetime

def receta():
    #---------------Conexion con la BD-----------------------------------
    try:
        conexion=pymysql.connect(host='localhost',
                                user='root',
                                password='Mendoza1239',
                                db='Proyecto_Teleton3'
                                )
        print("Conectado")
    except(pymysql.err.OperationalError,pymysql.err.InternalError) as e:
        print("Error: ", e)



    #-----------------------------------------------------
    # Diccionario con la información de los médicos acompañantes
    medicos_info = {
        'Dr. Juan': {
            'nombre': 'Dr. Juan José',
            'cedula': '3872526',
            'especialidad': 'Rehabilitación',
            'egresado': 'ESM/IPN'
        },
        'Dr. Federico': {
            'nombre': 'Dr. Federico',
            'cedula': '654321',
            'especialidad': 'Neurología',
            'egresado': 'IPN'
        },
        'Dr. Diana': {
            'nombre': 'Dr. Diana',
            'cedula': '112233',
            'especialidad': 'Pediatría',
            'egresado': 'UAM'
        }
    }

    def crear_cuadro_especificaciones():
        global cuadro_especificaciones
        cuadro_especificaciones = tk.Text(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
        cuadro_especificaciones.place(x=23, y=220, width=850, height=260)
        cuadro_especificaciones.config(bg='white', bd=0, relief=tk.SOLID)  # Configuración de color de fondo y borde
        cuadro_especificaciones.focus_set()  # Enfocar el cuadro de texto

    # Función para mostrar el calendario en la posición del clic del ratón
    def mostrar_calendario(event):
        cal.place(x=event.x_root, y=event.y_root)

    # Función para obtener la fecha seleccionada y mostrarla en la posición deseada
    def obtener_fecha():
        fecha_seleccionada = cal.get_date()
        etiqueta_fecha.config(text=fecha_seleccionada)  # Mostrar solo la fecha seleccionada sin texto adicional
        etiqueta_fecha.place(x=desired_x_position, y=desired_y_position)  # Establecer la posición deseada
        cal.place_forget()  # Oculta el calendario después de seleccionar la fecha

    # Función para resetear la pantalla
    def resetear_pantalla():
        # Limpiar campos de entrada
        nombre_paciente_entry.delete(0, tk.END)
        expediente_paciente_entry.delete(0, tk.END)
        edad_paciente_entry.delete(0, tk.END)
        peso_paciente_entry.delete(0, tk.END)
        diag_paciente_entry.delete(0, tk.END)
        fec_nac_paciente_entry.delete(0, tk.END)
        domicilio_paciente_entry.delete(0, tk.END)
        #descripcion_paciente_entry.delete(0,tk.END)
        nombre_medico_entry.delete(0, tk.END)
        cedula_medico_entry.delete(0, tk.END)
        especialidad_medico_entry.delete(0, tk.END)
        egresado_medico_entry.delete(0, tk.END)
    # cuadro_especificaciones_entry.delete(0,tk.END)

        # Limpiar cuadro de especificaciones
        cuadro_especificaciones.delete("1.0", tk.END)

    # Función para actualizar la información del médico acompañante
    def actualizar_info_medico(event):
        medico_seleccionado = medicos_acompanantes_combobox.get()
        if medico_seleccionado in medicos_info:
            info = medicos_info[medico_seleccionado]
            nombre_medico_entry.delete(0, tk.END)
            nombre_medico_entry.insert(0, info['nombre'])
            cedula_medico_entry.delete(0, tk.END)
            cedula_medico_entry.insert(0, info['cedula'])
            especialidad_medico_entry.delete(0, tk.END)
            especialidad_medico_entry.insert(0, info['especialidad'])
            egresado_medico_entry.delete(0, tk.END)
            egresado_medico_entry.insert(0, info['egresado'])
        
        # Restablecer el combobox al valor predeterminado
        medicos_acompanantes_combobox.set("Médicos")

    # Función para llenar la información del paciente desde la base de datos
    def llenar_informacion_paciente():
        num_expediente = expediente_paciente_entry.get()

        try:
            with conexion.cursor() as cursor:
                # Ejecutar una consulta SELECT en lugar de llamar a un procedimiento almacenado
                consulta = "SELECT nombre_pacientes,apellidopaterno_pacientes,apellidomaterno_pacientes, fecha_nacimiento_paciente FROM pacientes WHERE numero_expediente = %s"
                cursor.execute(consulta, (num_expediente,))
                resultado = cursor.fetchone()

                if resultado:
                    nombre_completo=resultado[0]+' '+ resultado[1]+' '+resultado[2]
                    nombre_paciente_entry.delete(0, tk.END)
                    nombre_paciente_entry.insert(0, nombre_completo)  # Llena el campo de nombre del paciente
                    fec_nac_paciente_entry.delete(0, tk.END)
                    fec_nac_paciente_entry.insert(0, resultado[3])  # Llena el campo de fecha de nacimiento


                    # Calcular la edad del paciente
                    fecha_nacimiento = resultado[3]  # Esta ya es una fecha en formato datetime.date
                    fecha_actual = datetime.date.today()

                    edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

                    edad_paciente_entry.delete(0, tk.END)
                    edad_paciente_entry.insert(0, edad)


                else:
                    messagebox.showerror("Error", "Paciente no encontrado en la base de datos.")

        except pymysql.Error as e:
            messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos: {str(e)}")




    # Función para generar el PDF con el código QR
    def generar_pdf(nombre_paciente, expediente_paciente):
        # Validar que los campos requeridos no estén vacíos
        if not nombre_paciente or not expediente_paciente:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el nombre y el expediente del paciente.")
            return
        
        edad_paciente = edad_paciente_entry.get()
        peso_paciente = peso_paciente_entry.get()
        diag_paciente = diag_paciente_entry.get()
        fec_nac_paciente = fec_nac_paciente_entry.get()
        domicilio_paciente = domicilio_paciente_entry.get()

        fecha_seleccionada = etiqueta_fecha.cget("text")
        nombre_medico = nombre_medico_entry.get()
        cedula = cedula_medico_entry.get()
        especialidad = especialidad_medico_entry.get()
        egresado = egresado_medico_entry.get()
    # medico_acompanante = medicos_acompanantes_combobox.get()
    #  especificaciones = cuadro_especificaciones_entry.get()
        especificaciones = cuadro_especificaciones.get("1.0", "end-1c")

        # Concatenar toda la información en una sola cadena
        informacion_total = (
            f"{fecha_seleccionada.rjust(145)}\n\n\n"
            f"{nombre_paciente.rjust(55)} {expediente_paciente.rjust(50)}\n"
            f"{edad_paciente.rjust(13)} {peso_paciente.rjust(36)} {diag_paciente.rjust(53)}\n\n"
            f"{fec_nac_paciente.rjust(43)} {domicilio_paciente.rjust(45)}\n"
            f"{especificaciones}\n\n\n\n\n\n\n\n\n"
            f"{nombre_medico.rjust(22)}\n"
            f"{cedula.rjust(22)}\n"
            f"{especialidad.rjust(22)}\n"
            f"{egresado.rjust(22)}"
        )

        # Generar código QR con la información total
        qr = qrcode.make(informacion_total)
        qr_path = f"{nombre_paciente}_{expediente_paciente}_codigo_qr.png"
        qr.save(qr_path)

        # Generar PDF con el código QR sobre la imagen de la receta
        pdf_path = f"{nombre_paciente}_{expediente_paciente}_codigo_qr.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Cargar la imagen de la receta
        receta_img = Image.open("Receta.png")
        receta_img = receta_img.resize((int(letter[0]), int(letter[1])))  # Redimensionar al tamaño de la página
        receta_img = ImageReader(receta_img)

        # Dibujar la imagen de la receta en el PDF
        c.drawImage(receta_img, 0, int(letter[1]) / 2, width=letter[0], height=letter[1]/2)
        
        # Posicionar la fecha seleccionada en la parte superior del PDF
        c.setFont("Helvetica", 12)
        c.drawString(450, 740, fecha_seleccionada)# Ajustar la coordenada Y para que esté en la parte superior del PDF
        c.drawString(133, 694, nombre_paciente)
        c.drawString(440, 694, expediente_paciente)
        c.drawString(68, 677, edad_paciente)
        c.drawString(206, 675, peso_paciente)
        c.drawString(366, 675, diag_paciente)
        c.drawString(141, 655, fec_nac_paciente)
        c.drawString(300, 655, domicilio_paciente)

        # Ajuste para especificaciones con saltos de línea
        y_position = 630
        for line in especificaciones.split("\n"):
            c.drawString(30, y_position, line)
            y_position -= 15  # Ajustar la posición Y para la siguiente línea

        c.drawString(90, 465, nombre_medico)
        c.drawString(88, 455, cedula)
        c.drawString(80, 445, especialidad)
        c.drawString(80, 435, egresado)

        # Dibujar el código QR en la receta (ajusta las coordenadas y el tamaño según sea necesario)
        qr_img = Image.open(qr_path)
        qr_img = qr_img.resize((150, 150), Image.Resampling.LANCZOS)
        qr_img = ImageReader(qr_img)
        c.drawImage(qr_img, 175, 70, width=250, height=250)  # Ajusta la posición (450, 400) y el tamaño (150x150) según sea necesario

        c.save()

        messagebox.showinfo("PDF Generado", "El PDF con el código QR se ha generado correctamente.")

        # Eliminar imagen temporal del código QR
        import os
        os.remove(qr_path)

        # Resetear la pantalla después de generar el PDF
        resetear_pantalla()


    ventana = tk.Tk()
    ventana.title("Receta")
    ventana.geometry("900x600")
    ventana.resizable(width=False, height=False)

    # Cargar la imagen de fondo
    fondo = tk.PhotoImage(file="Receta.png")
    fondo1 = tk.Label(ventana, image=fondo)
    fondo1.place(x=0, y=0, relwidth=1, relheight=1)

    # Crear el widget de calendario
    cal = Calendar(ventana, selectmode="day", date_pattern= "dd         /     mm    /    yyyy")

    # Widget de entrada para el nombre del paciente
    nombre_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    nombre_paciente_entry.place(x=185, y=132, width=300, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para el expediente
    expediente_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    expediente_paciente_entry.place(x=650, y=132, width=150, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para la edad
    edad_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    edad_paciente_entry.place(x=85, y=158, width=50, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para el peso
    peso_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    peso_paciente_entry.place(x=295, y=160, width=50, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para el diagnóstico
    diag_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    diag_paciente_entry.place(x=540, y=163, width=320, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para la fecha de nacimiento
    fec_nac_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    fec_nac_paciente_entry.place(x=200, y=190, width=120, height=20)  # Establece el tamaño del Entry

    # Widget de entrada para el domicilio
    domicilio_paciente_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    domicilio_paciente_entry.place(x=420, y=190, width=440, height=20)  # Establece el tamaño del Entry

    #Widget de Descripcion
    #cuadro_especificaciones_entry=tk.Entry(ventana, font=("Arial", 12),highlightthickness=0, bd=0)
    #cuadro_especificaciones_entry.place(x=23, y=220, width=850, height=260)


    # Widget de entrada para el nombre del medico
    nombre_medico_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    nombre_medico_entry.place(x=127, y=480, width=440, height=18)  # Establece el tamaño del Entry

    # Widget de entrada para la cedula del medico
    cedula_medico_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    cedula_medico_entry.place(x=127, y=498, width=100, height=17)  # Establece el tamaño del Entry

    # Widget de entrada para la especialidad del medico
    especialidad_medico_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    especialidad_medico_entry.place(x=100, y=513, width=150, height=16)  # Establece el tamaño del Entry

    # Widget de entrada para la escuela del medico
    egresado_medico_entry = tk.Entry(ventana, font=("Arial", 12), highlightthickness=0, bd=0)
    egresado_medico_entry.place(x=100, y=529, width=150, height=16)  # Establece el tamaño del Entry

    # Crear el cuadro de especificaciones
    crear_cuadro_especificaciones()

    # Etiqueta para mostrar la fecha seleccionada
    etiqueta_fecha = tk.Label(ventana, font=("Arial", 12), bg=ventana.cget('bg'), highlightthickness=0, bd=0)  # Configura el color de fondo para que sea el mismo que el de la ventana

    # Botón para obtener la fecha seleccionada
    boton_obtener_fecha = tk.Button(ventana, text="Fecha", command=obtener_fecha)
    boton_obtener_fecha.place(x=770, y=100)

    # Botón para generar el PDF con el código QR
    boton_generar_pdf = tk.Button(ventana, text="Generar PDF", command=lambda: generar_pdf(nombre_paciente_entry.get(), expediente_paciente_entry.get()))
    boton_generar_pdf.place(x=650, y=515,width=200,height=50)

    # Botón para llenar la información del paciente
    boton_llenar_info = tk.Button(ventana, text="Llenar Info", command=llenar_informacion_paciente)
    boton_llenar_info.place(x=810, y=130, width=70, height=20)

    # Coordenadas X e Y donde deseas que aparezca la etiqueta de fecha después de seleccionar la fecha de nacimiento
    desired_x_position = 700
    desired_y_position = 70

    # Lista desplegable para seleccionar el médico acompañante
    medicos_acompanantes_combobox = ttk.Combobox(ventana, values=list(medicos_info.keys()), font=("Arial", 12), state="readonly")
    medicos_acompanantes_combobox.set("Médicos")
    medicos_acompanantes_combobox.place(x=350, y=430, width=200, height=30)
    medicos_acompanantes_combobox.bind("<<ComboboxSelected>>", actualizar_info_medico)

    ventana.bind("<Button-3>", mostrar_calendario)  # Vincula el evento de clic derecho para mostrar el calendario
    ventana.mainloop()

if __name__ == "__main__":
    receta()