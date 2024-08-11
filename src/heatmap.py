import pandas as pd
import folium
from folium.plugins import HeatMap
from database import Database
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
def run_heatmap(provincia, departamento):
    db = Database()
    #provincia, departamento = get_user_input()
    df = fetch_data(db, provincia, departamento)

    #df = db.execute_query(query)

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
