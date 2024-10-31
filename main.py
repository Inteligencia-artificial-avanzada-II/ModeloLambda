from utils.install_requirements import install_requirements
install_requirements()
from utils.process_input_xlsx import process_data
from utils.load_data_as_objects import cargar_camiones, cargar_ordenes
from utils.response import get_response
from objects.cedis import CEDIS
from objects.patio import Patio
from scripts.estrategia_evolutiva import evolve

def main():

    # Step 1: Procesar el archivo de entrada
    try:
        process_data('Info.xlsx')
    except Exception as e:
        return get_response(e)

    # Step 2: crear los objetos
    try:
        camiones = cargar_camiones('data/camiones.csv')
        ordenes = cargar_ordenes('data/ordenes.csv')
    except Exception as e:
        return get_response(e)

    camiones = camiones[:5]
    cedis = CEDIS(n_fosas=8,path_inventario='data/inventario.csv')
    patio = Patio()

    # Step 3: Estrategia evolutiva

    flag = 'DEMANDA'
    try:
        mejor_orden = evolve(flag, camiones, ordenes, cedis)
        result = [camion.id_camion for camion in mejor_orden]
        print("PROPUESTA GENERADA.")
    except Exception as e:
        return get_response(e)
    
    # ------------------------------------------------------------------------------------------------

    flag = "ESCASEZ"
    try:
        mejor_orden = evolve(flag, camiones, ordenes, cedis)
        result = [camion.id_camion for camion in mejor_orden]
    except Exception as e:
        return get_response(e)

    print("Propuesta generada")
    return get_response(response_list=result)
    # TO DO:
    """
    - crear matriz de pruebas con datos sinteticos para evaluar las distintas funciones de fitness (maybe | flojera)
    """
main()
