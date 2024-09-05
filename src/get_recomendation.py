from database import Database
import folium
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import shapely.geometry
from shapely.geometry import MultiPoint
from flask import jsonify

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

def configure_dbscan(zona):
    if zona == 'Urbana':
        epsilon = 300 / 6371000  # 300 metros para zona Urbana
    else:
        epsilon = 1000 / 6371000  # 1000 metros para zona Rural
    return DBSCAN(eps=epsilon, min_samples=2, metric='haversine')

def get_zona(db, provincia, departamento, localidad):
    query_zona = f"""
    SELECT DISTINCT s.Siniestro_zona_de_ocurrencia_desc 
    FROM siniestro s
    INNER JOIN localidad l ON (s.localidad_id = l.id)
    WHERE s.categoria_del_Siniestro_id in (1,2) 
    AND l.provincia_desc = '{provincia}'
    AND l.departamento_desc = '{departamento}'
    AND l.localidad_desc = '{localidad}'
    """
    result = db.execute_query(query_zona)
    if result.empty:
        print("No se obtuvieron datos para la zona.")
        return None
    return result.iloc[0, 0]

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

def get_clusters(provincia, departamento, localidad):
    db = Database()
    data = fetch_data(db, provincia, departamento, localidad)

    if data is not None and not data.empty:
        data[['latitud', 'longitud']] = data[['latitud', 'longitud']].astype(float)
        coordinates = np.radians(data[['latitud', 'longitud']].values)
        zona = get_zona(db, provincia, departamento, localidad)
        dbscan = configure_dbscan(zona)
        clusters = dbscan.fit_predict(coordinates)
        data['cluster'] = clusters
        map = create_map(data)
        add_cluster_polygons_to_map(map, data)
        #map.save('static/clusteringmap_perimetro.html')
        cluster_counts = data['cluster'].value_counts()
        cluster_data = []
        for cluster, count in cluster_counts.items():
            if cluster != -1:
                if count >= 10:
                    cluster_data.append({"cluster_id": cluster, "count": count})
            
        #print(cluster_data)
        return cluster_data
    else:
        print("No data returned from query or empty DataFrame")