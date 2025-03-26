import pandas as pd
import numpy as np
import os

# Función para cargar datos desde un archivo CSV
def cargar_datos(ruta_archivo):
    """
    Carga un conjunto de datos desde un archivo CSV y genera coordenadas GPS para paquetes y centros.
    
    Parámetros:
    ruta_archivo (str): Ruta del archivo CSV que contiene los datos.
    
    Retorna:
    paquetes (DataFrame): DataFrame con los datos de los paquetes.
    centros (DataFrame): DataFrame con los datos de los centros.
    """
    # Cargar el dataset
    datos = pd.read_csv(ruta_archivo)
    
    # Generar coordenadas GPS para paquetes y centros
    N = len(datos)
    M = 5  # Número de centros
    paquetes = pd.DataFrame({
        'ID_Paquete': datos['Order_ID'],  # ID único para cada paquete
        'Ubicacion_X': datos['Drop_Latitude'],  # Coordenada X (latitud)
        'Ubicacion_Y': datos['Drop_Longitude'],  # Coordenada Y (longitud)
        'Tiempo_Entrega': datos['Delivery_Time']  # Tiempo de entrega
    })
    centros = pd.DataFrame({
        'ID_Centro': [f'C{i+1}' for i in range(M)],  # ID único para cada centro
        'Ubicacion_X': np.random.uniform(datos['Drop_Latitude'].min(), datos['Drop_Latitude'].max(), M),  # Coordenada X aleatoria
        'Ubicacion_Y': np.random.uniform(datos['Drop_Longitude'].min(), datos['Drop_Longitude'].max(), M),  # Coordenada Y aleatoria
        'Capacidad': np.random.randint(5, 20, M)  # Capacidad aleatoria (entre 5 y 20 paquetes)
    })
    return paquetes, centros

# Función para generar paquetes y centros de distribución
def generar_datos(N=100, M=5, ruta_csv=None):
    """
    Genera un conjunto de datos con paquetes y centros de distribución,
    utilizando un dataset CSV existente o datos sintéticos.

    Parámetros:
    N (int): Número de paquetes (para datos sintéticos).
    M (int): Número de centros de distribución.
    ruta_csv (str, opcional): Ruta al archivo CSV con los datos reales.

    Retorna:
    paquetes (DataFrame): DataFrame con los datos de los paquetes.
    centros (DataFrame): DataFrame con los datos de los centros.
    """
    if ruta_csv and os.path.exists(ruta_csv):
        # Cargar datos desde el CSV
        try:
            datos = pd.read_csv(ruta_csv)

            # Limitar a N filas si es necesario
            if len(datos) > N:
                datos = datos.sample(n=N, random_state=42)

            # Crear DataFrame de paquetes con datos reales
            paquetes = pd.DataFrame({
                'ID_Paquete': datos['Order_ID'],
                'Ubicacion_X': datos['Drop_Latitude'],
                'Ubicacion_Y': datos['Drop_Longitude'],
                'Tiempo_Entrega': datos['Delivery_Time']
            })

            # Crear centros de distribución basados en las ubicaciones de las tiendas
            tiendas_muestra = datos.sample(n=min(M, len(datos)), random_state=42)
            centros = pd.DataFrame({
                'ID_Centro': [f'C{i + 1}' for i in range(len(tiendas_muestra))],
                'Ubicacion_X': tiendas_muestra['Store_Latitude'].values,
                'Ubicacion_Y': tiendas_muestra['Store_Longitude'].values,
                'Capacidad': np.random.randint(5, 20, len(tiendas_muestra))
            })

            print(f"Datos cargados desde {ruta_csv}: {len(paquetes)} paquetes y {len(centros)} centros")
            return paquetes, centros

        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
            print("Generando datos sintéticos como alternativa...")

    # Si no hay archivo o hubo error, generar datos sintéticos
    paquetes = pd.DataFrame({
        'ID_Paquete': [f'P{i + 1}' for i in range(N)],
        'Ubicacion_X': np.random.uniform(0, 100, N),
        'Ubicacion_Y': np.random.uniform(0, 100, N),
        'Tiempo_Entrega': np.random.randint(10, 60, N)
    })

    centros = pd.DataFrame({
        'ID_Centro': [f'C{i + 1}' for i in range(M)],
        'Ubicacion_X': np.random.uniform(0, 100, M),
        'Ubicacion_Y': np.random.uniform(0, 100, M),
        'Capacidad': np.random.randint(5, 20, M)
    })

    print(f"Datos sintéticos generados: {N} paquetes y {M} centros")
    return paquetes, centros

# Generar el conjunto de datos por defecto (N=100, M=5)
# Ejemplo de uso
ruta_csv = "amazon_delivery.csv"
paquetes, centros = generar_datos(ruta_csv=ruta_csv)

# Crear el directorio Entrega si no existe
os.makedirs('Entrega', exist_ok=True)

# Guardar los datos preprocesados
paquetes.to_csv('Entrega/paquetes_preprocesados.csv', index=False)
centros.to_csv('Entrega/centros_preprocesados.csv', index=False)
