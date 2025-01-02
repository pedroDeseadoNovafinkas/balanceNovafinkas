import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import customtkinter as ctk
import xlrd
import glob
import pandas as pd
from pandastable import Table, TableModel, config
from comunidades import *

factorX=0.85
factorY=0.80

meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]

def calculartamanoPantalla(windows):
    anchoPantalla = windows.winfo_screenwidth()
    altoPantalla = windows.winfo_screenheight()
    return anchoPantalla, altoPantalla


def tamanoLetra(windows):
    X, Y = calculartamanoPantalla(windows)
    print(X, Y)


def centrarPantalla(windows, factorX, factorY):
    anchoPantalla, altoPantalla = calculartamanoPantalla(windows)
    anchoVentana = int(anchoPantalla * (factorX))
    altoVentana = int(altoPantalla * factorY)
    x = int((anchoPantalla - anchoVentana) /2)
    y = int((altoPantalla - altoVentana) /2)
    windows.geometry(f'{anchoVentana}x{altoVentana}+{x}+{y}')
    return anchoVentana, altoVentana

def centrarPantallaManual(windows):
    windows.geometry('500x500')


def configurar_regilla(windows, anchoPantalla, altoPantalla):
    windows.grid_rowconfigure(0, weight=9, minsize=anchoPantalla*0.9)  # Primera fila (90% del alto)
    windows.grid_rowconfigure(1, weight=1, minsize=anchoPantalla*0.1)  # Segunda fila (10% del alto)
    windows.grid_columnconfigure(0, weight=1, minsize=altoPantalla*0.2)  # Primera columna (20% del ancho)
    windows.grid_columnconfigure(1, weight=9, minsize=altoPantalla*0.8)  # Segunda columna (80% del ancho)

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    return frame

def generarPandasTables(frame, df):
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    #table.config
    table.grid(row=0, column=1, sticky='n', padx=5, pady=5)
    print(config.load_options())
    return table


def radioButton_event(comunidad_seleccionada, ruta_seleccionada, framePrincipal):
    global tabla
    framePrincipal= limpiar_frame(framePrincipal)
    df = pd.read_excel(ruta_seleccionada, skiprows= 8, usecols=["F. Operativa","Concepto","Importe","Saldo"], engine='xlrd')
    df.insert(1, 'PROVEEDOR', None)
    df.insert(2, 'CUENTA', None)
    df.insert(3, 'CONCEPTOD', None)

    tabla = generarPandasTables(framePrincipal, df)
    tabla.show()
    options = {'fontsize': 14, 'rowheight':30}
    config.apply_options(options, tabla)
    tabla.columnwidths = {"F. Operativa":150, "PROVEEDOR": 300, "CUENTA": 300, "CONCEPTOD": 700, "Concepto":700, "Importe":150, "Saldo":150}
    tabla.redraw()


def cargar_dataframe_comunidades(ruta_carpeta):
    df_comunidades = pd.DataFrame(columns=["NombreCorto", "Ruta"])
    archivos_excel = glob.glob(f"{ruta_carpeta}\\*.xls")
    for ruta_archivo in archivos_excel:
        workbook = xlrd.open_workbook(ruta_archivo)
        hoja = workbook.sheet_by_index(0)
        nombre_largo = hoja.cell_value(rowx=5, colx=1)
        nombre_corto = comunidades_dict.get(nombre_largo)
        if nombre_corto is None:
            raise ValueError(f"No se ha encontrado el valor al que corresponde {nombre_largo}")
        else:
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
    #framePrincipal = ctk.CTkScrollableFrame(ventana_padre, corner_radius=0, fg_color="lightblue")
    framePrincipal = ttk.Frame(ventana_padre)
    framePrincipal.grid(row=0, column=1, columnspan= 2, sticky="nsew")
    return framePrincipal


def generar_frame_botones(ventana_padre, frame):
    frameBotones = ctk.CTkFrame(ventana_padre, corner_radius=0)
    frameBotones.grid(row=1, column=1, columnspan=2, sticky="nsew")
    cargar_botones(ventana_padre, frame)


def cargar_botones(frameBotones, frame):
    global meses
    boton_carga = ctk.CTkButton(frameBotones, text="Seleccionar carpeta de trabajo",
                                 command=lambda: cargar_comunidades(boton_carga, frame))
    boton_carga.grid(row=1, column=1,pady=10, padx=10, sticky="w")
    menu_seleccion_mes = ctk.CTkOptionMenu(frameBotones, values = meses, command= lambda seleccion: print(f"Seleccion {seleccion}"))
    menu_seleccion_mes.grid(row=1, column= 2, pady=10, padx=10, sticky="w")





def principal(ventana_padre):
    global factorX, factorY
    ventana_padre.title("Balance Novafinkas")
    anchoVentana, altoVentana = centrarPantalla(ventana_padre, factorX, factorY)
    print(f"{anchoVentana}x{altoVentana}")
    configurar_regilla(ventana_padre, anchoVentana, altoVentana)

    #centrarPantallaManual(ventana_padre)

    frameLateral = generar_frame_lateral(ventana_padre)
    framePrincipal = generar_frame_principal(ventana_padre)
    frameBotones = generar_frame_botones(ventana_padre, framePrincipal)
    return frameLateral, framePrincipal, frameBotones

'''
Empieza aquí el programa principal
'''


tabla = None
app = ctk.CTk()
frameLateral, framePrincipal, frameBotones = principal(app)
print(tabla)
app.mainloop()
