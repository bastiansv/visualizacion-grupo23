import plotly.graph_objects as go
import json

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

json_path = r"./data_felipe/migracion_interna_2017.json"
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 2) Emigrantes totales por región (valores de la Tabla 4, columna "Emigrantes" en el informe)
emigrants = data["emigrants"]

# 3) Porcentajes de destino principal y secundario (según la Ilustración de flujos del informe)
# Cada entrada es una lista de tuplas: (destino, porcentaje)
flow_destinations = data["flow_destinations"]

# dos conjuntos de nodos: uno para orígenes y otro para destinos.
origin_labels = ["<b>" + r + " (Origen)</b>" for r in regions]
destination_labels = ["<b>" + r + " (Destino)</b>" for r in regions]
labels = origin_labels + destination_labels

# 4) colores para destinos
primary_color = 'rgba(0,128,0,0.6)'      
secondary_color = 'rgba(255,165,0,0.6)'    

# 5) Construir las listas para Sankey: source, target, value y link_colors
source = []
target = []
value = []
link_colors = []

# Número de regiones (n)
n = len(regions)

# Recorrer cada región de origen
for origen, destinos in flow_destinations.items():
    origen_idx = regions.index(origen)  # indice en la lista de orígenes
    total_emigrantes = emigrants[origen]
    
    for i, (destino, pct) in enumerate(destinos):
        destino_idx = regions.index(destino)  # indice en la lista de destinos
        flujo_abs = total_emigrantes * (pct / 100.0)
        
        source.append(origen_idx)         # Nodo de origen 
        target.append(destino_idx + n)      # Nodo de destino 
        value.append(flujo_abs)

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
    title_x=0.5, 
    title_xanchor="center", 
    font_color="black",
    font_size=13,
    title_font_family="Arial Black",
    title_font_color="black",
    margin=dict(l=300, r=300)
)

fig.show()
