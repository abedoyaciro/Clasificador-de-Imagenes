import os
from entrenamiento.entrenador import reconstruir_base_entrenada
from interface.validador import validar_y_etiquetar
from utils.helpers import cargar_json_seguro, guardar_json_seguro

RUTA_JSON = "data/clasificaciones.json"


def guardar_clasificaciones(clasificaciones):
    guardar_json_seguro(clasificaciones, RUTA_JSON)
    print(f"[💾] Clasificaciones guardadas en {RUTA_JSON}")


def cargar_clasificaciones():
    if not os.path.exists(RUTA_JSON):
        return {}
    return cargar_json_seguro(RUTA_JSON)


def flujo_interactivo_de_clasificacion(rostros):
    clasificaciones = cargar_clasificaciones()
    base_entrenada = reconstruir_base_entrenada(clasificaciones, rostros)
    nuevas_etiquetas = 0

    for rostro in rostros:
        nombre_archivo = rostro['nombre_archivo']
        encoding = rostro['encoding']
        if nombre_archivo in clasificaciones:
            continue

        nombre = validar_y_etiquetar(encoding, nombre_archivo, base_entrenada)

        clasificaciones[nombre_archivo] = {"nombre": nombre}
        nuevas_etiquetas += 1

        if nuevas_etiquetas % 5 == 0:
            base_entrenada = reconstruir_base_entrenada(clasificaciones,
                                                        rostros)

    guardar_clasificaciones(clasificaciones)
    return clasificaciones
