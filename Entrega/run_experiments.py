import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from preprocesamiento import generar_datos
from greedy import asignar_greedy, calcular_tiempo_total
from local_search import busqueda_local

# Asegurar que exista la carpeta Entrega al inicio del script
os.makedirs('Entrega', exist_ok=True)


def ejecutar_experimentos(tamaños=[50, 100, 500], repeticiones=1):
    """
    Ejecuta experimentos comparativos entre algoritmos Greedy y Búsqueda Local
    para diferentes tamaños de conjuntos de datos.

    Parámetros:
    -----------
    tamaños: list
        Lista con los tamaños de conjuntos de datos a utilizar
    repeticiones: int
        Número de veces que se repite cada experimento para obtener resultados más robustos

    Resultados:
    -----------
    - Archivos CSV con resultados detallados
    - Gráficos comparativos guardados en la carpeta 'Entrega'
    - Análisis de tiempos de ejecución computacional
    """
    resultados = []
    tiempos_ejecucion = []

    for N in tamaños:
        print(f"\nEjecutando experimentos para N={N}...")

        # Variables para promedio de repeticiones
        tiempo_greedy_acum = 0
        tiempo_optimizado_acum = 0
        tiempo_ejec_greedy_acum = 0
        tiempo_ejec_local_acum = 0
        mejora_acum = 0

        for rep in range(repeticiones):
            print(f"  Repetición {rep + 1}/{repeticiones}")

            # Generar el conjunto de datos
            paquetes, centros = generar_datos(N=N, ruta_csv="amazon_delivery.csv")

            # Ejecutar algoritmo Greedy y medir tiempo de ejecución
            inicio_greedy = time.time()
            asignaciones = asignar_greedy(paquetes, centros)
            tiempo_ejec_greedy = time.time() - inicio_greedy
            tiempo_greedy = calcular_tiempo_total(asignaciones, paquetes, centros)

            # Ejecutar algoritmo de Búsqueda Local y medir tiempo de ejecución
            inicio_local = time.time()
            asignaciones_optimizadas, tiempo_optimizado = busqueda_local(asignaciones, paquetes, centros)
            tiempo_ejec_local = time.time() - inicio_local

            # Calcular mejora
            mejora = ((tiempo_greedy - tiempo_optimizado) / tiempo_greedy) * 100

            # Acumular para promedios
            tiempo_greedy_acum += tiempo_greedy
            tiempo_optimizado_acum += tiempo_optimizado
            tiempo_ejec_greedy_acum += tiempo_ejec_greedy
            tiempo_ejec_local_acum += tiempo_ejec_local
            mejora_acum += mejora

        # Calcular promedios
        tiempo_greedy_prom = tiempo_greedy_acum / repeticiones
        tiempo_optimizado_prom = tiempo_optimizado_acum / repeticiones
        tiempo_ejec_greedy_prom = tiempo_ejec_greedy_acum / repeticiones
        tiempo_ejec_local_prom = tiempo_ejec_local_acum / repeticiones
        mejora_prom = mejora_acum / repeticiones

        # Guardar resultados
        resultados.append({
            'N': N,
            'Tiempo_Greedy': tiempo_greedy_prom,
            'Tiempo_Búsqueda_Local': tiempo_optimizado_prom,
            'Mejora (%)': round(mejora_prom, 2)
        })

        tiempos_ejecucion.append({
            'N': N,
            'Tiempo_Ejecución_Greedy': tiempo_ejec_greedy_prom,
            'Tiempo_Ejecución_Búsqueda_Local': tiempo_ejec_local_prom
        })

    # Convertir a DataFrame
    df_resultados = pd.DataFrame(resultados)
    df_tiempos = pd.DataFrame(tiempos_ejecucion)

    # Imprimir resultados
    print('\n===================== RESULTADOS =====================')
    print('\nMétrica: Tiempo total de entrega (calidad de solución)')
    print(df_resultados)

    print('\nMétrica: Tiempo de ejecución computacional (en segundos)')
    print(df_tiempos)

    # Guardar resultados en archivos CSV
    df_resultados.to_csv('Entrega/resultados_calidad_solucion.csv', index=False)
    df_tiempos.to_csv('Entrega/resultados_tiempo_ejecucion.csv', index=False)

    # ===== VISUALIZACIONES =====

    # 1. Gráfico de barras: Comparación de tiempo de entrega total
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    pos = np.arange(len(df_resultados['N']))

    plt.bar(pos - bar_width / 2, df_resultados['Tiempo_Greedy'], bar_width,
            label='Algoritmo Greedy', color='#3498db', edgecolor='black', alpha=0.8)
    plt.bar(pos + bar_width / 2, df_resultados['Tiempo_Búsqueda_Local'], bar_width,
            label='Algoritmo Búsqueda Local', color='#2ecc71', edgecolor='black', alpha=0.8)

    plt.xlabel('Tamaño del conjunto de datos (N)', fontsize=12)
    plt.ylabel('Tiempo total de entrega', fontsize=12)
    plt.title('Comparación de calidad de solución entre algoritmos', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.xticks(pos, df_resultados['N'])
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('Entrega/comparacion_calidad_solucion.png', dpi=300)

    # 2. Gráfico de línea: Porcentaje de mejora
    plt.figure(figsize=(10, 6))
    plt.plot(df_resultados['N'], df_resultados['Mejora (%)'], marker='o', linestyle='-',
             linewidth=2, color='#9b59b6', markersize=8)

    for x, y in zip(df_resultados['N'], df_resultados['Mejora (%)']):
        plt.text(x, y + 0.5, f"{y:.2f}%", ha='center', fontsize=9)

    plt.xlabel('Tamaño del conjunto de datos (N)', fontsize=12)
    plt.ylabel('Mejora (%)', fontsize=12)
    plt.title('Porcentaje de mejora con Búsqueda Local respecto a Greedy', fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('Entrega/porcentaje_mejora.png', dpi=300)

    # 3. Gráfico de tiempo de ejecución computacional
    plt.figure(figsize=(10, 6))

    plt.plot(df_tiempos['N'], df_tiempos['Tiempo_Ejecución_Greedy'], marker='s',
             linestyle='-', linewidth=2, color='#e74c3c', markersize=8, label='Greedy')
    plt.plot(df_tiempos['N'], df_tiempos['Tiempo_Ejecución_Búsqueda_Local'], marker='^',
             linestyle='-', linewidth=2, color='#f39c12', markersize=8, label='Búsqueda Local')

    plt.xlabel('Tamaño del conjunto de datos (N)', fontsize=12)
    plt.ylabel('Tiempo de ejecución (segundos)', fontsize=12)
    plt.title('Comparación de tiempos de ejecución', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('Entrega/tiempo_ejecucion.png', dpi=300)

    # Análisis de resultados
    print('\n================ ANÁLISIS DE RESULTADOS ================')
    for i, resultado in enumerate(resultados):
        print(f"\n>> Para N={resultado['N']}:")
        print(f"  Calidad de la solución:")
        print(f"  - Tiempo entrega Greedy: {resultado['Tiempo_Greedy']:.2f}")
        print(f"  - Tiempo entrega Búsqueda Local: {resultado['Tiempo_Búsqueda_Local']:.2f}")
        print(f"  - Mejora: {resultado['Mejora (%)']}%")
        print(f"  Eficiencia computacional:")
        print(f"  - Tiempo ejecución Greedy: {tiempos_ejecucion[i]['Tiempo_Ejecución_Greedy']:.4f} segundos")
        print(
            f"  - Tiempo ejecución Búsqueda Local: {tiempos_ejecucion[i]['Tiempo_Ejecución_Búsqueda_Local']:.4f} segundos")

    # Resumen final
    print('\n================ RESUMEN FINAL ================')
    print(
        f"- Greedy es {df_tiempos['Tiempo_Ejecución_Búsqueda_Local'].mean() / df_tiempos['Tiempo_Ejecución_Greedy'].mean():.2f}x más rápido en ejecución que Búsqueda Local")
    print(f"- Búsqueda Local produce soluciones {df_resultados['Mejora (%)'].mean():.2f}% mejores en promedio")
    print(f"- Experimento realizado para tamaños de conjunto: {tamaños}")
    print(f"- Cada experimento repetido {repeticiones} veces para mayor robustez")


if __name__ == "__main__":
    print("=== EXPERIMENTOS DE ASIGNACIÓN DE PAQUETES A CENTROS DE DISTRIBUCIÓN ===")
    print("Repositorio GitHub: https://github.com/ANUAR222/Practica_1_Metaheuristicas")
    print("\nIniciando experimentos...")
    ejecutar_experimentos()
    print("\nExperimentos completados. Resultados guardados en carpeta 'Entrega/'")
