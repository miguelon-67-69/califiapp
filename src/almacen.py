# almacen.py - Guardar y cargar los datos de CalifiApp (HU-07)
# Es el ÚNICO archivo de CalifiApp que toca el disco.
import csv
import json
import os

# La ruta se arma desde la carpeta de este archivo (src), no desde
# la carpeta donde abriste PowerShell: así siempre encuentra data/.
CARPETA_SRC = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(CARPETA_SRC, "..", "data", "califiapp.json")
RUTA_REPORTE  = os.path.join(CARPETA_SRC, "..", "data", "reporte_grupo.csv")

def datos_vacios():
    return {"alumnos": [], "calificaciones": {}}


def guardar_datos(ruta, alumnos, calificaciones):
    datos = {"alumnos": alumnos, "calificaciones": calificaciones}
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return datos_vacios()
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        return None
    
    
    # HU-09 Exportar el reporte a CSV (Excel lo abre con doble clic)
def exportar_csv(ruta, encabezado, filas):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    try:
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezado)
            escritor.writerows(filas)
        return True
    except PermissionError:
        return False