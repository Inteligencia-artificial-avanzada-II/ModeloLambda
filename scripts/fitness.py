# EN ESTE SCRIPT SE IMPLEMENTARÁN LAS DISTINTAS FITNESS FUNCTIONS.
from collections import defaultdict

def producto_escaso(individuo, cedis):
    """ 
    Priorizar el llenado de los productos escasos en el almacén
    """
    # priorizar producto escaso en almacen
    # Crear un diccionario de disponibilidad de productos con la columna 'Producto' y 'Ubicado' del inventario
    inventario_disponible = cedis.inventario.set_index('Producto')['Ubicado'].to_dict()
    
    # Definir productos escasos con un umbral 
    umbral_escasez = 340 # El umbral es el primer cuartil de la distribución de productos ubicados en el inventario
    productos_escasos = {producto for producto, cantidad in inventario_disponible.items() if cantidad < umbral_escasez}
    
    # Calcular el puntaje en función de la prioridad dada a los camiones que más aportan productos escasos
    puntaje_total = 0
    for posicion, camion in enumerate(individuo):
        # Calcular la contribución del camión a los productos escasos con un peso adicional inversamente proporcional a la cantidad disponible
        contribucion_escasa = sum(
            cantidad * (umbral_escasez / (inventario_disponible[producto] + 1))
            for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
            if producto in productos_escasos
        )
        
        # Sumar la contribución del camión al puntaje total
        puntaje_total += contribucion_escasa

    return puntaje_total

def producto_ordenes(individuo, ordenes):
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

def tiempo_espera():
    # priorizar camiones con poco producto
    pass