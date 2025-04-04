import os
import shutil


def organizar_imagenes(embeddings, origen='data/source',
                       destino='data/processed'):
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
        destino_archivo = os.path.join(destino, d['grupo'],
                                       d['nombre_archivo'])

        try:
            shutil.copy(origen_archivo, destino_archivo)
        except (shutil.Error, OSError) as e:
            print(f"[!] Error al mover {d['nombre_archivo']}: {e}")
