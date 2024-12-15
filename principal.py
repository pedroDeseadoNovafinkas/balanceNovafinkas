import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import xlrd
import glob
import pandas as pd


import tkinter as tk

from CrearComunidades import ruta_archivo
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

def cargar_comunidades():
    df_comunidades = pd.DataFrame(columns=["NombreCorto", "Ruta"])
    initial_dir = r'C:\Users\Pedro Novafinkas\OneDrive\PEDRO'
    ruta_carpeta = filedialog.askdirectory(initialdir=initial_dir)
    if ruta_carpeta:
        archivos_excel = glob.glob(f"{ruta_carpeta}\\*.xls")
        for ruta_archivo in archivos_excel:
            workbook = xlrd.open_workbook(ruta_archivo)
            hoja = workbook.sheet_by_index(0)
            nombre_largo = hoja.cell_value(rowx=5, colx=1)
            nombre_corto = comunidades_dict.get(nombre_largo)
            nueva_fila = {"NombreCorto": nombre_corto, "Ruta": ruta_archivo}
            df_comunidades = pd.concat([df_comunidades, pd.DataFrame([nueva_fila])], ignore_index=True)
        radio_var = tk.IntVar(value=0)
        contador = 0
        for comunidad in df_comunidades["NombreCorto"].unique():
            ctk.CTkRadioButton(frameLateral, text = comunidad,
                               command= lambda com_selec= comunidad, ruta_selec = df_comunidades.loc[df_comunidades["NombreCorto"] == comunidad].values[0][1]:
                               radioButton_event(com_selec, ruta_selec),
                               variable=radio_var, value=contador).pack(padx = 10, pady = 5,anchor="w")
            contador += 1






app = ctk.CTk()
app.title("Balance Novafinkas")
centrarPantalla(app, 0.85)
configurar_regilla(app)

# Frame 1: Panel lateral (20% del ancho, todo el alto)
frameLateral = ctk.CTkScrollableFrame(app, corner_radius=0)
frameLateral.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Ocupa toda la altura con rowspan=2
label = ctk.CTkLabel(frameLateral, text="Panel Lateral", font=("Arial", 14))
label.pack(pady=20, padx=20)
#Comunidades


# Frame 2: Área superior (80% del ancho, 90% del alto)
framePrincipal = ctk.CTkScrollableFrame(app, corner_radius=0, fg_color="lightblue")
framePrincipal.grid(row=0, column=1, sticky="nsew")
label2 = ctk.CTkLabel(framePrincipal, text="Área Superior", font=("Arial", 14))
label2.pack(pady=20, padx=20)

# Frame 3: Área inferior (80% del ancho, 10% del alto)
frameBotones = ctk.CTkFrame(app, corner_radius=0)
frameBotones.grid(row=1, column=1, sticky="nsew")
label3 = ctk.CTkLabel(frameBotones, text="Área Inferior", font=("Arial", 14))
label3.pack(pady=10, padx=10)

boton_cargar = ctk.CTkButton(frameBotones, text="Seleccionar carpeta de trabajo",
                             command=cargar_comunidades).pack(pady=5, padx=10, anchor="w")

app.mainloop()
