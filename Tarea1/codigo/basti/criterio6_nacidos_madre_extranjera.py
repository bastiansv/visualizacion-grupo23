import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json

# 1. Cargar el dataset JSON con los porcentajes
json_path = r".\data_basti\nacidos_vivos_madre_extranjera_2021.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convertir los datos de las regiones a un DataFrame
df = pd.DataFrame(data['regiones'])

# 2. Cargar el archivo GeoJSON con los límites de las regiones de Chile
gdf = gpd.read_file(r".\data_basti\regiones.json")

# 3. Unir los datos del DataFrame con el GeoDataFrame
gdf = gdf.merge(df, left_on='Region', right_on='region', how='left')

# 5. Crear el mapa coroplético
fig, ax = plt.subplots(1, 1, figsize=(8, 14))  # Ajustamos el tamaño para que sea más alargado
gdf.plot(column='porcentaje', ax=ax, legend=True, cmap='Blues',
         legend_kwds={'label': "Porcentaje de nacidos vivos de madre extranjera (%)",
                      'orientation': "horizontal",
                      'shrink': 0.6},  # Reduce el tamaño de la barra de color
         missing_kwds={'color': 'lightgrey', 'label': 'Datos no disponibles'})

# Añadir título
plt.title("Porcentaje de nacidos vivos de madre extranjera por región, Chile 2021", fontsize=12)

# Ocultar los ejes de coordenadas (latitud y longitud)
ax.set_axis_off()

# Ajustar los límites de los ejes para centrar el mapa (enfocándonos en el territorio continental)
ax.set_xlim(-78, -66)  # Limitar las longitudes al rango de Chile continental
ax.set_ylim(-56, -17)  # Limitar las latitudes al rango de Chile continental

# Ajustar márgenes para centrar el gráfico
plt.tight_layout()

# Mostrar el mapa
plt.show()