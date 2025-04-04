import numpy as np
from sklearn.metrics import pairwise_distances

from procesador_img import (
    cargar_imagenes,
    extraer_rostros,
    agrupar_por_rostros,
    organizar_imagenes
)


def analizar_distancias(embeddings):
    """
    Calcula y analiza las distancias entre embeddings.
    """
    codificaciones = [d['encoding'] for d in embeddings]
    distancias = pairwise_distances(codificaciones, metric='euclidean')

    # Análisis básico de las distancias
    print("Distancia mínima:", np.min(distancias))
    print("Distancia máxima:", np.max(distancias))
    print("Distancia promedio:", np.mean(distancias))
    print("Desviación estándar de las distancias:", np.std(distancias))

    # Puedes agregar análisis más detallados, como histogramas de distancias
    # para visualizar la distribución.

    return distancias


imagenes = cargar_imagenes("source")

embeddings = extraer_rostros(imagenes)

# Uso de la función
distancias = analizar_distancias(embeddings)

print("Distancias entre embeddings calculadas.")
print(distancias)
