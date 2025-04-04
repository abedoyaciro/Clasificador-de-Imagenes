import os
from utils.helpers import cargar_json_seguro, guardar_json_seguro
from entrenamiento.entrenador import reconstruir_base_visual
from core.caracteristicas import extraer_embedding_visual
from interface.validador import validar_y_etiquetar
import numpy as np

RUTA_JSON = "data/clasificaciones.json"
CARPETA_IMAGENES = "data/source"
UMBRAL_VISUAL_SEGURO = 0.4
UMBRAL_VISUAL_DUDA = 0.6


def comparar_visualmente(embedding, base):
    if not base:
        return None, None

    distancias = [
        np.linalg.norm(embedding - persona["embedding_visual"])
        for persona in base
    ]
    idx_min = int(np.argmin(distancias))
    return base[idx_min], distancias[idx_min]


def main():
    clasificaciones = cargar_json_seguro(RUTA_JSON)

    # Filtrar imágenes sin rostro (marcadas como pendientes)
    pendientes = [
        img for img, info in clasificaciones.items()
        if info.get("nombre") == "pendiente"
        and info.get("motivo") == "no_se_detecto_rostro"
    ]

    if not pendientes:
        print("[✅] No hay imágenes pendientes por clasificar visualmente.")
        return

    base_visual = reconstruir_base_visual(
        clasificaciones, carpeta=CARPETA_IMAGENES
    )

    for archivo in pendientes:
        ruta = os.path.join(CARPETA_IMAGENES, archivo)

        if not os.path.exists(ruta):
            print(f"[⚠️] Archivo no encontrado: {archivo}")
            continue

        emb = extraer_embedding_visual(ruta)
        mejor_match, distancia = comparar_visualmente(emb, base_visual)

        print(f"\n📷 Clasificando visualmente: {archivo}")
        if mejor_match and distancia < UMBRAL_VISUAL_SEGURO:
            nombre = mejor_match["nombre"]
            print(f"[AUTO] Clasificado como: {nombre}")
        elif mejor_match and distancia < UMBRAL_VISUAL_DUDA:
            nombre = validar_y_etiquetar(
                emb, archivo, base_visual, tipo='visual'
            )
        else:
            nombre = validar_y_etiquetar(
                emb, archivo, base_visual, tipo='visual')

        clasificaciones[archivo] = {
            "nombre": nombre,
            "motivo": "clasificacion_visual"
        }

    guardar_json_seguro(clasificaciones, RUTA_JSON)
    print("\n[✔] Clasificación visual finalizada.")


if __name__ == "__main__":
    main()
