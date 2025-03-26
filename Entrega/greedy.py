import numpy as np
import pandas as pd
from preprocesamiento import paquetes, centros

# Función para calcular la distancia euclidiana
def calcular_distancia(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Algoritmo voraz (greedy) para asignar paquetes a centros
def asignar_greedy(paquetes, centros):
    asignaciones = {}
    capacidades_centros = dict(zip(centros['ID_Centro'], centros['Capacidad']))
    
    for _, paquete in paquetes.iterrows():
        distancia_min = float('inf')
        mejor_centro = None
        
        for _, centro in centros.iterrows():
            if capacidades_centros[centro['ID_Centro']] > 0:
                distancia = calcular_distancia(paquete['Ubicacion_X'], paquete['Ubicacion_Y'], 
                                            centro['Ubicacion_X'], centro['Ubicacion_Y'])
                if distancia < distancia_min:
                    distancia_min = distancia
                    mejor_centro = centro['ID_Centro']
        
        if mejor_centro:
            asignaciones[paquete['ID_Paquete']] = mejor_centro
            capacidades_centros[mejor_centro] -= 1
    
    return asignaciones

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

# Ejecutar el algoritmo greedy
asignaciones = asignar_greedy(paquetes, centros)
tiempo_inicial = calcular_tiempo_total(asignaciones, paquetes, centros)
print('Asignaciones iniciales:', asignaciones)
print('Tiempo total inicial:', tiempo_inicial)
