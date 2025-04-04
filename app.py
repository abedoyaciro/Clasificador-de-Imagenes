import streamlit as st
import os
import shutil
from procesador_img import cargar_imagenes, extraer_rostros, agrupar_por_rostros, organizar_imagenes

def run_pipeline():
    # Ejecuta el flujo completo: carga, detección, agrupación y organización.
    imagenes = cargar_imagenes("source")
    if not imagenes:
        st.error("No se encontraron imágenes en la carpeta /source.")
        return
    rostros = extraer_rostros(imagenes)
    if not rostros:
        st.error("No se detectaron rostros en las imágenes.")
        return
    agrupados = agrupar_por_rostros(rostros)
    organizar_imagenes(agrupados)
    st.success("¡Procesamiento completado!")
    return agrupados

def display_groups():
    processed_dir = "processed"
    if not os.path.exists(processed_dir):
        st.warning("No se ha generado la carpeta /processed.")
        return
    grupos = os.listdir(processed_dir)
    st.header("Resultados agrupados")
    for grupo in grupos:
        st.subheader(grupo)
        grupo_dir = os.path.join(processed_dir, grupo)
        imagenes = os.listdir(grupo_dir)
        if imagenes:
            for imagen in imagenes:
                imagen_path = os.path.join(grupo_dir, imagen)
                st.image(imagen_path, caption=imagen, width=200)
        else:
            st.write("No hay imágenes en este grupo.")

def clear_processed():
    processed_dir = "processed"
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
        st.success("Carpeta /processed eliminada.")
    else:
        st.info("La carpeta /processed no existe.")

st.title("Clasificador de Imágenes con IA")
st.write("Esta aplicación clasifica imágenes por rostros y las organiza en grupos.")

# Menú lateral de navegación
option = st.sidebar.selectbox("Navegación", ["Inicio", "Procesar Imágenes", "Ver Resultados", "Limpiar Resultados"])

if option == "Inicio":
    st.write("Bienvenido a la aplicación de clasificación de imágenes.")
    st.write("Utiliza el menú lateral para ejecutar el procesamiento, visualizar los resultados o limpiar la carpeta de resultados.")

elif option == "Procesar Imágenes":
    st.write("Ejecuta el pipeline de procesamiento.")
    if st.button("Procesar imágenes en /source"):
        run_pipeline()

elif option == "Ver Resultados":
    st.write("Visualiza los grupos generados en la carpeta /processed.")
    display_groups()

elif option == "Limpiar Resultados":
    st.write("Elimina la carpeta /processed para reiniciar el proceso.")
    if st.button("Limpiar carpeta /processed"):
        clear_processed()
