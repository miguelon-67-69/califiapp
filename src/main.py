# ==============================================================
#  Proyecto Scrum: "CalifiApp" - Control de calificaciones
#  Submódulo 2: Aplica metodologías ágiles para el desarrollo de software
#  CBTIS 200 - 3AM PGR
#
#  Versión del Sprint 2 (Práctica guiada 9): HU-01 a HU-08.
#  La lógica vive en calificaciones.py, el disco solo lo toca
#  almacen.py (26 pruebas en total); aquí solo está el menú.
#  Ejecútalo desde la carpeta califiapp con:  python src/main.py
#
#  Organización (una función por historia de usuario):
#    opcion_registrar()  -> HU-01     opcion_capturar()  -> HU-02
#    opcion_promedios()  -> HU-03     opcion_reporte()   -> HU-04
#    opcion_lista()      -&gt; HU-05     opcion_consultar() -&gt; HU-06
#    iniciar_datos() y guardar()      -&gt; HU-07
#    opcion_riesgo()     -&gt; HU-08
#  El menú principal, main(), llama a cada una según la opción.
# ==============================================================

from calificaciones import (LIMITE_ALUMNOS, registrar_alumno, validar_calificacion, nombre_repetido,
                            calcular_promedio, obtener_estatus, fila_reporte,
                            promedio_grupal, lista_ordenada, linea_lista,
                            buscar_alumno,alumnos_sin_calificar,
                            alumnos_en_riesgo, ENCABEZADO_REPORTE, filas_reporte,
                            estadisticas)

from almacen import RUTA_DATOS, guardar_datos, cargar_datos, RUTA_REPORTE, exportar_csv

NOMBRE_APP = "CalifiApp"
OBJETIVO = "Registrar y consultar las calificaciones de un grupo desde la consola"
PARCIALES = 3

alumnos = []          # HU-01: nombres de los alumnos del grupo
calificaciones = {}   # HU-02: nombre -> [parcial 1, parcial 2, parcial 3]


# HU-01 Registrar alumnos
def opcion_registrar():
    print("\nREGISTRAR ALUMNOS (deja el nombre vacío para terminar)")
    while True:
        nombre = input("Nombre del alumno: ")
        if nombre.strip() == "":
            break
        if nombre_repetido(alumnos, nombre):
            print("Ese alumno ya está registrado. Escribe otro nombre.")
        elif registrar_alumno(alumnos, nombre):
            print("  Registrado. Total:", len(alumnos), "de", LIMITE_ALUMNOS)
        else:
            print("  No se pudo registrar: el grupo ya tiene", LIMITE_ALUMNOS, "alumnos.")
            break


# HU-02 Capturar calificaciones
def opcion_capturar():
    if len(alumnos) == 0:
        print("\nPrimero registra alumnos (opción 1).")
        return
    pendientes = alumnos_sin_calificar(alumnos, calificaciones)
    if len(pendientes) == 0:
        print("\nTodos los alumnos ya tienen sus calificaciones.")
        return
    print("\nCAPTURAR CALIFICACIONES (de 0 a 10)")
    for nombre in pendientes:
        parciales = []
        print("Alumno:", nombre)
        while len(parciales) < PARCIALES:
            texto = input("  Parcial " + str(len(parciales) + 1) + ": ")
            calificacion = validar_calificacion(texto)
            if calificacion is None:
                print("  Calificación no válida. Escribe un número de 0 a 10.")
            else:
                parciales.append(calificacion)
        calificaciones[nombre] = parciales
# Refactorización (PG7): un solo lugar calcula los promedios del grupo.
# Regresa una lista de parejas (nombre, promedio) de los alumnos
# que ya tienen calificaciones. La usan HU-03 y HU-04.
def promedios_del_grupo():
    resultado = []
    for nombre in alumnos:
        if nombre in calificaciones:
            promedio = calcular_promedio(calificaciones[nombre])
            resultado.append((nombre, promedio))
    return resultado


# HU-03 Calcular promedio y estatus
def opcion_promedios():
    if len(calificaciones) == 0:
        print("\nPrimero captura calificaciones (opción 2).")
        return
    print("\nPROMEDIO Y ESTATUS")
    for nombre, promedio in promedios_del_grupo():
        print(" ", nombre, "->", promedio, obtener_estatus(promedio))


# HU-04 Mostrar reporte del grupo
def opcion_reporte():
    if len(calificaciones) == 0:
        print("\nPrimero captura calificaciones (opción 2).")
        return
    print("\nREPORTE DEL GRUPO")
    print("-" * 50)
    print("Alumno | Promedio | Estatus")
    print("-" * 50)
    promedios = []
    for nombre, promedio in promedios_del_grupo():
        promedios.append(promedio)
        print(fila_reporte(nombre, promedio))
    print("-" * 50)
    print("Promedio grupal:", promedio_grupal(promedios))
    print("Total de alumnos en el reporte:", len(promedios))
    
    
 
 
    # HU-05 Ver la lista del grupo
def opcion_lista():
    if len(alumnos) == 0:
        print("\nAún no hay alumnos registrados (opción 1).")
        return
    print("\nLISTA DEL GRUPO (orden alfabético)")
    print("-" * 50)
    numero = 1
    for nombre in lista_ordenada(alumnos):
        print(linea_lista(numero, nombre))
        numero = numero + 1
    print("-" * 50)
    print("Total:", len(alumnos), "de", LIMITE_ALUMNOS, "alumnos")
    
    
