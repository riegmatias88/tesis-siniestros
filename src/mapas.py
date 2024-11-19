import pandas as pd
import folium
import sys
import numpy as np
import shapely.geometry
from database import Database
from siniestro import Siniestro
from folium.plugins import HeatMap
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint

db = Database()
siniestro = Siniestro(db)

#def fetch_data(db, provincia, departamento, localidad):
#    query = f"""
#    SELECT s.latitud, s.longitud 
#    FROM siniestro s
#    INNER JOIN localidad l ON (s.localidad_id = l.id)
#    WHERE s.categoria_del_Siniestro_id in (1,2) 
#    AND l.provincia_desc = '{provincia}'
#    AND l.departamento_desc = '{departamento}'
#    AND l.localidad_desc = '{localidad}'
#    """
#    data = db.execute_query(query)
#    return data

## Main ##

def run_georeference_by_id(id_siniestro):
    #data = fetch_data(db, provincia, departamento, localidad)
    data = siniestro.get_geo_siniestro_by_id(id_siniestro)

    if isinstance(data, list):
        data = pd.DataFrame(data, columns=["latitud", "longitud"])
        print(data)

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

def run_georeference(provincia, departamento, localidad):
    #data = fetch_data(db, provincia, departamento, localidad)
    data = siniestro.get_siniestro_geo(provincia, departamento, localidad)


    if isinstance(data, list):
        data = pd.DataFrame(data, columns=["latitud", "longitud"])
        print(data)

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


def run_heatmap(provincia, departamento, localidad):
    #provincia, departamento = get_user_input()
    #df = fetch_data(db, provincia, departamento, localidad)

    data = siniestro.get_siniestro_geo(provincia, departamento, localidad)

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data, columns=["latitud", "longitud"])
        print(df)

    if df is None or df.empty:
        print("No se obtuvieron datos de la consulta.")
    else:
        # Imprimir los datos obtenidos
        print("Datos obtenidos de la base de datos:")
        print(df)

        # Filtrar filas con valores no numéricos en las columnas 'latitud' y 'longitud'
        df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
        df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

        # Mostrar filas con valores no numéricos para depuración
        non_numeric_lat = df[df['latitud'].isnull()]
        non_numeric_long = df[df['longitud'].isnull()]

        print("Filas con valores no numéricos en 'latitud':")
        print(non_numeric_lat)
        print("Filas con valores no numéricos en 'longitud':")
        print(non_numeric_long)

        # Imprimir los datos después de la conversión a numérico
        print("Datos después de la conversión a numérico:")
        print(df)

        # Eliminar filas con valores NaN en 'latitud' y 'longitud'
        df = df.dropna(subset=['latitud', 'longitud'])

        # Imprimir los datos después de eliminar filas con NaN
        print("Datos después de eliminar filas con NaN:")
        print(df)

        if df.empty:
            print("No hay datos válidos para mostrar en el mapa de calor.")
        else:
            # Crear un mapa base centrado en el promedio de las coordenadas
            m = folium.Map(location=[df['latitud'].mean(), df['longitud'].mean()], zoom_start=10)

            # Crear los datos para el mapa de calor
            heatmap_data = df[['latitud', 'longitud']].values.tolist()

            # Añadir el HeatMap al mapa base
            #HeatMap(heatmap_data, radius=10, blur=15, max_zoom=10).add_to(m)
            #HeatMap(heatmap_data, radius=10, blur=15, max_zoom=10).add_to(m)
            HeatMap(heatmap_data, radius=12, blur=7, max_zoom=18).add_to(m)


            # Guardar el mapa en un archivo HTML
            m.save('static/heatmap.html')
            print("El mapa de calor se ha guardado como 'heatmap.html'.")

def configure_dbscan(zona):
    #if zona == 'Urbana':
    #    epsilon = 300 / 6371000  # 300 metros para zona Urbana
    #else:
    #    epsilon = 1000 / 6371000  # 1000 metros para zona Rural
    if zona == 'rural':
        epsilon = 1000 / 6371000  # 1000 metros para zona Rural
    else:
        epsilon = 300 / 6371000  # 300 metros para zona comercial, residencial o escolar
    return DBSCAN(eps=epsilon, min_samples=2, metric='haversine')

#def get_zona_old(db, provincia, departamento, localidad):
#    query_zona = f"""
#    SELECT DISTINCT s.Siniestro_zona_de_ocurrencia_desc 
#    FROM siniestro s
#    INNER JOIN localidad l ON (s.localidad_id = l.id)
#    WHERE s.categoria_del_Siniestro_id in (1,2) 
#    AND l.provincia_desc = '{provincia}'
#    AND l.departamento_desc = '{departamento}'
#    AND l.localidad_desc = '{localidad}'
#    """
#    result = db.execute_query(query_zona)
#    if result.empty:
#        print("No se obtuvieron datos para la zona.")
#        return None
#    return result.iloc[0, 0]

def create_map(data):
    center_lat = np.mean(data['latitud'])
    center_lon = np.mean(data['longitud'])
    map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    return map

def add_cluster_polygons_to_map(map, data):
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    cluster_counts = data['cluster'].value_counts()  # Conteo de puntos por cluster

    for cluster in data['cluster'].unique():
        if cluster != -1:
            cluster_points = data[data['cluster'] == cluster][['latitud', 'longitud']]
            polygon = MultiPoint(cluster_points.values).convex_hull
            num_siniestros = cluster_counts[cluster]
            cluster_label = f"Cluster {cluster}: {num_siniestros} siniestros"  # Incluye la cantidad en el label

            # Verificar si el resultado es un Polygon para dibujar
            if isinstance(polygon, shapely.geometry.Polygon):
                folium.Polygon(
                    locations=[(lat, lon) for lat, lon in polygon.exterior.coords],
                    color=colors[int(cluster) % len(colors)],
                    fill=True,
                    fill_opacity=0.5,
                    popup=cluster_label
                ).add_to(map)
            elif isinstance(polygon, shapely.geometry.LineString):
                folium.PolyLine(
                    locations=[(lat, lon) for lat, lon in polygon.coords],
                    color=colors[int(cluster) % len(colors)],
                    weight=5,
                    popup=cluster_label
                ).add_to(map)
            elif isinstance(polygon, shapely.geometry.Point):
                folium.Marker(
                    location=[polygon.y, polygon.x],
                    icon=folium.Icon(color=colors[int(cluster) % len(colors)]),
                    popup=cluster_label
                ).add_to(map)

def run_clustering_zonas(provincia, departamento, localidad):
    #db = Database()
    #data = fetch_data(db, provincia, departamento, localidad)

    data = siniestro.get_siniestro_geo(provincia, departamento, localidad)

    if isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data, columns=["latitud", "longitud"])
        print(df)

    if df is not None and not df.empty:
        df[['latitud', 'longitud']] = df[['latitud', 'longitud']].astype(float)
        coordinates = np.radians(df[['latitud', 'longitud']].values)
        #zona = get_zona(db, provincia, departamento, localidad)
        zona = siniestro.get_siniestro_zona(provincia, departamento, localidad)
        print(zona)
        dbscan = configure_dbscan(zona)
        clusters = dbscan.fit_predict(coordinates)
        df['cluster'] = clusters
        map = create_map(df)
        add_cluster_polygons_to_map(map, df)
        map.save('static/clusteringmap_perimetro.html')
    else:
        print("No data returned from query or empty DataFrame")    
