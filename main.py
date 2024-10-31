from utils.install_requirements import install_requirements
install_requirements()
from utils.process_input_xlsx import process_data
from utils.load_data_as_objects import cargar_camiones, cargar_ordenes
from utils.response import get_response
from objects.cedis import CEDIS
from objects.patio import Patio
from scripts.estrategia_evolutiva import evolve

def main():
    errors = {}
    
    # Step 1: Procesar el archivo de entrada
    try:
        process_data('Info.xlsx')
    except Exception as e:
        errors["input_data"] = "Error al procesar los datos de entrada: " + str(e)
        print(errors)
        return get_response(errors)

    # Step 2: crear los objetos
    try:
        camiones = cargar_camiones('data/camiones.csv')
        ordenes = cargar_ordenes('data/ordenes.csv')
    except Exception as e:
        errors["data_load"] = "Error al cargar los datos: " + str(e)
        print(errors)
        return get_response(e)

    camiones = camiones[:10]
    cedis = CEDIS(n_fosas=8,path_inventario='data/inventario.csv')
    patio = Patio()

    # Step 3: Estrategia evolutiva
    # _flag -> mejor fitness de cada flag, en caso de necesitarse en el futuro

    results = {}

    flag = 'DEMANDA'
    try:
        mejor_orden_demanda, _demanda, gens_demanda = evolve(flag, camiones, ordenes, cedis)
        result_demanda = [camion.id_camion for camion in mejor_orden_demanda]
        results["propuesta_demanda"] = result_demanda
        print("PROPUESTA GENERADA.")
    except Exception as e:
        errors["propuesta_demanda"] = "Error al generar propuesta DEMANDA: " + str(e)
        print("Error al generar propuesta DEMANDA:\n", e)
    
    # ------------------------------------------------------------------------------------------------

    flag = "ESCASEZ"
    try:
        mejor_orden_escasez, _escasez, gens_escasez = evolve(flag, camiones, ordenes, cedis)
        result_escasez = [camion.id_camion for camion in mejor_orden_escasez]
        results["propuesta_escasez"] = result_escasez
        print("PROPUESTA GENERADA.")
    except Exception as e:
        errors["propuesta_escasez"] = "Error al generar propuesta ESCASEZ: " + str(e)
        print("Error al generar propuesta ESCASEZ:\n", e)

    # ------------------------------------------------------------------------------------------------

    flag = "CARGA"
    try:
        mejor_orden_carga, _carga, gens_carga = evolve(flag, camiones, ordenes, cedis)
        result_carga = [camion.id_camion for camion in mejor_orden_carga]
        results["propuesta_carga"] = result_carga
        print("PROPUESTA GENERADA.")
    except Exception as e:
        errors["propuesta_carga"] = "Error al generar propuesta CARGA: " + str(e)
        print("Error al generar propuesta CARGA:\n", e)

    return get_response(e=errors,propuestas=results)

if __name__ == "__main__":
    main()