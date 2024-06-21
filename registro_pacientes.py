from tkinter import *
from tkinter import Tk, Button, Label, Entry, Frame, Scrollbar, Listbox, END
from tkinter import messagebox
from PIL import Image, ImageTk
from fpdf import FPDF
from tkinter import Toplevel
import os
from typing import Any
import menu_segunda_pantalla

def main():
    def abrir_ventana_registro():     #Abre la vetana de regitroooo-----------------
        ventana_registro = Toplevel()
        ventana_registro.title('Registro de Pacientes')

    
    data = [
        ['ID', 'Nombre', 'Apellido', 'Edad', 'Núm. Requisición', 'Artículo Solicitado', 'Costo Aproximado', 'Estado de Pago', 'Num. Factura', 'Proveedor','Folio de Pago '],
        ['1', 'Juan', 'Perez', '30', '123456', 'Muletas', '$50', 'Pendiente','3333','muletas, s.a de c.v', '1111' ],
        ['2', 'Maria', 'Garcia', '25', '654321', 'Silla de ruedas', '$100', 'Pagado', '2222','Sillas, s.a de c.v','9898' ],
        # Agrega más filas según sea necesario
    ]

    def mostrar_info_detallada(id_paciente, info_paciente):
        ventana_info = Toplevel(root)
        ventana_info.title('Información Detallada')

        ventana_info.geometry(f"300x200+{int(ventana_info.winfo_screenwidth()/2 - 150)}+{int(ventana_info.winfo_screenheight()/2 - 100)}")

        etiquetas = ['Número de Requisición', 'Artículo Solicitado', 'Costo Aproximado', 'Estado de Pago', 'Num. Factura ', 'Proveedor', 'Folio de Pago']
        for i, campo in enumerate(info_paciente[4:]):
            label = Label(ventana_info, text=f"{etiquetas[i]}: {campo}")
            label.pack()

        cerrar_btn = Button(ventana_info, text='Cerrar', command=ventana_info.destroy)
        cerrar_btn.pack()

    def generar_pdf(id_paciente: Any) -> None:
        for paciente in data:
            if paciente[0] == id_paciente:
                info_paciente = paciente
                break

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)

        pdf.cell(200, 10, 'Centro de Rehabilitacion e Inclusion Infantil CRIT Hidalgo', 0, 1, 'C')

        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, f'ID: {info_paciente[0]}', 0, 1)
        pdf.cell(200, 10, f'Num. Factura : {info_paciente[1]}', 0, 1)
        pdf.cell(200, 10, f'Nombre: {info_paciente[2]} {info_paciente[2]}', 0, 1)
        pdf.cell(200, 10, f'Edad: {info_paciente[3]}', 0, 1)
        pdf.cell(200, 10, f'Núm. Requisición: {info_paciente[4]}', 0, 1)
        pdf.cell(200, 10, f'Artículo Solicitado: {info_paciente[5]}', 0, 1)
        pdf.cell(200, 10, f'Costo Aproximado: {info_paciente[6]}', 0, 1)
        pdf.cell(200, 10, f'Estado de Pago: {info_paciente[7]}', 0, 1)
        pdf.cell(200, 10, f'Num. Factura : {info_paciente[8]}', 0, 1)
        pdf.cell(200, 10, f'Proveedor: {info_paciente[9]}', 0, 1)
        pdf.cell(200, 10, f'Folio de Pago: {info_paciente[10]}', 0, 1)


        pdf_output = f"paciente_{id_paciente}.pdf"
        pdf.output(pdf_output)
        messagebox.showinfo("PDF Generado", f"Se ha generado el PDF para el paciente {info_paciente[1]} {info_paciente[2]}.")
        os.system(pdf_output)

    def agregar_paciente():
        id_paciente = entry_id.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        edad = entry_edad.get()
        num_req = entry_num_req.get()
        articulo = entry_articulo.get()
        costo = entry_costo.get()
        estado_pago = entry_estado_pago.get()
        #--------------------------------
        num_fac= entry_num_Factura.get()
        proveedor=entry_Proovedor.get()
        fol_Pago=entry_num_Folio.get()


        for paciente in data:
            if paciente[0] == id_paciente or (paciente[1], paciente[2], paciente[3], paciente[5]) == (nombre, apellido, edad, articulo):
                messagebox.showinfo("Paciente Existente", "Este paciente ya está registrado. Por favor, consulte sus datos y modifique si es necesario.")
                limpiar_formulario()
                return

        data.append([id_paciente, nombre, apellido, edad, num_req, articulo, costo, estado_pago,num_fac,proveedor,fol_Pago])
        mostrar_tabla_completa()
        limpiar_formulario()

    def limpiar_formulario() -> None:
        entry_id.delete(0, END)
        entry_nombre.delete(0, END)
        entry_apellido.delete(0, END)
        entry_edad.delete(0, END)
        entry_num_req.delete(0, END)
        entry_articulo.delete(0, END)
        entry_costo.delete(0, END)
        entry_estado_pago.delete(0, END)
        #------------------------
        entry_num_Factura.delete(0,END)
        entry_Proovedor.delete(0,END)
        entry_num_Folio.delete(0,END)

    def mostrar_tabla_completa(filtrar: bool = False, index: Any | None = None) -> None:
        for widget in table_frame.winfo_children():
            widget.grid_forget()
        for i, row in enumerate(data):
            if not filtrar or (filtrar and i == index):
                for j, cell in enumerate(row[:4]):
                    width = 20 if j == 2 else 10
                    cell_label = Label(table_frame, text=cell, width=width, borderwidth=1, relief="solid", bg="white")
                    cell_label.grid(row=i, column=j, padx=5, pady=5)

                    if i == 0:
                        cell_label.config(bg='#d9d9d9', font=('Arial', 12, 'bold'), relief="ridge")

                if i > 0:
                    green_button = Button(table_frame, text="Ver Información", bg="green", command=lambda id_paciente=data[i][0], info_paciente=data[i]: mostrar_info_detallada(id_paciente, info_paciente))
                    green_button.grid(row=i, column=4, padx=5, pady=5)

                    orange_button = Button(table_frame, text="Modificar Datos", bg="orange", command=lambda id_paciente=data[i][0]: modificar_datos(id_paciente))
                    orange_button.grid(row=i, column=5, padx=5, pady=5)

                    red_button = Button(table_frame, text="Generar PDF", bg="red", command=lambda id_paciente=data[i][0]: generar_pdf(id_paciente))
                    red_button.grid(row=i, column=6, padx=5, pady=5)

    def regresar_menu():
        root.destroy()  # Cierra la ventana actual
        root_menu = Tk()  # Crea una nueva instancia de Tk para la ventana del menú principal
        menu_principal = menu_segunda_pantalla.MenuPrincipal(root_menu)  # Crea la instancia del menú principal
        menu_principal.abrir_menu()  # Abre la ventana del menú principal
        root_menu.mainloop()  # Inicia el bucle de eventos para la ventana del menú principal


    root = Tk()
    root.title('Pacientes')
    root.geometry('1220x800')
    root.resizable(True, True)

    IMAGE_PATH = r"C:/Users/catal/OneDrive/Desktop/logo-CRIT-Hidalgo-removebg-preview.png"
    original_image = Image.open(IMAGE_PATH)

    aspect_ratio = original_image.width / original_image.height

    resized_height = 150
    resized_width = int(resized_height * aspect_ratio)
    resized_image = original_image.resize((resized_width, resized_height), Image.BILINEAR)

    logo_image = ImageTk.PhotoImage(resized_image)
    logo_label = Label(root, image=logo_image)
    logo_label.place(x=10, y=10)

    title_label = Label(root, text="Pacientes", font=("Arial", 30, 'bold'))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    formulario_frame = Frame(root)
    formulario_frame.place(relx=0.5, rely=0.2, anchor="center")

    Label(formulario_frame, text="ID:").grid(row=0, column=0)
    Label(formulario_frame, text="Nombre:").grid(row=0, column=2)
    Label(formulario_frame, text="Apellido:").grid(row=0, column=4)
    Label(formulario_frame, text="Edad:").grid(row=0, column=6)
    Label(formulario_frame, text="Núm. Requisición:").grid(row=1, column=0)
    Label(formulario_frame, text="Artículo Solicitado:").grid(row=1, column=2)
    Label(formulario_frame, text="Costo Aproximado:").grid(row=1, column=4)
    Label(formulario_frame, text="Estado de Pago:").grid(row=1, column=6)
    Label(formulario_frame, text="Num. Factura:").grid(row=2, column=0)
    Label(formulario_frame, text="Proveedores:").grid(row=2, column=2)
    Label(formulario_frame, text="Folio de Pago :") .grid(row=2, column=4)


    entry_id = Entry(formulario_frame)
    entry_id.grid(row=0, column=1)
    entry_nombre = Entry(formulario_frame)
    entry_nombre.grid(row=0, column=3)
    entry_apellido = Entry(formulario_frame)
    entry_apellido.grid(row=0, column=5)
    entry_edad = Entry(formulario_frame)
    entry_edad.grid(row=0, column=7)
    entry_num_req = Entry(formulario_frame)
    entry_num_req.grid(row=1, column=1)
    entry_articulo = Entry(formulario_frame)
    entry_articulo.grid(row=1, column=3)
    entry_costo = Entry(formulario_frame)
    entry_costo.grid(row=1, column=5)
    entry_estado_pago = Entry(formulario_frame)
    entry_estado_pago.grid(row=1, column=7)
    #-----------------
    entry_num_Factura= Entry(formulario_frame)
    entry_num_Factura.grid(row=2, column=1)
    entry_Proovedor= Entry(formulario_frame)
    entry_Proovedor.grid(row=2, column=3)
    entry_num_Folio= Entry(formulario_frame)
    entry_num_Folio.grid(row=2, column=5)

    button_agregar = Button(formulario_frame, text="Agregar Paciente", command=agregar_paciente)
    button_agregar.grid(row=3, columnspan=8, pady=5)

    button_limpiar = Button(formulario_frame, text="Limpiar Formulario", command=limpiar_formulario)
    button_limpiar.grid(row=4, columnspan=8, pady=5)

    table_frame = Frame(root)
    table_frame.place(relx=0.5, rely=0.3, anchor="center", y=150)

    mostrar_tabla_completa()

    def buscar_paciente():
        buscar_texto = entry_buscar.get().lower()
        for i, paciente in enumerate(data):
            if buscar_texto in paciente[1].lower() or buscar_texto in paciente[0].lower():
                mostrar_tabla_completa(filtrar=True, index=i)
                return
        mostrar_tabla_completa(filtrar=False)

    def borrar_busqueda():
        entry_buscar.delete(0, END)
        mostrar_tabla_completa()

    entry_buscar = Entry(root)
    entry_buscar.place(relx=0.1, rely=0.05, anchor="nw")

    Label(root, text="Nombre del paciente o ID:").place(relx=0.1, rely=0.025, anchor="nw")

    buscar_button = Button(root, text="Buscar", command=buscar_paciente)
    buscar_button.place(relx=0.25, rely=0.05, anchor="nw")

    borrar_button = Button(root, text="Borrar", command=borrar_busqueda)
    borrar_button.place(relx=0.3, rely=0.05, anchor="nw")

    regresar_btn = Button(root, text='Regresar al Menú', bg='yellow', command=regresar_menu)
    regresar_btn.place(relx=0.95, rely=0.95, anchor='se')

    def modificar_datos(id_paciente):
        ventana_modificar = Toplevel(root)
        ventana_modificar.title('Modificar Datos')
        ventana_modificar.geometry("300x300")

        for paciente in data:
            if paciente[0] == id_paciente:
                info_paciente = paciente
                break

        Label(ventana_modificar, text="Nombre:").grid(row=0, column=0)
        nombre_entry = Entry(ventana_modificar)
        nombre_entry.grid(row=0, column=1)
        nombre_entry.insert(0, info_paciente[1])

        Label(ventana_modificar, text="Apellido:").grid(row=1, column=0)
        apellido_entry = Entry(ventana_modificar)
        apellido_entry.grid(row=1, column=1)
        apellido_entry.insert(0, info_paciente[2])

        Label(ventana_modificar, text="Edad:").grid(row=2, column=0)
        edad_entry = Entry(ventana_modificar)
        edad_entry.grid(row=2, column=1)
        edad_entry.insert(0, info_paciente[3])

        Label(ventana_modificar, text="Núm. Requisición:").grid(row=3, column=0)
        num_req_entry = Entry(ventana_modificar)
        num_req_entry.grid(row=3, column=1)
        num_req_entry.insert(0, info_paciente[4])

        Label(ventana_modificar, text="Artículo Solicitado:").grid(row=4, column=0)
        articulo_entry = Entry(ventana_modificar)
        articulo_entry.grid(row=4, column=1)
        articulo_entry.insert(0, info_paciente[5])

        Label(ventana_modificar, text="Costo Aproximado:").grid(row=5, column=0)
        costo_entry = Entry(ventana_modificar)
        costo_entry.grid(row=5, column=1)
        costo_entry.insert(0, info_paciente[6])

        Label(ventana_modificar, text="Estado de Pago:").grid(row=6, column=0)
        estado_pago_entry = Entry(ventana_modificar)
        estado_pago_entry.grid(row=6, column=1)
        estado_pago_entry.insert(0, info_paciente[7])

        Label(ventana_modificar, text="Num. Factura:").grid(row=7, column=0)
        estado_pago_entry = Entry(ventana_modificar)
        estado_pago_entry.grid(row=7, column=1)
        estado_pago_entry.insert(0, info_paciente[8])

        Label(ventana_modificar, text="Proveedores :").grid(row=8, column=0)
        estado_pago_entry = Entry(ventana_modificar)
        estado_pago_entry.grid(row=8, column=1)
        estado_pago_entry.insert(0, info_paciente[9])

        Label(ventana_modificar, text="Folio de Pago:").grid(row=9, column=0)
        estado_pago_entry = Entry(ventana_modificar)
        estado_pago_entry.grid(row=9, column=1)
        estado_pago_entry.insert(0, info_paciente[10])



        def guardar_modificacion():
            info_paciente[1] = nombre_entry.get()
            info_paciente[2] = apellido_entry.get()
            info_paciente[3] = edad_entry.get()
            info_paciente[4] = num_req_entry.get()
            info_paciente[5] = articulo_entry.get()
            info_paciente[6] = costo_entry.get()
            info_paciente[7] = estado_pago_entry.get()
            info_paciente[8] = Num_fac_entry.get()
            info_paciente[9] = proveedor_entry.get()
            info_paciente[10]= fol_pago._entry.get()
            mostrar_tabla_completa()
            ventana_modificar.destroy()

        guardar_btn = Button(ventana_modificar, text='Guardar', command=guardar_modificacion)
        guardar_btn.grid(row=10, columnspan=2, pady=5)

        cancelar_btn = Button(ventana_modificar, text='Cancelar', command=ventana_modificar.destroy)
        cancelar_btn.grid(row=11, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()