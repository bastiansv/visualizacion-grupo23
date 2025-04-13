import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
import pandas as pd
import json

# ---------------------------------------------
# Datos: Población, Área y Nombres acortados
# (valores en km²)
# ---------------------------------------------
json_path = r"./data_felipe/densidad_poblacional_2024.json"
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Asignar a variables
poblacion_por_region = data['poblacion_por_region']
area_por_region = data['area_por_region']

nombre_regiones_acortados = {
    "Arica y Parinacota": "Arica y Parinacota",
    "Tarapacá": "Tarapacá",
    "Antofagasta": "Antofagasta",
    "Atacama": "Atacama",
    "Coquimbo": "Coquimbo",
    "Valparaíso": "Valparaíso",
    "Metropolitana de Santiago": "Metropolitana",
    "Libertador General Bernardo O'Higgins": "O'Higgins",
    "Maule": "Maule",
    "Ñuble": "Ñuble",
    "Biobío": "Biobío",
    "La Araucanía": "Araucanía",
    "Los Ríos": "Ríos",
    "Los Lagos": "Lagos",
    "Aysén del General Carlos Ibáñez del Campo": "Aysén",
    "Magallanes y de la Antártica Chilena": "Magallanes",
}

# ---------------------------------------------
# Cálculo de la densidad poblacional (hab/km²)
# ---------------------------------------------
densidad_por_region = {
    region: round(poblacion_por_region[region] / area_por_region[region], 2)
    for region in poblacion_por_region
}

df = pd.DataFrame({
    'region': list(densidad_por_region.keys()),
    'densidad': list(densidad_por_region.values()),
    'numero': ["XV", "I", "II", "III", "IV", "V", "RM", "VI", "VII", "XVI", "VIII", "IX", "XIV", "X", "XI", "XII"]
})

# ---------------------------------------------
# Cálculo de anchos de pétalos (en radianes)
# Basado en el área de cada región
# ---------------------------------------------
area_total = sum(area_por_region.values())
anchos = []
for region in df['region']:
    ancho = (area_por_region[region] / area_total) * 2 * np.pi
    anchos.append(ancho)
anchos = np.array(anchos)

# Calcular ángulos de inicio usando la suma acumulada de los anchos
theta_starts = np.concatenate(([0], np.cumsum(anchos)[:-1]))

# ---------------------------------------------
# Creación del gráfico polar
# ---------------------------------------------
plt.figure(figsize=(14, 12), facecolor='white')
ax = plt.subplot(111, polar=True)

# Configurar colormap
cmap = plt.cm.viridis
norm = mcolors.LogNorm(vmin=df['densidad'].min(), vmax=df['densidad'].max())

# ---------------------------------------------
# Dibujar cada pétalo y colocar la etiqueta en el borde exterior
# ---------------------------------------------
for i, (_, row) in enumerate(df.iterrows()):
    theta_inicio = theta_starts[i]
    ancho_petalo = anchos[i]
    
    # Calcular la altura del pétalo en función de la densidad
    r = 0.2 + 0.8 * (row['densidad'] / df['densidad'].max())
    color = cmap(norm(row['densidad']))
    
    # Dibujar el sector (pétalo) usando align='edge'
    ax.bar(theta_inicio, r, width=ancho_petalo, bottom=0.1, alpha=0.8,
           color=color, edgecolor='white', linewidth=1, align="edge")
    
    # Calcular el ángulo central del sector
    theta_centro = theta_inicio + ancho_petalo / 2
    
    # Posición en el borde exterior: radio = bottom + r
    r_texto = 0.12 + r
    
    # Calcular rotación en grados para alinear el texto tangencialmente
    angle_deg = np.degrees(theta_centro) - 90
    
    # Colocar la etiqueta (número romano) en el borde exterior del pétalo
    ax.text(theta_centro, r_texto, row['numero'],
            color='black', fontweight='bold', ha='center', va='center',
            fontsize=10, rotation=angle_deg, rotation_mode='anchor')

# ---------------------------------------------
# Ajustes del gráfico
# ---------------------------------------------
plt.title('Densidad Poblacional por Región de Chile', fontsize=20, pad=20)
ax.set_xticklabels([])
ax.set_yticklabels([])

# Agregar círculo central y etiqueta
circle = plt.Circle((0, 0), 0.1, transform=ax.transData._b, color='#333333', alpha=0.7)
ax.add_artist(circle)
ax.text(0, 0, "CHILE", ha='center', va='center', fontsize=12,
        fontweight='bold', color='white')

# Barra de color
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.6, pad=0.05)
cbar.set_label('Densidad (hab/km²)', fontsize=12)

# ---------------------------------------------
# Crear leyenda
# ---------------------------------------------
handles = []
labels = []
for i, (_, row) in enumerate(df.iterrows()):
    label = f"{row['numero']}. {nombre_regiones_acortados[row['region']]} \n{row['densidad']} hab/km² \n{area_por_region[row['region']]} km²"

    color = cmap(norm(row['densidad']))
    handle = plt.Line2D([0], [0], marker='o', color='w', label=label,
                        markerfacecolor=color, markersize=10)
    handles.append(handle)
    labels.append(label)

ax.legend(handles=handles, labels=labels, loc='best', bbox_to_anchor=(-0, 1),
          fontsize=9, frameon=False, ncol=1)

plt.show()
