#Con este script creo comunidades en un fichero.

import pandas as pd
import xlrd
import glob

directorio = r"C:\Users\Pedro Novafinkas\OneDrive\PEDRO\Balances\2024\11. Noviembre"
archivos_excel = glob.glob(f"{directorio}\\*.xls")

for ruta_archivo in archivos_excel:
    workbook = xlrd.open_workbook(ruta_archivo)
    hoja = workbook.sheet_by_index(0)
    celda = hoja.cell_value(rowx=5, colx=1)




