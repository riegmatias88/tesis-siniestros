from database import Database
import folium
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import shapely.geometry
from shapely.geometry import MultiPoint

#def get_user_input():
#    provincia = input("Ingrese provincia: ")
#    departamento = input("Ingrese departamento: ")
#    return provincia, departamento

def fetch_data(db, provincia, departamento):
    query = f"""
    SELECT latitud, longitud 
    FROM siniestro 
    WHERE categoria_del_Siniestro_id in (1,2) 
    AND provincia_desc = '{provincia}' 
    AND departamento_desc = '{departamento}'
    """
    data = db.execute_query(query)
    return data

def configure_dbscan(zona):
    if zona == 'Urbana':
        epsilon = 300 / 6371000  # 300 metros para zona Urbana
    else:
        epsilon = 1000 / 6371000  # 1000 metros para zona Rural
    return DBSCAN(eps=epsilon, min_samples=2, metric='haversine')

def get_zona(db, provincia, departamento):
    query_zona = f"""
    SELECT DISTINCT Siniestro_zona_de_ocurrencia_desc 
    FROM siniestro 
    WHERE categoria_del_Siniestro_id in (1,2) 
    AND provincia_desc = '{provincia}' 
    AND departamento_desc = '{departamento}'
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


def run_clustering_zonas(provincia, departamento):
    db = Database()
    #provincia, departamento = get_user_input()
    data = fetch_data(db, provincia, departamento)

    if data is not None and not data.empty:
        data[['latitud', 'longitud']] = data[['latitud', 'longitud']].astype(float)
        coordinates = np.radians(data[['latitud', 'longitud']].values)
        zona = get_zona(db, provincia, departamento)
        dbscan = configure_dbscan(zona)
        clusters = dbscan.fit_predict(coordinates)
        data['cluster'] = clusters
        map = create_map(data)
        add_cluster_polygons_to_map(map, data)
        map.save('static/clusteringmap_perimetro.html')
        print("Top Clusters por cantidad de siniestros:")
        cluster_counts = data['cluster'].value_counts()
        for cluster, count in cluster_counts.items():
            if cluster != -1:
                print(f"Cluster {cluster}: {count} siniestros")
    else:
        print("No data returned from query or empty DataFrame")