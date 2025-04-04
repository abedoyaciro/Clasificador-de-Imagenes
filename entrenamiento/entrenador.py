import os
import numpy as np
import face_recognition
from core.caracteristicas import extraer_embedding_visual


def reconstruir_base_entrenada(clasificaciones, rostros=None,
                               carpeta="data/source"):
    '''
    Reconstruye la base entrenada a partir de clasificaciones y encodings.

    Si no se proporcionan rostros, carga imágenes del disco y extrae los
    encodings de las que estén clasificadas y tengan rostro.

    Args:
        clasificaciones: Diccionario con las clasificaciones.
        rostros: (opcional) Lista de rostros extraídos.
        carpeta: Carpeta donde se encuentran las imágenes.

    Returns:
        base_entrenada: Lista de diccionarios con nombre, encoding promedio e
        imágenes.
    '''
    base = {}

    if rostros:
        # ✅ Usar directamente los rostros extraídos
        for item in rostros:
            nombre_archivo = item['nombre_archivo']
            if nombre_archivo not in clasificaciones:
                continue
            nombre = clasificaciones[nombre_archivo]['nombre']
            encoding = item['encoding']
            if nombre not in base:
                base[nombre] = {'encodings': [], 'imagenes': []}
            base[nombre]['encodings'].append(encoding)
            base[nombre]['imagenes'].append(nombre_archivo)
    else:
        # 🔄 Extraer desde cero si no hay rostros proporcionados
        for archivo, info in clasificaciones.items():
            if info['nombre'] == 'pendiente':
                continue

            ruta = os.path.join(carpeta, archivo)
            if not os.path.exists(ruta):
                continue

            imagen = face_recognition.load_image_file(ruta)
            ubicaciones = face_recognition.face_locations(imagen)
            codificaciones = face_recognition.face_encodings(
                imagen, ubicaciones
            )

            if not codificaciones:
                continue

            # Si hay más de un rostro, usar el más grande
            if len(codificaciones) > 1:
                tamaños = [(b - t) * (r - l) for t, r, b, l in ubicaciones]
                idx = int(np.argmax(tamaños))
                encoding = codificaciones[idx]
            else:
                encoding = codificaciones[0]

            nombre = info['nombre']
            if nombre not in base:
                base[nombre] = {'encodings': [], 'imagenes': []}
            base[nombre]['encodings'].append(encoding)
            base[nombre]['imagenes'].append(archivo)

    # Convertir al formato final
    base_entrenada = []
    for nombre, datos in base.items():
        promedio = np.mean(datos['encodings'], axis=0)
        base_entrenada.append({
            'nombre': nombre,
            'encoding': promedio,
            'imagenes': datos['imagenes']
        })

    print(
        f"[📚] Base entrenada reconstruida con {len(base_entrenada)} personas."
    )
    return base_entrenada


def reconstruir_base_visual(clasificaciones, carpeta="data/source"):
    base = {}

    for archivo, info in clasificaciones.items():
        if info.get("nombre") == "pendiente":
            continue  # Saltar los aún no clasificados

        path_img = os.path.join(carpeta, archivo)
        if not os.path.exists(path_img):
            continue

        emb = extraer_embedding_visual(path_img)
        nombre = info["nombre"]

        if nombre not in base:
            base[nombre] = {"vectores": [], "imagenes": []}

        base[nombre]["vectores"].append(emb)
        base[nombre]["imagenes"].append(archivo)

    # Tomar el vector promedio por persona
    base_final = []
    for nombre, datos in base.items():
        promedio = np.mean(datos["vectores"], axis=0)
        base_final.append({
            "nombre": nombre,
            "embedding_visual": promedio,
            "imagenes": datos["imagenes"]
        })

    print(f"[🔁] Base visual reconstruida con {len(base_final)} personas.")
    return base_final
