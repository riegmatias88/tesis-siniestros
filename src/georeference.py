from database import Database
import folium
import numpy as np
import pandas as pd

def fetch_data(db, provincia, departamento, localidad):
    query = f"""
    SELECT s.latitud, s.longitud 
    FROM siniestro s
    INNER JOIN localidad l ON (s.localidad_id = l.id)
    WHERE s.categoria_del_Siniestro_id in (1,2) 
    AND l.provincia_desc = '{provincia}'
    AND l.departamento_desc = '{departamento}'
    AND l.localidad_desc = '{localidad}'
    """
    data = db.execute_query(query)
    return data

## Main ##
def run_georeference(provincia, departamento, localidad):
    db = Database()
    data = fetch_data(db, provincia, departamento, localidad)

    if data is not None and not data.empty:
        # Asegurarse de que los datos son floats
        data[['latitud', 'longitud']] = data[['latitud', 'longitud']].astype(float)

        # Crear un mapa con Folium en una ubicación central
        center_lat = np.mean(data['latitud'])
        center_lon = np.mean(data['longitud'])
        map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Color fijo para todos los marcadores
        fixed_color = 'blue'

        # Agregar marcadores al mapa
        for idx, row in data.iterrows():
            lat, lon = row['latitud'], row['longitud']
            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(color=fixed_color)
            ).add_to(map)

        # Guardar el mapa en un archivo HTML
        map.save('static/georeferencemap.html')
    else:
        print("No data returned from query or empty DataFrame")

