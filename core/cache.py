import os
import numpy as np


def guardar_rostros_cache(rostros, archivo):
    """
    Guarda los rostros detectados y sus encodings.
    """
    nombres = [d['nombre_archivo'] for d in rostros]
    encodings = np.array([d['encoding'] for d in rostros])
    np.savez(archivo, nombres=nombres, encodings=encodings)
    print(f"[💾] Se guardaron {len(nombres)} rostros en {archivo}")


def cargar_rostros_cache(archivo):
    """
    Carga rostros y encodings previamente guardados.
    """
    if not os.path.exists(archivo):
        print(f"[!] No se encontró el archivo de cache {archivo}")
        return []

    data = np.load(archivo, allow_pickle=True)
    nombres = data['nombres']
    encodings = data['encodings']

    rostros = []
    for nombre, encoding in zip(nombres, encodings):
        rostros.append({
            'nombre_archivo': str(nombre),
            'encoding': encoding
        })
    print(f"[📂] Se cargaron {len(rostros)} rostros desde cache")
    return rostros
