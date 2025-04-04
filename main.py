from core.procesamiento import cargar_imagenes, extraer_rostros
from core.organizacion import organizar_imagenes
from interface.clasificador import flujo_interactivo_de_clasificacion

USAR_CACHE = True
RUTA_CACHE = "data/rostros_cache.npz"


def main():
    '''
    if USAR_CACHE and os.path.exists(RUTA_CACHE):
        rostros = cargar_rostros_cache(RUTA_CACHE)
    else:
    '''
    imagenes = cargar_imagenes("data/source")
    rostros = extraer_rostros(imagenes)
    '''
    guardar_rostros_cache(rostros, RUTA_CACHE)
    '''
    clasificaciones = flujo_interactivo_de_clasificacion(rostros)

    # Actualizar etiquetas en los embeddings
    for r in rostros:
        archivo = r['nombre_archivo']
        if archivo in clasificaciones:
            r['grupo'] = clasificaciones[archivo]["nombre"]

    organizar_imagenes(rostros, origen="data/source", destino="data/processed")


if __name__ == "__main__":
    main()
