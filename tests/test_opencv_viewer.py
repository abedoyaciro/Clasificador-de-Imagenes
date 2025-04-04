import os
import cv2

def mostrar_imagen(imagen_path, titulo="Imagen"):
    """
    Muestra la imagen redimensionada para que se ajuste a la pantalla.
    Espera una tecla para continuar.
    """
    if not os.path.exists(imagen_path):
        print(f"[❌] Imagen no encontrada: {imagen_path}")
        return

    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print(f"[❌] No se pudo cargar la imagen: {imagen_path}")
        return

    # Redimensionar si es muy grande
    max_dim = 800  # píxeles máximos de ancho o alto
    height, width = imagen.shape[:2]
    scale = min(max_dim / width, max_dim / height, 1.0)
    nueva_medida = (int(width * scale), int(height * scale))
    imagen_redimensionada = cv2.resize(imagen, nueva_medida)

    print(f"[✔] Mostrando {os.path.basename(imagen_path)} - Dimensión original: {width}x{height} | Redimensionada: {nueva_medida}")

    cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
    cv2.imshow(titulo, imagen_redimensionada)
    print("Presiona una tecla en la ventana para continuar...")
    cv2.waitKey(0)
    cv2.destroyWindow(titulo)

def mostrar_imagenes_en_carpeta(carpeta):
    """
    Recorre todas las imágenes válidas en la carpeta y las muestra una por una.
    """
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp')
    imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]

    if not imagenes:
        print("⚠️ No se encontraron imágenes válidas en la carpeta.")
        return

    print(f"[🔎] Imágenes encontradas: {len(imagenes)}")

    for archivo in imagenes:
        ruta = os.path.join(carpeta, archivo)
        mostrar_imagen(ruta, "Visualización")

if __name__ == "__main__":
    carpeta = "source"
    mostrar_imagenes_en_carpeta(carpeta)
