import pandas as pd
import tkinter as tk
from tkinter import Tk

from pandastable import Table

# Crear un DataFrame de ejemplo
data = {
    "Nombre": ["Juan", "Ana", "Pedro", "Luisa"],
    "Edad": [28, 34, 45, 23],
    "Ciudad": ["Madrid", "Barcelona", "Sevilla", "Valencia"],
}
df = pd.DataFrame(data)

# Crear la ventana principal de Tkinter
root = Tk()
root.title("Ejemplo de Pandastable")

# Crear un frame para la tabla
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Crear una tabla a partir del DataFrame
table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
table.show()

# Ejecutar el bucle principal de la aplicación
root.mainloop()