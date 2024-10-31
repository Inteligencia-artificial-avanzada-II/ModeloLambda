# EN ESTE SCRIPT SE IMPLEMENTARÁN LAS DISTINTAS FITNESS FUNCTIONS.
from collections import defaultdict

def producto_escaso():
    # priorizar producto escaso en almacen
    pass

def tiempo_espera():
    # priorizar camiones con poco producto
    pass

def producto_ordenes(individuo, ordenes):
    """
    priorizar producto que cumple con ordenes de mayoreo (tipo de producto)
    """
    # Filtrar solo las órdenes con status "Created"
    ordenes_creadas = [orden for orden in ordenes if orden.status == "Created" | "Partly Allocated"]

    # Crear un diccionario con la necesidad total de cada producto por cada tipo de orden
    necesidad_productos_fp = defaultdict(int)
    necesidad_productos_pk = defaultdict(int)
    for orden in ordenes_creadas:
        for producto_info in orden.productos:
            for producto, cantidades in producto_info.items():
                if orden.tipo_de_orden == 'FP':
                    necesidad_productos_fp[producto] += cantidades[1] # solicitada en ordenes tipo 'FP'
                elif orden.tipo_de_orden == 'PK':
                    necesidad_productos_pk[producto] += cantidades[1] # solicitada en ordenes tipo 'PK'

    # Calcular la contribución de cada camión y darle más peso a los que cumplan con las ordenes tipo 'FP'
    puntaje_total = 0
    for posicion, camion in enumerate(individuo):
        # Calcular la contribución de cada camión según los productos que contiene
        contribucion_camion_fp = sum(
            min(cantidad, necesidad_productos_fp[producto])
            for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
            if producto in necesidad_productos_fp
        )

        contribucion_camion_pk = sum(
            min(cantidad, necesidad_productos_pk[producto])
            for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
            if producto in necesidad_productos_pk
        )

        # Dar más peso a los camiones que cumplen con las ordenes de mayoreo
        peso_fp = 2
        puntaje_total += (peso_fp * contribucion_camion_fp) * contribucion_camion_pk 

    return puntaje_total
