# test_almacen.py - Pruebas de la HU-07 (guardar y cargar en un archivo JSON)
# Se ejecutan desde la carpeta califiapp con:
#     python -m unittest discover -s tests -v
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from almacen import guardar_datos, cargar_datos

# Archivo SOLO para las pruebas: así nunca tocamos los datos reales del grupo.
RUTA_PRUEBA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_prueba.json")


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


if __name__ == "__main__":
    unittest.main(verbosity=2)