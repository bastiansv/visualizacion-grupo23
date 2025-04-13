import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.patches import Patch

# 1. Cargar el dataset temporal JSON
json_path = r".\data_basti\nacimientos_temporal_regiones_2009_2021.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Convertir los datos a un DataFrame
years = [str(year) for year in range(2009, 2022)]  # 2009 a 2021
regions = [entry['region'] for entry in data['regiones']]
df = pd.DataFrame(index=years, columns=regions)

for entry in data['regiones']:
    region = entry['region']
    for year, value in entry['nacimientos'].items():
        df.loc[year, region] = value

df = df.astype(float).fillna(0)

# 3. Agrupar regiones pequeñas en "Otras regiones"
small_regions = ['Aysén', 'Magallanes', 'Los Ríos', 'Arica y Parinacota', 'Ñuble', 'Atacama', 'Tarapacá', 'Coquimbo', 'Los Lagos']
df['Otras regiones'] = df[small_regions].sum(axis=1)
df = df.drop(columns=small_regions)
regions = [col for col in df.columns if col not in small_regions]

# 4. Crear un gráfico de horizonte normalizado entre 0 y 1 por región
fig, axes = plt.subplots(len(regions), 1, figsize=(12, 8), sharex=True)

color = '#1f77b4'  # Color único para todas las regiones

for i, region in enumerate(regions):
    ax = axes[i]
    values = df[region].values

    # Normalizar entre 0 y 1
    values_normalized = (values - values.min()) / (values.max() - values.min())

    ax.fill_between(df.index, 0, values_normalized, color=color, alpha=0.8)

    # Añadir el nombre de la región
    ax.text(-0.1, 0.5, region, transform=ax.transAxes, va='center', ha='right', fontsize=10)

    # Ocultar los ejes Y
    ax.set_yticks([])
    ax.set_ylim(0, 1)

# Añadir título y etiquetas
plt.suptitle("Evolución relativa de nacimientos por región en Chile (2009-2021)", fontsize=14)
axes[-1].set_xlabel("Año", fontsize=12)

# Leyenda
fig.legend([Patch(facecolor=color)], ['Nacimientos normalizados (0-1)'], loc='upper right')

# Ajustar el diseño
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Mostrar el gráfico
plt.show()


