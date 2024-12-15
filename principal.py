import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import xlrd
import glob
import pandas as pd
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


def radioButton_event(comunidad_seleccionada, ruta_seleccionada):
    print(f"Seleccionada {comunidad_seleccionada} hallada en fichero {ruta_seleccionada}")


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


def generar_botones_radio(df_comunidades):
    radio_var = tk.IntVar(value=0)
    contador = 0
    for comunidad in df_comunidades["NombreCorto"].unique():
        ctk.CTkRadioButton(frameLateral, text=comunidad,
                           command=lambda com_selec=comunidad, ruta_selec=
                           df_comunidades.loc[df_comunidades["NombreCorto"] == comunidad].values[0][1]:
                           radioButton_event(com_selec, ruta_selec),
                           variable=radio_var, value=contador).pack(padx=10, pady=5, anchor="w")
        contador += 1


def cargar_comunidades():
    initial_dir = r'C:\Users\Pedro Novafinkas\OneDrive\PEDRO'
    ruta_carpeta = filedialog.askdirectory(initialdir=initial_dir)
    if ruta_carpeta:
        df_comunidades = cargar_dataframe_comunidades(ruta_carpeta)
        generar_botones_radio(df_comunidades)


def generar_frame_lateral(ventana_padre):
    frameLateral = ctk.CTkScrollableFrame(ventana_padre, corner_radius=0)
    frameLateral.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Ocupa toda la altura con rowspan=2
    label = ctk.CTkLabel(frameLateral, text="Panel Lateral", font=("Arial", 14))
    label.pack(pady=20, padx=20)
    return frameLateral


def generar_frame_principal(ventana_padre):
    framePrincipal = ctk.CTkScrollableFrame(ventana_padre, corner_radius=0, fg_color="lightblue")
    framePrincipal.grid(row=0, column=1, sticky="nsew")
    label2 = ctk.CTkLabel(framePrincipal, text="Área Superior", font=("Arial", 14))
    label2.pack(pady=20, padx=20)


def generar_frame_botones(ventana_padre):
    frameBotones = ctk.CTkFrame(ventana_padre, corner_radius=0)
    frameBotones.grid(row=1, column=1, sticky="nsew")
    label3 = ctk.CTkLabel(frameBotones, text="Área Inferior", font=("Arial", 14))
    label3.pack(pady=10, padx=10)


def cargar_botones(frameBotones):
    ctk.CTkButton(frameBotones, text="Seleccionar carpeta de trabajo",
                                 command=cargar_comunidades).grid(row=1, column=1,pady=5, padx=10, sticky="w")

def principal(ventana_padre):
    ventana_padre.title("Balance Novafinkas")
    centrarPantalla(ventana_padre, 0.60)
    configurar_regilla(ventana_padre)
    frameLateral = generar_frame_lateral(ventana_padre)
    framePrincipal = generar_frame_principal(ventana_padre)
    frameBotones = generar_frame_botones(ventana_padre)
    cargar_botones(frameBotones)
    return frameLateral, framePrincipal, frameBotones


app = ctk.CTk()
frameLateral, framePrincipal, frameBotones = principal(app)
app.mainloop()
