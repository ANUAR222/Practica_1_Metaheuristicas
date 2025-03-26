import numpy as np
import pandas as pd
from preprocesamiento import paquetes, centros
from greedy import asignar_greedy, calcular_distancia

# Función para calcular el tiempo total de entrega
def calcular_tiempo_total(asignaciones, paquetes, centros):
    tiempo_total = 0
    for id_paquete, id_centro in asignaciones.items():
        paquete = paquetes[paquetes['ID_Paquete'] == id_paquete].iloc[0]
        centro = centros[centros['ID_Centro'] == id_centro].iloc[0]
        distancia = calcular_distancia(paquete['Ubicacion_X'], paquete['Ubicacion_Y'], 
                                    centro['Ubicacion_X'], centro['Ubicacion_Y'])
        tiempo_total += paquete['Tiempo_Entrega'] * distancia
    return tiempo_total

# Algoritmo de Búsqueda Local
def busqueda_local(asignaciones, paquetes, centros, max_iteraciones=1000):
    tiempo_actual = calcular_tiempo_total(asignaciones, paquetes, centros)
    for _ in range(max_iteraciones):
        mejora = False
        for id_paquete, id_centro in asignaciones.items():
            for nuevo_id_centro in centros['ID_Centro']:
                if nuevo_id_centro != id_centro:
                    # Crear una nueva asignación cambiando el centro
                    nuevas_asignaciones = asignaciones.copy()
                    nuevas_asignaciones[id_paquete] = nuevo_id_centro
                    nuevo_tiempo = calcular_tiempo_total(nuevas_asignaciones, paquetes, centros)
                    if nuevo_tiempo < tiempo_actual:
                        asignaciones = nuevas_asignaciones
                        tiempo_actual = nuevo_tiempo
                        mejora = True
                        break
            if mejora:
                break
        if not mejora:
            break
    return asignaciones, tiempo_actual

# Ejecutar el Algoritmo de Búsqueda Local
asignaciones_iniciales = asignar_greedy(paquetes, centros)
asignaciones_optimizadas, tiempo_optimizado = busqueda_local(asignaciones_iniciales, paquetes, centros)
print('Asignaciones optimizadas:', asignaciones_optimizadas)
print('Tiempo total optimizado:', tiempo_optimizado)
