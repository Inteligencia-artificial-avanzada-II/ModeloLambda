# EN ESTE SCRIPT SE IMPLEMENTARÁN LAS DISTINTAS FITNESS FUNCTIONS.
from collections import defaultdict

def ordenes_fp(individuo, ordenes):
    """
    Priorizar el producto que cumpla con las órdenes, dándole un peso mayor a las órdenes tipo 'FP'
    """
    # Filtrar solo las órdenes con status "Created" o "Partly Allocated"
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

def ordenes_pk(individuo, ordenes):
    """
    Priorizar el producto que cumpla con las órdenes, dándole un peso mayor a las órdenes tipo 'PK'
    """
    # Filtrar solo las órdenes con status "Created" o "Partly Allocated"
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
        peso_pk = 2
        puntaje_total += (peso_pk * contribucion_camion_pk) * contribucion_camion_fp 

    return puntaje_total

def max_ordenes(individuo, ordenes):
    """
    Priorizar el llenado de las ordenes
    """
    # Filtrar solo las órdenes con status "Created" o "Partly Allocated"
    ordenes_creadas = [orden for orden in ordenes if orden.status == "Created" | "Partly Allocated"]

    # Crear un diccionario con la necesidad total de cada producto por cada tipo de orden
    necesidad_productos = defaultdict(int)
    for orden in ordenes_creadas:
        for producto_info in orden.productos:
            for producto, cantidades in producto_info.items():
                necesidad_productos[producto] += cantidades[1]

    # Calcular la contribución de cada camión y darle más peso a los que cumplan con las ordenes tipo 'FP'
    puntaje_total = 0
    for posicion, camion in enumerate(individuo):
        # Calcular la contribución de cada camión según los productos que contiene
        contribucion_camion = sum(
            min(cantidad, necesidad_productos[producto])
            for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
        )

        # Dar más peso a los camiones que cumplen con las ordenes de mayoreo
        puntaje_total += contribucion_camion

    return puntaje_total

def tiempo_espera():
    # priorizar camiones con poco producto
    pass