# HU-06 Consultar a un alumno
def opcion_consultar():
    if len(alumnos) == 0:
        print("\nAún no hay alumnos registrados (opción 1).")
        return
    texto = input("\nNombre del alumno a consultar: ")
    nombre = buscar_alumno(alumnos, texto)
    if nombre is None:
        print(" No encontré a", texto.strip(), "en el grupo. Revisa la lista (opción 5).")
        return
    print("\nCONSULTA DE", nombre)
    if nombre not in calificaciones:
        print(" Aún no tiene calificaciones (opción 2).")
        return
    parciales = calificaciones[nombre]
    numero = 1
    for calificacion in parciales:
        print(" Parcial " + str(numero) + " : " + str(calificacion))
        numero = numero + 1
    promedio = calcular_promedio(parciales)
    print(" Promedio:", promedio, obtener_estatus(promedio))


# HU-08 Ver alumnos en riesgo
def opcion_riesgo():
    if len(calificaciones) == 0:
        print("\nPrimero captura calificaciones (opción 2).")
        return
    print("\nALUMNOS EN RIESGO (promedio menor a 6)")
    print("-" * 50)
    en_riesgo = alumnos_en_riesgo(calificaciones)
    for nombre, promedio in en_riesgo:
        print(fila_reporte(nombre, promedio))
    if len(en_riesgo) == 0:
        print("Nadie está en riesgo. ¡Todos aprueban!")
    print("-" * 50)
    print("En riesgo:", len(en_riesgo), "de", len(calificaciones), "alumnos con calificaciones")


# HU-09 Exportar el reporte a CSV
def opcion_exportar():
    if len(calificaciones) == 0:
        print("\nPrimero captura calificaciones (opción 2).")
        return
    filas = filas_reporte(calificaciones)
    if exportar_csv(RUTA_REPORTE, ENCABEZADO_REPORTE, filas):
        print("\nReporte exportado a data/reporte_grupo.csv con", len(filas), "alumnos.")
        print("Ábrelo con doble clic: se abre en Excel.")
    else:
        print("\nNo se pudo exportar: cierra reporte_grupo.csv en Excel y vuelve a intentar.")


# HU-10 Estadísticas del grupo
def opcion_estadisticas():
    if len(calificaciones) == 0:
        print("\nPrimero captura calificaciones (opción 2).")
        return
    datos = estadisticas(calificaciones)
    print("\nESTADÍSTICAS DEL GRUPO")
    print("-" * 50)
    print("Alumnos con calificaciones:", datos["total"])
    print("Aprobados:", datos["aprobados"], "  Reprobados:", datos["reprobados"])
    print("Porcentaje de aprobación:", datos["porcentaje"], "%")
    print("Promedio grupal:", datos["promedio_grupal"])
    print("Promedio más alto:", datos["mas_alto"][0], "con", datos["mas_alto"][1])
    print("Promedio más bajo:", datos["mas_bajo"][0], "con", datos["mas_bajo"][1])
    print("-" * 50)


# HU-07 Guardar y cargar los datos
def guardar():
    guardar_datos(RUTA_DATOS, alumnos, calificaciones)
    print("  (Datos guardados en data/califiapp.json)")


def iniciar_datos():
    datos = cargar_datos(RUTA_DATOS)
    if datos is None:
        print("¡Cuidado! data/califiapp.json está dañado. CalifiApp inicia vacía.")
        return
    alumnos.extend(datos["alumnos"])
    calificaciones.update(datos["calificaciones"])
    print("Se cargaron", len(alumnos), "alumnos de data/califiapp.json")
    

# ==============================================================
#  Menú principal
# ==============================================================
def main():
    iniciar_datos()
    opcion = ""
    while opcion != "0":
        print()
        print("=" * 50)
        print("  " + NOMBRE_APP + " - " + OBJETIVO)
        print("=" * 50)
        print("  1. Registrar alumnos             (HU-01)")
        print("  2. Capturar calificaciones       (HU-02)")
        print("  3. Calcular promedio y estatus   (HU-03)")
        print("  4. Mostrar reporte del grupo     (HU-04)")
        print("  5. Ver lista del grupo           (HU-05)")
        print("  6. Consultar a un alumno         (HU-06)")
        print("  7. Ver alumnos en riesgo         (HU-08)")
        print("  8. Exportar reporte a Excel      (HU-09)")
        print("  9. Estadísticas del grupo        (HU-10)")
        print("  0. Salir")
        print("-" * 50)

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            opcion_registrar()
            guardar()
        elif opcion == "2":
            opcion_capturar()
            guardar()
        elif opcion == "3":
            opcion_promedios()
        elif opcion == "4":
            opcion_reporte()
        elif opcion == "5":
            opcion_lista()
        elif opcion == "6":
            opcion_consultar()
        elif opcion == "7":
            opcion_riesgo()
        elif opcion == "8":
            opcion_exportar()
        elif opcion == "9":
            opcion_estadisticas()
        elif opcion == "0":
            print("Gracias por usar " + NOMBRE_APP + ". ¡Hasta pronto!")
        else:
            print("\nOpción no válida. Escribe un número del 0 al 9.")

        if opcion != "0":
            input("\nPresiona ENTER para volver al menú...")


if __name__ == "__main__":
    main()
