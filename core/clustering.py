from sklearn.cluster import DBSCAN


def agrupar_por_rostros(embeddings, eps=0.5, min_samples=3):
    """
    Agrupa embeddings de rostros con DBSCAN y asigna etiquetas por grupo.
    """
    codificaciones = [d['encoding'] for d in embeddings]

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    etiquetas = clustering.fit_predict(codificaciones)

    for i, etiqueta in enumerate(etiquetas):
        embeddings[i]['grupo'] = (
            f"persona_{etiqueta}" if etiqueta != -1 else "desconocido"
        )

    return embeddings
