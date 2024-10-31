import random
from collections import defaultdict

# Función de evaluación de la solución
def fitness(individuo, ordenes):
    # Filtrar solo las órdenes con status "Created"
    ordenes_creadas = [orden for orden in ordenes if orden.status == "Created" | "Partly Allocated"]
    
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

# Generar la población inicial
def generar_poblacion_inicial(camiones, tamano_poblacion):
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = random.sample(camiones, len(camiones))  # Orden aleatorio de camiones
        poblacion.append(individuo)
    return poblacion

# Selección del mejor individuo
def seleccion_mejor(poblacion, ordenes):
    # Evaluar cada individuo y obtener el de mejor puntaje
    mejor_individuo = max(poblacion, key=lambda ind: fitness(ind, ordenes))
    return mejor_individuo

# Función de mutación con varias técnicas basadas en probabilidades
def mutacion(individuo):
    probabilidad = random.random()

    if probabilidad < 0.20:
        # 20% de las veces: Mutación por Intercambio Simple
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    
    elif probabilidad < 0.40:
        # 20% de las veces: Mutación por Inversión de Segmento
        inicio = random.randint(0, len(individuo) - 2)
        fin = random.randint(inicio + 1, len(individuo) - 1)
        individuo[inicio:fin] = reversed(individuo[inicio:fin])
    
    elif probabilidad < 0.60:
        # 20% de las veces: Mutación por Intercambio Múltiple
        num_intercambios = random.randint(2, 5)  # Definir cuántos intercambios hacer
        for _ in range(num_intercambios):
            idx1, idx2 = random.sample(range(len(individuo)), 2)
            individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]

    elif probabilidad < 0.80:
        # 20% de las veces: Mutación por Intercambio Total
        return random.sample(individuo, len(individuo))
    
    else:
        # 20% de las veces: Mutación por Inserción
        idx1 = random.randint(0, len(individuo) - 1)
        idx2 = random.randint(0, len(individuo) - 1)
        camion = individuo.pop(idx1)
        individuo.insert(idx2, camion)
    
    return individuo

# Estrategia evolutiva
def evolve(camiones, ordenes, tamano_poblacion=30, num_generaciones=30):
    # Generar la población inicial
    poblacion = generar_poblacion_inicial(camiones, tamano_poblacion)

    for generacion in range(num_generaciones):
        print(f"\n--- Generación {generacion + 1} ---")
        
        # Evaluar y seleccionar el mejor individuo de la población
        mejor_individuo = seleccion_mejor(poblacion, ordenes)
        
        # Evaluar el mejor puntaje de la generación actual
        mejor_puntaje = fitness(mejor_individuo, ordenes)
        print(f"Mejor puntaje de la generación {generacion + 1}: {mejor_puntaje}")
        
        # Imprimir el mejor individuo en esta generación (orden de camiones)
        print("Mejor individuo (orden de camiones):", [camion.id_camion for camion in mejor_individuo])

        # Aplicar mutación para crear una nueva población
        nueva_poblacion = [mutacion(mejor_individuo) for _ in range(tamano_poblacion)]
        poblacion = nueva_poblacion

    print('-'*50)

    # Retornar el mejor orden final
    mejor_orden = seleccion_mejor(poblacion, ordenes)
    return mejor_orden