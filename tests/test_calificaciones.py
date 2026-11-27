# test_calificaciones.py - Cada criterio de aceptación es una prueba
# Se ejecutan desde la carpeta califiapp con:
#     python -m unittest discover -s tests -v
import os
import sys
import unittest

# Permite importar src/calificaciones.py aunque las pruebas vivan en tests/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from calificaciones import *


class HU01RegistrarAlumnos(unittest.TestCase):

    def test_registrar_alumno_valido(self):
        alumnos = []
        self.assertTrue(registrar_alumno(alumnos, "Ana López"))
        self.assertEqual(alumnos, ["Ana López"])

    def test_no_registrar_nombre_vacio(self):
        alumnos = []
        self.assertFalse(registrar_alumno(alumnos, "   "))
        self.assertEqual(len(alumnos), 0)

    def test_limite_30_alumnos(self):
        alumnos = ["Alumno"] * 30
        self.assertFalse(registrar_alumno(alumnos, "Luis"))
        self.assertEqual(len(alumnos), 30)

    def test_no_registrar_nombre_repetido(self):
            alumnos = ["Ana López"]
            self.assertFalse(registrar_alumno(alumnos, "Ana López"))
            self.assertFalse(registrar_alumno(alumnos, "ana lópez"))
            self.assertEqual(len(alumnos), 1)

class HU02CapturarCalificaciones(unittest.TestCase):

    def test_calificacion_valida(self):
        self.assertEqual(validar_calificacion("8.5"), 8.5)
        self.assertEqual(validar_calificacion("0"), 0)
        self.assertEqual(validar_calificacion("10"), 10)

    def test_calificacion_fuera_de_rango(self):
        self.assertIsNone(validar_calificacion("11"))
        self.assertIsNone(validar_calificacion("-1"))

    def test_calificacion_no_numerica(self):
        self.assertIsNone(validar_calificacion("ocho"))


class HU03PromedioYEstatus(unittest.TestCase):

    def test_promedio_un_decimal(self):
        self.assertEqual(calcular_promedio([7, 8, 8]), 7.7)

    def test_estatus_aprobado_en_6(self):
        self.assertEqual(obtener_estatus(6.0), "APROBADO")

    def test_estatus_reprobado(self):
        self.assertEqual(obtener_estatus(5.9), "REPROBADO")


class HU04ReporteDelGrupo(unittest.TestCase):

    def test_fila_reporte(self):
        self.assertEqual(fila_reporte("Ana", 8.0), "Ana | 8.0 | APROBADO")

    def test_promedio_grupal(self):
        self.assertEqual(promedio_grupal([8.0, 6.0, 7.0]), 7.0)

    def test_promedio_grupal_sin_alumnos(self):
        self.assertEqual(promedio_grupal([]), 0.0)



class HU05ListaDelGrupo(unittest.TestCase):

    def test_lista_en_orden_alfabetico(self):
        alumnos = ["Luis Pérez", "Ana López", "Carla Ruiz"]
        self.assertEqual(lista_ordenada(alumnos), ["Ana López", "Carla Ruiz", "Luis Pérez"])

    def test_lista_original_no_cambia(self):
        alumnos = ["Luis Pérez", "Ana López"]
        lista_ordenada(alumnos)
        self.assertEqual(alumnos, ["Luis Pérez", "Ana López"])

    def test_linea_de_la_lista(self):
        self.assertEqual(linea_lista(1, "Ana López"), "1. Ana López")
        
        
class HU06ConsultarAlumno(unittest.TestCase):

    def test_buscar_sin_importar_mayusculas(self):
        alumnos = ["Ana López", "Luis Pérez"]
        self.assertEqual(buscar_alumno(alumnos, " luis pérez "), "Luis Pérez")

    def test_buscar_alumno_que_no_existe(self):
        self.assertIsNone(buscar_alumno(["Ana López"], "Pedro"))
        

class HU02DefectoCapturaRepetida(unittest.TestCase):

    def test_solo_los_que_no_tienen_calificaciones(self):
        alumnos = ["Ana López", "Luis Pérez", "Carla Ruiz"]
        calificaciones = {"Ana López": [8.0, 9.0, 10.0]}
        self.assertEqual(alumnos_sin_calificar(alumnos, calificaciones),
                         ["Luis Pérez", "Carla Ruiz"])

    def test_todos_calificados_regresa_lista_vacia(self):
        alumnos = ["Ana López"]
        calificaciones = {"Ana López": [8.0, 9.0, 10.0]}
        self.assertEqual(alumnos_sin_calificar(alumnos, calificaciones), [])
        
        
class HU08AlumnosEnRiesgo(unittest.TestCase):

    def test_solo_aparecen_los_reprobados(self):
        calificaciones = {"Ana López": [8.0, 8.0, 8.0],
                          "Luis Pérez": [5.0, 5.0, 6.0]}
        self.assertEqual(alumnos_en_riesgo(calificaciones), [("Luis Pérez", 5.3)])

    def test_del_promedio_mas_bajo_al_mas_alto(self):
        calificaciones = {"Carla Ruiz": [5.0, 5.0, 5.0],
                          "Beto Díaz": [2.0, 3.0, 4.0]}
        self.assertEqual(alumnos_en_riesgo(calificaciones),
                         [("Beto Díaz", 3.0), ("Carla Ruiz", 5.0)])

    def test_nadie_en_riesgo(self):
        calificaciones = {"Ana López": [6.0, 6.0, 6.0]}
        self.assertEqual(alumnos_en_riesgo(calificaciones), [])
        
        
class HU09FilasDelReporte(unittest.TestCase):

    def test_cada_fila_tiene_seis_columnas(self):
        calificaciones = {"Ana López": [8.0, 9.0, 10.0]}
        self.assertEqual(filas_reporte(calificaciones),
                         [["Ana López", 8.0, 9.0, 10.0, 9.0, "APROBADO"]])

    def test_filas_de_menor_a_mayor_promedio(self):
        calificaciones = {"Carla Ruiz": [9.0, 10.0, 9.5],
                          "Beto Díaz": [3.0, 5.0, 4.0]}
        filas = filas_reporte(calificaciones)
        self.assertEqual(filas[0][0], "Beto Díaz")
        self.assertEqual(filas[1][0], "Carla Ruiz")
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
