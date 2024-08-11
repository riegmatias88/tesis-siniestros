from database import Database
import folium
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import sys

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

## Main ##
def run_clustering(provincia, departamento):
    db = Database()
    #provincia, departamento = get_user_input()
    data = fetch_data(db, provincia, departamento)

    if data is not None and not data.empty:
        # Asegurarse de que los datos son floats
        data[['latitud', 'longitud']] = data[['latitud', 'longitud']].astype(float)

        # Preparar los datos para DBSCAN
        coordinates = np.radians(data[['latitud', 'longitud']].values)  # Convertir a radianes para la métrica haversine

        # Configuración de DBSCAN

        query_zona = "SELECT DISTINCT Siniestro_zona_de_ocurrencia_desc FROM siniestro WHERE categoria_del_Siniestro_id in (1,2) AND provincia_desc = %s AND departamento_desc = %s"
        result = db.execute_select_queries(query_zona, (provincia, departamento))

        if result:  # Verifica si result no está vacío
            zona = result[0][0]  # Accede al primer elemento de la primera tupla
            print(f"Zona obtenida: {zona}")
        else:
            zona = None
            print("No se obtuvieron datos para la zona.")

        print(zona)

        if zona == 'Urbana':
            epsilon = 300 / 6371000  # 300 metros de radio por zona Urbana
        else:
            epsilon = 1000 / 6371000  #1000 metros de radio por zona Rural

        dbscan = DBSCAN(eps=epsilon, min_samples=2, metric='haversine')

        # Ajustar el modelo
        clusters = dbscan.fit_predict(coordinates)
        data['cluster'] = clusters  # Añadir la asignación de cluster al DataFrame

        # Contar puntos en cada cluster y obtener top 10
        cluster_counts = data['cluster'].value_counts().reset_index()
        cluster_counts.columns = ['cluster', 'count']
        top_clusters = cluster_counts[cluster_counts['cluster'] != -1].head(10)  # Excluir outliers y obtener top 10
        print("Top 10 Clusters con más siniestros:")
        print(top_clusters)

        # Crear un mapa con Folium en una ubicación central
        center_lat = np.mean(data['latitud'])
        center_lon = np.mean(data['longitud'])
        map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Colores para los clústeres
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

        # Agregar marcadores al mapa
        for idx, row in data.iterrows():
            lat, lon, cluster = row['latitud'], row['longitud'], row['cluster']
            if cluster != -1:  # No añadir marcadores para outliers
                folium.Marker(
                    location=[lat, lon],
                    popup=f'Cluster: {cluster}, Count: {cluster_counts.loc[cluster_counts["cluster"] == cluster, "count"].values[0]}',
                    icon=folium.Icon(color=colors[int(cluster) % len(colors)])  # Usar int() para asegurar un índice entero
                ).add_to(map)

        # Guardar el mapa en un archivo HTML
        map.save('static/clusteringmap.html')
    else:
        print("No data returned from query or empty DataFrame")

