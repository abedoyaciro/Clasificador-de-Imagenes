import os
import face_recognition
import numpy as np

from utils.helpers import cargar_json_seguro, guardar_json_seguro


RUTA_JSON = "data/clasificaciones.json"


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
    Marca en el JSON las imágenes sin rostro para no reprocesarlas.
    """
    datos_rostros = []
    clasificaciones = cargar_json_seguro(RUTA_JSON)

    for imagen, nombre in imagenes:
        # 👀 Saltar si ya fue procesada (con rostro o marcada como sin rostro)
        if nombre in clasificaciones:
            print(f"[↪] Ya procesada anteriormente: {nombre}")
            continue

        ubicaciones = face_recognition.face_locations(imagen)
        codificaciones = face_recognition.face_encodings(imagen, ubicaciones)

        if not codificaciones:
            print(f"[!] No se detectó ningún rostro en: {nombre}")
            clasificaciones[nombre] = {
                "nombre": "pendiente",
                "motivo": "no_se_detecto_rostro"
            }
            continue

        if len(codificaciones) > 1:
            print(
                f"[⚠️] {len(codificaciones)} rostros detectados en: {nombre}"
            )
            tamaños = [
                (bottom - top) * (right - left)
                for top, right, bottom, left in ubicaciones
            ]
            idx_mayor = int(np.argmax(tamaños))
            encoding = codificaciones[idx_mayor]
        else:
            encoding = codificaciones[0]

        datos_rostros.append({
            'nombre_archivo': nombre,
            'encoding': encoding
        })

    # Guardar clasificaciones actualizadas solo si hubo nuevas
    if datos_rostros:
        guardar_json_seguro(clasificaciones, RUTA_JSON)

    return datos_rostros
