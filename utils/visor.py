import cv2
import os


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

    max_dim = 800
    h, w = imagen.shape[:2]
    scale = min(max_dim / w, max_dim / h, 1.0)
    nueva_medida = (int(w * scale), int(h * scale))
    imagen_redimensionada = cv2.resize(imagen, nueva_medida)

    print(f"[✔] Mostrando: {os.path.basename(imagen_path)}")
    print("Presiona una tecla en la ventana para continuar...")
    cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
    cv2.imshow(titulo, imagen_redimensionada)
    cv2.waitKey(0)
    cv2.destroyWindow(titulo)
