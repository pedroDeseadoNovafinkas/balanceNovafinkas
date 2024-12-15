import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import xlrd
import glob
import pandas as pd


import tkinter as tk
from comunidades import *



def centrarPantalla(windows, factor):
    anchoPantalla = windows.winfo_screenwidth()
    altoPantalla = windows.winfo_screenheight()
    anchoVentana = int(anchoPantalla * factor)
    altoVentana = int(altoPantalla * factor)
    x = int((anchoPantalla - anchoVentana) /2)
    y = int((altoPantalla - altoVentana) /2)
    windows.geometry(f'{anchoVentana}x{altoVentana}+{x}+{y}')





app = ctk.CTk()
app.title("Balance Novafinkas")
centrarPantalla(app, 0.85)

app.grid_rowconfigure(0, weight=19)  # Primera fila (90% del alto)
app.grid_rowconfigure(1, weight=1)  # Segunda fila (10% del alto)
app.grid_columnconfigure(0, weight=1)  # Primera columna (20% del ancho)
app.grid_columnconfigure(1, weight=9)  # Segunda columna (80% del ancho)

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
'''
boton_cargar = ctk.CTkButton(frameBotones, text="Seleccionar carpeta de trabajo",
                             command=seleccionar_carpeta).pack(pady=5, padx=10, anchor="w")
'''
app.mainloop()
