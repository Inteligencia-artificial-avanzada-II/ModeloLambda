# EN ESTE SCRIPT SE IMPLEMENTARÁN LAS DISTINTAS FITNESS FUNCTIONS.
from collections import defaultdict

def producto_demandado(individuo, ordenes):
    # Filtrar solo las órdenes con status "Created"
    ordenes_creadas = [orden for orden in ordenes if orden.status == "Created"]
    
    # Crear un diccionario con la necesidad total de cada producto de las órdenes creadas
    necesidad_productos = defaultdict(int)
    for orden in ordenes_creadas:
        for producto_info in orden.productos:
            for producto, cantidades in producto_info.items():
                necesidad_productos[producto] += cantidades[1]  # 'solicitada'

    # Calcular el puntaje basado en la posición del camión en la lista
    puntaje_total = 0
    for posicion, camion in enumerate(individuo):
        # Calcular la contribución de cada camión según los productos que contiene
        contribucion_camion = sum(
            min(cantidad, necesidad_productos[producto])
            for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
            if producto in necesidad_productos
        )
        
        # Dar más peso a los camiones al inicio de la lista (posición inversa)
        peso = len(individuo) - posicion  # El primer camión tiene el mayor peso
        puntaje_total += contribucion_camion * peso

    return puntaje_total

def producto_escaso(individuo, cedis):
    # Crear un diccionario de disponibilidad de productos con la columna 'Producto' y 'Ubicado' del inventario
    inventario_disponible = cedis.inventario.set_index('Producto')['Ubicado'].to_dict()
    
    # Definir productos escasos con un umbral (por ejemplo, cantidad < 10)
    umbral_escasez = 340 # El umbral es el primer cuartil de la distribución de productos ubicados en el inventario
    productos_escasos = {producto for producto, cantidad in inventario_disponible.items() if cantidad < umbral_escasez}
    
    # Calcular el puntaje en función de la prioridad dada a los camiones que más aportan productos escasos
    puntaje_total = 0
    for posicion, camion in enumerate(individuo):
        # Calcular la contribución del camión a los productos escasos
        contribucion_escasa = sum(
            cantidad for producto_info in camion.contenido
            for producto, cantidad in producto_info.items()
            if producto in productos_escasos
        )
        
        # Dar más peso a camiones con alta contribución en posiciones iniciales
        peso = len(individuo) - posicion
        puntaje_total += contribucion_escasa * peso

    return puntaje_total

def tiempo_descarga():
    # priorizar camiones con poco producto
    pass

def mayoreo():
    # priorizar producto que cumple con ordenes de mayoreo (tipo de producto)
    pass