from collections import Counter


def reporte_resumen_clasificaciones(clasificaciones):
    """
    Imprime un resumen por persona y cantidad de imágenes asociadas.
    """
    nombres = [info['nombre'] for info in clasificaciones.values()]
    conteo = Counter(nombres)

    print("\n📊 Resumen de clasificaciones:")
    sorted_items = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    for nombre, cantidad in sorted_items:
        print(f" - {nombre}: {cantidad} imagen(es)")
