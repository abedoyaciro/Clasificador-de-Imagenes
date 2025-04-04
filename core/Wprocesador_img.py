'''
Este script contiene las funciones necesarias para procesar las imágenes de
rostros detectados y codificados.

Funciones:
    agrupar_por_rostros(embeddings, eps=0.5, min_samples=1)
    organizar_imagenes(embeddings, origen='source', destino='processed')

Uso:
    embeddings = [{'nombre_archivo': 'imagen1.jpg',
                    'encoding': [0.1, 0.2, ...]},
                  {'nombre_archivo': 'imagen2.jpg',
                    'encoding': [0.3, 0.4, ...]},
                  ...]
    embeddings = agrupar_por_rostros(embeddings, eps=0.5, min_samples=1)
    organizar_imagenes(embeddings, origen='source', destino='processed')

    El resultado es una carpeta 'processed' con subcarpetas para cada grupo de
    rostros detectados. Dentro de cada subcarpeta se encuentran las imágenes
    renombradas con el nombre del grupo y la imagen original.
'''

import os
import shutil
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN


def cargar_imagenes(carpeta):
    """
    Carga todas las imágenes desde la carpeta indicada.
    Devuelve una lista de tuplas (imagen_cargada, nombre_archivo).
    """
    imagenes = []
    extensiones_validas = ('.jpg', '.jpeg', '.png')

    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(extensiones_validas):
            ruta = os.path.join(carpeta, archivo)
            try:
                imagen = face_recognition.load_image_file(ruta)
                imagenes.append((imagen, archivo))
            except OSError as e:
                print(f"[!] Error al cargar {archivo}: {e}")
    return imagenes


def extraer_rostros(imagenes):
    """
    Detecta rostros y extrae el más grande de cada imagen.
    Devuelve una lista de diccionarios con nombre de archivo y encoding.
    """
    datos_rostros = []

    for imagen, nombre in imagenes:
        ubicaciones = face_recognition.face_locations(imagen)
        codificaciones = face_recognition.face_encodings(imagen, ubicaciones)

        if not codificaciones:
            print(f"[!] No se detectó ningún rostro en: {nombre}")
            continue

        if len(codificaciones) > 1:
            print(
                f"[⚠️] {len(codificaciones)} rostros detectados en: {nombre}"
            )
            # Seleccionar el rostro más grande
            tamaños = [(bottom - top) * (right - left)
                       for top, right, bottom, left in ubicaciones]
            idx_mayor = int(np.argmax(tamaños))
            encoding = codificaciones[idx_mayor]
        else:
            encoding = codificaciones[0]

        datos_rostros.append({
            'nombre_archivo': nombre,
            'encoding': encoding
        })

    return datos_rostros


def agrupar_por_rostros(embeddings, eps=0.5, min_samples=1):
    """
    Agrupa embeddings de rostros con DBSCAN y asigna etiquetas por grupo.
    """
    codificaciones = [d['encoding'] for d in embeddings]

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    etiquetas = clustering.fit_predict(codificaciones)

    for i, etiqueta in enumerate(etiquetas):
        embeddings[i]['grupo'] =\
            f"persona_{etiqueta}" if etiqueta != -1 else "desconocido"

    return embeddings


def organizar_imagenes(embeddings, origen='source', destino='processed'):
    """
    Renombra y mueve las imágenes según el grupo asignado.
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    for persona in set(d['grupo'] for d in embeddings):
        carpeta = os.path.join(destino, persona)
        os.makedirs(carpeta, exist_ok=True)

    for d in embeddings:
        origen_archivo = os.path.join(origen, d['nombre_archivo'])
        nombre_nuevo = f"{d['grupo']}_{d['nombre_archivo']}"
        destino_archivo = os.path.join(destino, d['grupo'], nombre_nuevo)

        try:
            shutil.copy(origen_archivo, destino_archivo)
        except (shutil.Error, OSError) as e:
            print(f"[!] Error al mover {d['nombre_archivo']}: {e}")


def guardar_rostros_cache(rostros, archivo='rostros_cache.npz'):
    """Guarda los rostros detectados y sus encodings."""
    nombres = [d['nombre_archivo'] for d in rostros]
    encodings = np.array([d['encoding'] for d in rostros])
    np.savez(archivo, nombres=nombres, encodings=encodings)
    print(f"[💾] Se guardaron {len(nombres)} rostros en {archivo}")


def cargar_rostros_cache(archivo='rostros_cache.npz'):
    """Carga rostros y encodings previamente guardados."""
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
