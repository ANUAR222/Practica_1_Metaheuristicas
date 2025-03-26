import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from preprocesamiento import generar_datos
from greedy import asignar_greedy, calcular_tiempo_total
from local_search import busqueda_local

# Asegurar que exista la carpeta Entrega al inicio del script
os.makedirs('Entrega', exist_ok=True)

# Función para ejecutar experimentos con diferentes tamaños de datos
def ejecutar_experimentos(tamaños=[50, 100, 500]):
    resultados = []
    for N in tamaños:
        # Generar el conjunto de datos
        # Generar el conjunto de datos
        paquetes, centros = generar_datos(N=N,
                                          ruta_csv="amazon_delivery.csv")
        
        # Ejecutar algoritmo Greedy
        asignaciones = asignar_greedy(paquetes, centros)
        tiempo_greedy = calcular_tiempo_total(asignaciones, paquetes, centros)
        
        # Ejecutar algoritmo de Búsqueda Local
        asignaciones_optimizadas, tiempo_optimizado = busqueda_local(asignaciones, paquetes, centros)
        
        # Guardar resultados
        resultados.append({
            'N': N,
            'Tiempo_Greedy': tiempo_greedy,
            'Tiempo_Búsqueda_Local': tiempo_optimizado,
            'Mejora (%)': round(((tiempo_greedy - tiempo_optimizado) / tiempo_greedy) * 100, 2)
        })
    
    # Imprimir resultados
    print('\nResultados:')
    print(pd.DataFrame(resultados))
    
    # Guardar resultados en un archivo CSV
    pd.DataFrame(resultados).to_csv('Entrega/resultados_experimentos.csv', index=False)
    
    # Generar gráficas
    df = pd.DataFrame(resultados)
    
    # Gráfico de barras: Comparación de tiempo de entrega total
    plt.figure(figsize=(10, 5))
    plt.bar(df['N'] - 10, df['Tiempo_Greedy'], width=20, label='Algoritmo Greedy', color='blue')
    plt.bar(df['N'] + 10, df['Tiempo_Búsqueda_Local'], width=20, label='Algoritmo Búsqueda Local', color='orange')
    plt.xlabel('Tamaño del conjunto de datos (N)')
    plt.ylabel('Tiempo total de entrega')
    plt.title('Comparación de tiempo total de entrega')
    plt.legend()
    plt.savefig('Entrega/comparacion_tiempo_entrega.png')
    
    # Gráfico de línea: Porcentaje de mejora
    plt.figure(figsize=(10, 5))
    plt.plot(df['N'], df['Mejora (%)'], marker='o', linestyle='-', color='green')
    plt.xlabel('Tamaño del conjunto de datos (N)')
    plt.ylabel('Mejora (%)')
    plt.title('Porcentaje de mejora con el algoritmo de Búsqueda Local')
    plt.grid(True)
    plt.savefig('Entrega/porcentaje_mejora.png')

    # Análisis de resultados mejorado
    for resultado in resultados:
        print(f"\nAnálisis para N={resultado['N']}:")
        print(f"Tiempo Greedy: {resultado['Tiempo_Greedy']:.2f}")
        print(f"Tiempo Búsqueda Local: {resultado['Tiempo_Búsqueda_Local']:.2f}")
        print(f"Mejora: {resultado['Mejora (%)']}%")

    # Crear visualizaciones mejoradas
    df = pd.DataFrame(resultados)

    # Gráfico de barras con barras de error
    plt.figure(figsize=(12, 6))
    x = np.arange(len(df['N']))
    ancho = 0.35

    plt.bar(x - ancho/2, df['Tiempo_Greedy'], ancho, label='Greedy', color='skyblue')
    plt.bar(x + ancho/2, df['Tiempo_Búsqueda_Local'], ancho, label='Búsqueda Local', color='lightgreen')

    plt.xlabel('Tamaño del conjunto de datos (N)')
    plt.ylabel('Tiempo total de entrega')
    plt.title('Comparativa de rendimiento: Greedy vs Búsqueda Local')
    plt.xticks(x, df['N'])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('Entrega/rendimiento_comparativo.png', dpi=300, bbox_inches='tight')

    # Guardar resultados detallados en CSV
    df.to_csv('Entrega/resultados_detallados.csv', index=False)

if __name__ == "__main__":
    print("Iniciando experimentos...")
    ejecutar_experimentos()
    print("Experimentos completados. Resultados guardados en 'Entrega/resultados_detallados.csv'")
