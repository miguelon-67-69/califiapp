LIMITE_ALUMNOS = 30
MINIMA_APROBATORIA = 6

# calificaciones.py - Lógica de CalifiApp (una función por criterio)
# Cada función responde a un criterio de aceptación de las HU-01 a HU-04.


# HU-01 Registrar alumnos
def nombre_repetido(alumnos, nombre):
   return buscar_alumno(alumnos, nombre) is not None

def registrar_alumno(alumnos, nombre):
    nombre = nombre.strip()
    if nombre == "" or len(alumnos) >= LIMITE_ALUMNOS:
        return False
    if nombre_repetido(alumnos, nombre):
        return False
    alumnos.append(nombre)
    return True


# HU-02 Capturar calificaciones
def validar_calificacion(texto):
    try:
        calificacion = float(texto)
    except ValueError:
        return None
    if calificacion < 0 or calificacion > 10:
        return None
    return calificacion


# HU-03 Calcular promedio y estatus
def calcular_promedio(calificaciones):
    return round(sum(calificaciones) / len(calificaciones), 1)


def obtener_estatus(promedio):
    if promedio >= MINIMA_APROBATORIA:
        return "APROBADO"
    return "REPROBADO"


# HU-04 Mostrar reporte del grupo
def fila_reporte(nombre, promedio):
    return nombre + " | " + str(promedio) + " | " + obtener_estatus(promedio)


def promedio_grupal(promedios):
    if len(promedios) == 0:
        return 0.0
    return round(sum(promedios) / len(promedios), 1)


# MU-05 Ver la lista del grupo

def lista_ordenada(alumnos):
    return sorted(alumnos, key=str.lower)

def linea_lista(numero, nombre):
    return str(numero) + ". " + nombre

# HU-06 Consultar a un alumno
def buscar_alumno(alumnos, nombre):
    nombre = nombre.strip().lower()
    for registrado in alumnos:
        if registrado.lower() == nombre:
            return registrado
    return None


# HU-02 (defecto del Sprint 2): capturar solo a los que faltan
def alumnos_sin_calificar(alumnos, calificaciones):
    pendientes = []
    for nombre in alumnos:
        if nombre not in calificaciones:
            pendientes.append(nombre)
    return pendientes


# HU-08 Ver alumnos en riesgo
def promedio_de(pareja):
    return pareja[1]


def alumnos_en_riesgo(calificaciones):
    en_riesgo = []
    for nombre in calificaciones:
        promedio = calcular_promedio(calificaciones[nombre])
        if promedio < MINIMA_APROBATORIA:
            en_riesgo.append((nombre, promedio))
    return sorted(en_riesgo, key=promedio_de)

# HU-09 Exportar el reporte a CSV
ENCABEZADO_REPORTE = ["Alumno", "Parcial 1", "Parcial 2", "Parcial 3", "Promedio", "Estatus"]


def promedio_de_fila(fila):
    return fila[4]


def filas_reporte(calificaciones):
    filas = []
    for nombre in calificaciones:
        parciales = calificaciones[nombre]
        promedio = calcular_promedio(parciales)
        fila = [nombre] + parciales + [promedio, obtener_estatus(promedio)]
        filas.append(fila)
    return sorted(filas, key=promedio_de_fila)


# HU-10 Estadísticas del grupo
def porcentaje_aprobacion(aprobados, total):
    if total == 0:
        return 0.0
    return round(aprobados * 100 / total, 1)


def estadisticas(calificaciones):
    filas = filas_reporte(calificaciones)
    promedios = []
    aprobados = 0
    for fila in filas:
        promedios.append(fila[4])
        if fila[5] == "APROBADO":
            aprobados = aprobados + 1
    return {
        "total": len(filas),
        "aprobados": aprobados,
        "reprobados": len(filas) - aprobados,
        "porcentaje": porcentaje_aprobacion(aprobados, len(filas)),
        "promedio_grupal": promedio_grupal(promedios),
        "mas_bajo": [filas[0][0], filas[0][4]],
        "mas_alto": [filas[-1][0], filas[-1][4]],
    }