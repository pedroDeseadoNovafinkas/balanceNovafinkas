import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import customtkinter as ctk
import xlrd
import glob
import pandas as pd
from pandastable import Table, TableModel, config
from comunidades import *

def centrarPantalla(windows, factor):
    anchoPantalla = windows.winfo_screenwidth()
    altoPantalla = windows.winfo_screenheight()
    anchoVentana = int(anchoPantalla * factor)
    altoVentana = int(altoPantalla * factor)
    x = int((anchoPantalla - anchoVentana) /2)
    y = int((altoPantalla - altoVentana) /2)
    windows.geometry(f'{anchoVentana}x{altoVentana}+{x}+{y}')


def configurar_regilla(windows):
    app.grid_rowconfigure(0, weight=19)  # Primera fila (90% del alto)
    app.grid_rowconfigure(1, weight=1)  # Segunda fila (10% del alto)
    app.grid_columnconfigure(0, weight=1)  # Primera columna (20% del ancho)
    app.grid_columnconfigure(1, weight=9)  # Segunda columna (80% del ancho)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    return frame

def aumentar_tabla(tabla, veces):
    for i in range(1, veces):
        tabla.zoomIn()
    return tabla

def radioButton_event(comunidad_seleccionada, ruta_seleccionada, framePrincipal):
    print(f"Seleccionada {comunidad_seleccionada} hallada en fichero {ruta_seleccionada}")
    framePrincipal= limpiar_frame(framePrincipal)

    df = pd.read_excel(ruta_seleccionada, skiprows= 8, usecols=["F. Operativa","Concepto","Importe","Saldo"], engine='xlrd')

    style = ttk.Style()
    style.configure("Treeview", rowheight=40, font=("Arial", 18))  # Fuente para las celdas
    style.configure("Treeview.Heading", font=("Arial", 24, "bold"))  # Fuente para los encabezados

    tabla = ttk.Treeview(framePrincipal, columns=list(df.columns), show="headings", height=600)


    tabla.column('F. Operativa', width = 250, anchor = 'c')
    tabla.column('Concepto',  width = 900, anchor = 'w')
    tabla.column('Importe',  width = 250, anchor = 'c')
    tabla.column('Saldo',  width = 250, anchor = 'c')

    tabla.heading('F. Operativa', text="Fecha", anchor='c')
    tabla.heading('Concepto', text="Concepto", anchor='w')
    tabla.heading('Importe', text="Importe", anchor='c')
    tabla.heading('Saldo', text="Saldo", anchor='c')
    for _, row in df.iterrows():
        tabla.insert("", "end", values=list(row))
    tabla.pack(fill='x')

def cargar_dataframe_comunidades(ruta_carpeta):
    df_comunidades = pd.DataFrame(columns=["NombreCorto", "Ruta"])
    archivos_excel = glob.glob(f"{ruta_carpeta}\\*.xls")
    for ruta_archivo in archivos_excel:
        workbook = xlrd.open_workbook(ruta_archivo)
        hoja = workbook.sheet_by_index(0)
        nombre_largo = hoja.cell_value(rowx=5, colx=1)
        nombre_corto = comunidades_dict.get(nombre_largo)
        nueva_fila = {"NombreCorto": nombre_corto, "Ruta": ruta_archivo}
        df_comunidades = pd.concat([df_comunidades, pd.DataFrame([nueva_fila])], ignore_index=True)
    return df_comunidades


def generar_botones_radio(df_comunidades, frame):
    radio_var = tk.IntVar(value=0)
    contador = 0
    for comunidad in df_comunidades["NombreCorto"].unique():
        ctk.CTkRadioButton(frameLateral, text=comunidad,
                           command=lambda com_selec=comunidad,
                           ruta_selec = df_comunidades.loc[df_comunidades["NombreCorto"] == comunidad].values[0][1],
                           framePrincipal = frame:
                           radioButton_event(com_selec, ruta_selec, framePrincipal),
                           variable=radio_var, value=contador).pack(padx=10, pady=5, anchor="w")
        contador += 1


def cargar_comunidades(boton_carga, frame):
    initial_dir = r'C:\Users\Pedro Novafinkas\OneDrive\PEDRO'
    ruta_carpeta = filedialog.askdirectory(initialdir=initial_dir)
    if ruta_carpeta:
        df_comunidades = cargar_dataframe_comunidades(ruta_carpeta)
        generar_botones_radio(df_comunidades, frame)
        boton_carga.configure(state="disabled")


def generar_frame_lateral(ventana_padre):
    frameLateral = ctk.CTkScrollableFrame(ventana_padre, corner_radius=0)
    frameLateral.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Ocupa toda la altura con rowspan=2
    label = ctk.CTkLabel(frameLateral, text="Panel Lateral", font=("Arial", 14))
    label.pack(pady=20, padx=20)
    return frameLateral


def generar_frame_principal(ventana_padre):
    framePrincipal = ctk.CTkScrollableFrame(ventana_padre, corner_radius=0, fg_color="lightblue")
    #framePrincipal = tk.Frame(ventana_padre)
    framePrincipal.grid(row=0, column=1, sticky="nsew")
    return framePrincipal



def generar_frame_botones(ventana_padre, frame):
    frameBotones = ctk.CTkFrame(ventana_padre, corner_radius=0)
    frameBotones.grid(row=1, column=1, sticky="nsew")
    label3 = ctk.CTkLabel(frameBotones, text="Área Inferior", font=("Arial", 14))
    label3.pack(pady=10, padx=10)
    cargar_botones(ventana_padre, frame)


def cargar_botones(frameBotones, frame):
    boton_carga = ctk.CTkButton(frameBotones, text="Seleccionar carpeta de trabajo",
                                 command=lambda: cargar_comunidades(boton_carga, frame))
    boton_carga.grid(row=1, column=1,pady=5, padx=10, sticky="w")


def principal(ventana_padre):
    ventana_padre.title("Balance Novafinkas")
    centrarPantalla(ventana_padre, 0.85)
    configurar_regilla(ventana_padre)
    frameLateral = generar_frame_lateral(ventana_padre)
    framePrincipal = generar_frame_principal(ventana_padre)
    frameBotones = generar_frame_botones(app, framePrincipal)

    return frameLateral, framePrincipal, frameBotones

'''
Empieza aquí el programa principal
'''

app = ctk.CTk()
frameLateral, framePrincipal, frameBotones = principal(app)


app.mainloop()
