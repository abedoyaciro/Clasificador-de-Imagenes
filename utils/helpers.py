import os
import json


def confirmacion_binaria(pregunta):
    """
    Pregunta al usuario '¿s/n?' y repite hasta obtener una respuesta válida.
    Devuelve True si responde 's', False si responde 'n'.
    """
    while True:
        respuesta = input(pregunta + " (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"


def cargar_json_seguro(path):
    """
    Carga un archivo JSON si existe, o devuelve un diccionario vacío.
    """
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json_seguro(data, path):
    """
    Guarda un diccionario como archivo JSON con indentación.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
