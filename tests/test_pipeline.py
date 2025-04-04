from procesador_img import (
    cargar_imagenes,
    extraer_rostros,
    agrupar_por_rostros,
    organizar_imagenes
)


def main():
    print("🔄 Cargando imágenes desde /source...")
    imagenes = cargar_imagenes("source")
    print(f"📸 Imágenes cargadas: {len(imagenes)}")

    print("🧠 Detectando rostros y extrayendo vectores...")
    rostros = extraer_rostros(imagenes)
    print(f"🙂 Rostros detectados: {len(rostros)}")

    if not rostros:
        print("⚠️ No se detectaron rostros. Revisa tus imágenes.")
        return

    print("🔗 Agrupando rostros por similitud...")
    agrupados = agrupar_por_rostros(rostros)
    grupos_unicos = set(d['grupo'] for d in agrupados)
    print(f"👥 Grupos encontrados: {len(grupos_unicos)}")

    print("📁 Organizando imágenes en la carpeta /processed...")
    organizar_imagenes(agrupados)
    print("✅ Proceso completo. Revisa la carpeta /processed.")


if __name__ == "__main__":
    main()
