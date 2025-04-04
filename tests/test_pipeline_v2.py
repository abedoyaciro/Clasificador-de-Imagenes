import os
import sys
import cv2

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.procesamiento import cargar_imagenes, extraer_rostros
from core.cache import guardar_rostros_cache, cargar_rostros_cache
from interface.clasificador import (cargar_clasificaciones,
                                    guardar_clasificaciones,
                                    flujo_interactivo_de_clasificacion)


# from procesador_img import (cargar_imagenes, extraer_rostros,
#                             guardar_rostros_cache, cargar_rostros_cache)
# from core.cache import guardar_rostros_cache, cargar_rostros_cache
# from clasificador import clasificar_rostro
# from core.organizacion import organizar_imagenes

# Umbrales de comparación
# UMBRAL_SEGURO = 0.45
# UMBRAL_DUDA = 0.70

UMBRAL_SEGURO = 0.52
UMBRAL_DUDA = 0.57

# Base de datos manual
etiquetas_confirmadas = []

# Cambiar este valor si quieres forzar reprocesar
USAR_CACHE = True

if USAR_CACHE and os.path.exists("data/rostros_cache.npz"):
    rostros = cargar_rostros_cache("data/rostros_cache.npz")
else:
    imagenes = cargar_imagenes("data/source")
    rostros = extraer_rostros(imagenes)
    guardar_rostros_cache(rostros, "data/rostros_cache.npz")
    print(f"[📂] Se cargaron {len(rostros)} rostros desde cache")

'''
def mostrar_imagen(imagen_path, titulo="¿Quién es esta persona?"):
    """
    Muestra la imagen redimensionada si es muy grande, y permite
    que la ventana se pueda ajustar manualmente (WINDOW_NORMAL).
    """
    if not os.path.exists(imagen_path):
        print(f"[❌] Imagen no encontrada: {imagen_path}")
        return

    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print(f"[❌] No se pudo cargar la imagen: {imagen_path}")
        return

    # Redimensionar si es grande (máximo 800px)
    max_dim = 800
    h, w = imagen.shape[:2]
    scale = min(max_dim / w, max_dim / h, 1.0)
    nueva_medida = (int(w * scale), int(h * scale))
    imagen_redimensionada = cv2.resize(imagen, nueva_medida)

    print(
        f"[✔] Mostrando: {os.path.basename(imagen_path)} - Redimensionada: \
            {nueva_medida}")
    cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
    cv2.imshow(titulo, imagen_redimensionada)
    print("Presiona una tecla en la ventana para continuar...")
    cv2.waitKey(0)
    cv2.destroyWindow(titulo)
'''


def cerrar_ventanas():
    cv2.destroyAllWindows()


'''
def comparar_con_base(encoding, base):
    if not base:
        return None, None

    distancias = [np.linalg.norm(encoding - persona['encoding'])
                  for persona in base]
    idx_min = int(np.argmin(distancias))
    return base[idx_min], distancias[idx_min]


def clasificar_rostro(nombre_archivo, encoding):
    global etiquetas_confirmadas

    mejor_match, distancia = comparar_con_base(encoding, etiquetas_confirmadas)

    imagen_path = os.path.join("data/source", nombre_archivo)
    mostrar_imagen(imagen_path, "¿Quién es esta persona?")

    if mejor_match and distancia < UMBRAL_SEGURO:
        print(
            f"[AUTO] Clasificado automáticamente como: \
                {mejor_match['nombre']}")
        mejor_match['imagenes'].append(nombre_archivo)
        return mejor_match['nombre']

    elif mejor_match and distancia < UMBRAL_DUDA:
        respuesta = input(
            f"[¿?] ¿Es esta persona '{mejor_match['nombre']}'? \
                (s/n): ").lower()
        if respuesta == 's':
            mejor_match['imagenes'].append(nombre_archivo)
            return mejor_match['nombre']

    print("Personas existentes:")
    for i, persona in enumerate(etiquetas_confirmadas):
        print(f"{i + 1}. {persona['nombre']}")
    nombre = input(
        ("Escribe el nombre o número de la persona, o deja vacío para "
         "crear una nueva: ").strip())

    if nombre.isdigit():
        idx = int(nombre) - 1
        if 0 <= idx < len(etiquetas_confirmadas):
            etiquetas_confirmadas[idx]['imagenes'].append(nombre_archivo)
            return etiquetas_confirmadas[idx]['nombre']
    elif nombre:
        # Reutilizar si ya existe con ese nombre
        for persona in etiquetas_confirmadas:
            if persona['nombre'].lower() == nombre.lower():
                persona['imagenes'].append(nombre_archivo)
                return persona['nombre']
        # Crear nueva entrada
        etiquetas_confirmadas.append({
            'nombre': nombre,
            'encoding': encoding,
            'imagenes': [nombre_archivo]
        })
        return nombre
    else:
        # Crear como "desconocido_X"
        nombre = f"persona_{len(etiquetas_confirmadas)}"
        etiquetas_confirmadas.append({
            'nombre': nombre,
            'encoding': encoding,
            'imagenes': [nombre_archivo]
        })
        return nombre
'''

RUTA_JSON = "data/clasificaciones.json"

'''
def guardar_clasificaciones(clasificaciones):
    with open(RUTA_JSON, "w") as f:
        json.dump(clasificaciones, f, indent=4)
    print(f"[💾] Clasificaciones guardadas en {RUTA_JSON}")


def cargar_clasificaciones():
    if not os.path.exists(RUTA_JSON):
        return {}
    with open(RUTA_JSON, "r") as f:
        return json.load(f)
'''


def main():

    clasificaciones = flujo_interactivo_de_clasificacion(rostros)
    '''
    clasificaciones = cargar_clasificaciones()

    for rostro in rostros:
        nombre_archivo = rostro['nombre_archivo']

        # Saltar si ya está clasificado
        if nombre_archivo in clasificaciones:
            print(
                f"[↪] Ya clasificado: \
                    {nombre_archivo} → \
                        {clasificaciones[nombre_archivo]['nombre']}")
            continue

        encoding = rostro['encoding']
        nombre = validar_y_etiquetar(encoding, nombre_archivo, base_entrenada)

        clasificaciones[nombre_archivo] = {
            "nombre": nombre,
            # "encoding": encoding.tolist()
        }

    guardar_clasificaciones(clasificaciones)
    '''

    cerrar_ventanas()

    print("\n🧾 Resultado final:")
    for archivo, datos in clasificaciones.items():
        print(f"{archivo} → {datos['nombre']}")


if __name__ == "__main__":
    main()
