import plotly.graph_objects as go

# 1) Lista de regiones (orden base)
regions = [
    "Arica y Parinacota",
    "Tarapacá",
    "Antofagasta",
    "Atacama",
    "Coquimbo",
    "Valparaíso",
    "Metropolitana",
    "O’Higgins",
    "Maule",
    "Ñuble",
    "Biobío",
    "La Araucanía",
    "Los Ríos",
    "Los Lagos",
    "Aysén",
    "Magallanes"
]

# Creamos dos conjuntos de nodos: uno para orígenes y otro para destinos.
origin_labels = ["<b>" + r + " (Origen)</b>" for r in regions]
destination_labels = ["<b>" + r + " (Destino)</b>" for r in regions]
labels = origin_labels + destination_labels

# 2) Emigrantes totales por región (valores de la Tabla 4, columna "Emigrantes")
emigrants = {
    "Arica y Parinacota": 19729,
    "Tarapacá": 36703,
    "Antofagasta": 67462,
    "Atacama": 30328,
    "Coquimbo": 40537,
    "Valparaíso": 92193,
    "Metropolitana": 302078,
    "O’Higgins": 50391,
    "Maule": 47469,
    "Ñuble": 30505,
    "Biobío": 78345,
    "La Araucanía": 53762,
    "Los Ríos": 29972,
    "Los Lagos": 47716,
    "Aysén": 11486,
    "Magallanes": 18418
}

# 3) Porcentajes de destino principal y secundario (según la Ilustración de flujos)
# Cada entrada es una lista de tuplas: (destino, porcentaje)
flow_destinations = {
    "Arica y Parinacota": [("Metropolitana", 26.6), ("Tarapacá", 13.5)],
    "Tarapacá": [("Metropolitana", 25.8), ("Coquimbo", 23.9)],
    "Antofagasta": [("Coquimbo", 25.8), ("Metropolitana", 16.4)],
    "Atacama": [("Coquimbo", 36.9), ("Metropolitana", 17.9)],
    "Coquimbo": [("Metropolitana", 33.2), ("Valparaíso", 19.4)],
    "Valparaíso": [("Metropolitana", 50.2), ("O’Higgins", 6.5)],
    "Metropolitana": [("Valparaíso", 22.8), ("Biobío", 12.0)],
    "O’Higgins": [("Metropolitana", 47.3), ("Valparaíso", 10.6)],
    "Maule": [("Metropolitana", 34.6), ("O’Higgins", 30.2)],
    "Ñuble": [("Metropolitana", 37.9), ("Biobío", 10.8)],
    "Biobío": [("Metropolitana", 39.1), ("Ñuble", 13.8)],
    "La Araucanía": [("Metropolitana", 26.9), ("Biobío", 26.8)],
    "Los Ríos": [("Los Lagos", 28.3), ("Metropolitana", 17.7)],
    "Los Lagos": [("Metropolitana", 22.7), ("Los Ríos", 21.1)],
    "Aysén": [("Los Lagos", 24.4), ("Metropolitana", 22.9)],
    "Magallanes": [("Valparaíso", 24.4), ("Metropolitana", 22.4)]
}

# 4) Definir colores para destinos
primary_color = 'rgba(0,128,0,0.6)'      # Destino principal (mayor)
secondary_color = 'rgba(255,165,0,0.6)'    # Destino secundario

# 5) Construir las listas para Sankey: source, target, value y link_colors
source = []
target = []
value = []
link_colors = []

# Número de regiones (n)
n = len(regions)

# Recorrer cada región de origen
for origen, destinos in flow_destinations.items():
    origen_idx = regions.index(origen)  # Índice en la lista de orígenes
    total_emigrantes = emigrants[origen]
    
    for i, (destino, pct) in enumerate(destinos):
        destino_idx = regions.index(destino)  # Índice en la lista de destinos
        flujo_abs = total_emigrantes * (pct / 100.0)
        
        source.append(origen_idx)         # Nodo de origen (lado izquierdo)
        target.append(destino_idx + n)      # Nodo de destino (lado derecho)
        value.append(flujo_abs)
        
        # Asigna color según posición: el primero es principal, el segundo es secundario.
        if i == 0:
            link_colors.append(primary_color)
        else:
            link_colors.append(secondary_color)

# 6) Crear el diagrama de Sankey con Plotly
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=["rgba(0,0,150,0.3)"] * len(labels)
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors
    )
)])

fig.update_layout(
    title_text="Principales regiones de destino de emigrantes dentro de Chile",
    font_family="Arial Black",
    title_x=0.5,  # Centra el título horizontalmente (0.5 es el centro)
    title_xanchor="center",  # Ancla el título en el centro
    font_color="black",
    font_size=13,
    title_font_family="Arial Black",
    title_font_color="black",
    margin=dict(l=300, r=300)
)

fig.show()
