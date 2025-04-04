import os
import numpy as np
from utils.helpers import confirmacion_binaria
from utils.visor import mostrar_imagen

UMBRAL_SEGURO = 0.5
UMBRAL_DUDA = 0.6


def comparar_con_base(encoding, base, tipo='facial'):
    """
    Compara un encoding (facial o visual) con la base correspondiente.
    """
    if not base:
        return None, None

    campo = 'encoding' if tipo == 'facial' else 'embedding_visual'
    distancias = [
        np.linalg.norm(encoding - persona[campo])
        for persona in base
    ]
    idx_min = int(np.argmin(distancias))
    return base[idx_min], distancias[idx_min]


def validar_y_etiquetar(
    encoding, nombre_archivo, base_entrenada, tipo='facial'
):
    imagen_path = os.path.join("data/source", nombre_archivo)
    mostrar_imagen(imagen_path)

    mejor_match, distancia = comparar_con_base(encoding, base_entrenada,
                                               tipo=tipo)

    if tipo == 'visual':
        print(
            "[🔍] Clasificación basada en características visuales "
            "(ropa, postura...)"
        )
    else:
        print("[🧠] Clasificación basada en rostro detectado")

    if mejor_match and distancia < UMBRAL_SEGURO:
        nombre = mejor_match['nombre']
        print(f"[AUTO] Clasificado como: {nombre} "
              f"(distancia: {distancia:.3f})")
        return nombre

    elif mejor_match and distancia < UMBRAL_DUDA:
        print(
            f"[❓] Posible coincidencia: {mejor_match['nombre']} "
            f"(distancia: {distancia:.3f})"
        )
        if confirmacion_binaria("[]] ¿Es correcto?"):
            return mejor_match['nombre']

    print("Personas existentes:")
    for i, persona in enumerate(base_entrenada):
        print(f"{i + 1}. {persona['nombre']}")
    entrada = input("Escribe nombre o número (ENTER para nueva): ").strip()

    if entrada.isdigit() and 0 < int(entrada) <= len(base_entrenada):
        return base_entrenada[int(entrada) - 1]['nombre']
    elif entrada:
        return entrada
    else:
        return f"persona_{len(base_entrenada)}"
