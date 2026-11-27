# test_almacen.py - Pruebas de la HU-07 (guardar y cargar en un archivo JSON)
# Se ejecutan desde la carpeta califiapp con:
#     python -m unittest discover -s tests -v
import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from almacen import guardar_datos, cargar_datos, exportar_csv

# Archivo SOLO para las pruebas: así nunca tocamos los datos reales del grupo.
RUTA_PRUEBA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_prueba.json")
RUTA_CSV_PRUEBA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reporte_prueba.csv")


class HU07GuardarYCargar(unittest.TestCase):

    def tearDown(self):
        # Se ejecuta al terminar CADA prueba: borra el archivo de prueba.
        if os.path.exists(RUTA_PRUEBA):
            os.remove(RUTA_PRUEBA)

    def test_guardar_y_cargar_los_mismos_datos(self):
        alumnos = ["Ana López", "Íñigo Muñoz"]
        calificaciones = {"Ana López": [8.0, 9.5, 10.0]}
        guardar_datos(RUTA_PRUEBA, alumnos, calificaciones)
        datos = cargar_datos(RUTA_PRUEBA)
        self.assertEqual(datos["alumnos"], ["Ana López", "Íñigo Muñoz"])
        self.assertEqual(datos["calificaciones"], {"Ana López": [8.0, 9.5, 10.0]})

    def test_cargar_si_el_archivo_no_existe(self):
        datos = cargar_datos(RUTA_PRUEBA)
        self.assertEqual(datos, {"alumnos": [], "calificaciones": {}})

    def test_cargar_archivo_danado(self):
        with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
            archivo.write("esto no es JSON {")
        self.assertIsNone(cargar_datos(RUTA_PRUEBA))


class HU09ExportarCSV(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(RUTA_CSV_PRUEBA):
            os.remove(RUTA_CSV_PRUEBA)

    def test_exporta_encabezado_y_filas(self):
        filas = [["Beto Díaz", 3.0, 5.0, 4.0, 4.0, "REPROBADO"]]
        self.assertTrue(exportar_csv(RUTA_CSV_PRUEBA, ["Alumno", "Promedio"], filas))
        with open(RUTA_CSV_PRUEBA, "r", encoding="utf-8-sig", newline="") as archivo:
            renglones = list(csv.reader(archivo))
        self.assertEqual(renglones[0], ["Alumno", "Promedio"])
        self.assertEqual(renglones[1], ["Beto Díaz", "3.0", "5.0", "4.0", "4.0", "REPROBADO"])

    def test_el_archivo_lleva_la_marca_para_excel(self):
        exportar_csv(RUTA_CSV_PRUEBA, ["Alumno"], [["Íñigo Muñoz"]])
        with open(RUTA_CSV_PRUEBA, "rb") as archivo:
            primeros_bytes = archivo.read(3)
        self.assertEqual(primeros_bytes, b"\xef\xbb\xbf")
        
if __name__ == "__main__":
    unittest.main(verbosity=2)