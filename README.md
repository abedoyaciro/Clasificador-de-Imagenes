# 📦 Proyecto: Clasificador Personalizado de Imágenes con IA

Este proyecto es una herramienta local de clasificación automática de imágenes mediante reconocimiento facial y visual, orientado a usuarios que desean organizar grandes volúmenes de fotos de manera inteligente, incluso cuando el rostro no está visible. Utiliza técnicas de visión por computadora para detectar rostros, comparar similitudes y organizar imágenes en carpetas categorizadas por persona o grupo visual.

---

## 🎯 Objetivo

Crear una herramienta local de clasificación automática de imágenes mediante **reconocimiento de personas por rostro y apariencia visual general**, orientada a organizar fotos de manera inteligente, incluso cuando los rostros no estén completamente visibles, comparando con ejemplos ya agrupados automática o manualmente.

---

## ⚙️ Requisitos del sistema

- **Python 3.8+**
- **12 GB de RAM** (mínimo 4 GB funcionales)
- **Procesador Intel i3-6006U o similar**
- **Sin GPU dedicada**
- **Sistema operativo Windows o Linux**
- **Espacio mínimo recomendado: 5 GB libres**

---

## ✅ Requisitos funcionales

- RF01: Permitir subir o cargar imágenes desde una carpeta.
- RF02: Detectar rostros en las imágenes.
- RF03: Si no hay rostro, extraer características visuales generales (ropa, forma, colores).
- RF04: Comparar imágenes sin rostro contra otras ya clasificadas (por IA o manualmente).
- RF05: Asignar automáticamente una categoría si la similitud es suficientemente alta.
- RF06: Permitir al usuario clasificar manualmente imágenes para mejorar futuras detecciones.
- RF07: Renombrar imágenes según la categoría asignada.
- RF08: Mover imágenes a carpetas correspondientes a su categoría.
- RF09: Mostrar visualmente los grupos y sus imágenes.
- RF10: Permitir reiniciar todo el proceso desde cero.

---

## 📌 Requisitos no funcionales

- RNF01: Ejecutarse correctamente en entornos de bajo rendimiento.
- RNF02: Interfaz simple, intuitiva y en español.
- RNF03: Procesamiento eficiente de hasta 100 imágenes por lote.
- RNF04: Funcionar sin conexión a internet.
- RNF05: Código modular y fácilmente extensible.

---

## 👤 Casos de uso

| Código | Nombre | Actor | Descripción |
|--------|--------|-------|-------------|
| CU01 | Cargar imágenes | Usuario | El usuario carga imágenes desde una carpeta o interfaz. |
| CU02 | Detectar rostros | Sistema | El sistema detecta rostros en las imágenes cargadas. |
| CU03 | Agrupar por similitud facial | Sistema | Agrupa imágenes con rostros similares mediante IA. |
| CU04 | Clasificar por apariencia visual | Sistema | Imágenes sin rostro se agrupan comparando su contenido visual. |
| CU05 | Asignación automática de categorías | Sistema | El sistema asigna categorías o personas a las imágenes según su similitud. |
| CU06 | Clasificación manual | Usuario | El usuario puede etiquetar imágenes manualmente para ayudar al sistema. |
| CU07 | Renombrar y organizar | Sistema | Las imágenes se renombran y se mueven a carpetas organizadas. |
| CU08 | Ver resultados | Usuario | El usuario revisa visualmente las agrupaciones. |
| CU09 | Reiniciar proceso | Usuario | Permite limpiar resultados y comenzar desde cero. |

---

## 📁 Estructura del proyecto

```md

/Clasificación_de_Imágenes
│
├── app.py                    ← Interfaz principal (Streamlit o consola)
├── main.py                   ← Entrada principal para ejecución en consola
├── requirements.txt
├── README.md
│
├── /core                     ← Lógica del negocio (clustering, detección, organización)
│   ├── procesamiento.py      ← cargar_imagenes, extraer_rostros, organizar_imagenes
│   ├── clustering.py         ← agrupar_por_rostros (DBSCAN)
│   ├── cache.py              ← guardar_rostros_cache, cargar_rostros_cache
│
├── /interface                ← Entrada y validación humana
│   ├── clasificador.py       ← clasificar_rostro, mostrar_imagen
│   ├── validador.py          ← flujo interactivo de confirmación
│
├── /data
│   ├── source/               ← Imágenes originales
│   ├── processed/            ← Resultado clasificado
│   ├── rostros_cache.npz     ← Cache de encodings
│   ├── clasificaciones.json  ← Historial de clasificaciones
│
├── /utils
│   ├── visor.py              ← Funciones de visualización (OpenCV, PIL, matplotlib)
│   ├── helpers.py            ← Funciones auxiliares (formato, logs, resolución, etc.)
│
└── /entrenamiento            ← (Futuro) módulo incremental de aprendizaje
    ├── entrenador.py         ← reconstruir_base_entrenada
```

---

## 🚀 ¿Qué hace este proyecto?

1. Carga imágenes desde una carpeta.
2. Detecta rostros automáticamente cuando están presentes.
3. Agrupa imágenes con rostros similares.
4. Cuando no hay rostro, compara visualmente con imágenes ya clasificadas.
5. Renombra y organiza las imágenes en carpetas por persona o grupo.
6. Permite clasificar manualmente imágenes difíciles.
7. Muestra una galería visual de los resultados.
8. Todo el procesamiento ocurre localmente, sin necesidad de internet.

---

## 🧱 Próximos pasos

- [ ] Implementar el módulo de detección y comparación de imágenes.
- [ ] Integrar extracción visual general con `resnet` o `CLIP`.
- [ ] Crear interfaz en Streamlit para cargar, visualizar y controlar el proceso.
- [ ] Agregar opción de clasificación manual asistida.
- [ ] Agregar botón para reiniciar y limpiar las carpetas.

# README.md (resumen inicial)

"""
# Clasificador de Rostros con Validación Humana

Este proyecto utiliza reconocimiento facial automático con validación humana para clasificar, organizar y mejorar progresivamente la identificación de personas en fotografías.

## Características
- Detección de rostros con `face_recognition`
- Agrupación automática con `DBSCAN`
- Validación y corrección asistida por el usuario
- Memoria persistente de clasificaciones previas
- Interfaz en consola y posibilidad de interfaz gráfica

## Estructura
- `core/`: Módulos de lógica (detección, clustering, cache, organización)
- `interface/`: Clasificador interactivo (humano en el ciclo)
- `data/`: Imágenes fuente, resultados, cache y JSON de etiquetas

## Requisitos
```bash
conda activate clasificador-img
pip install -r requirements.txt
```

## Uso
```bash
python main.py
```
