from flask import send_file, jsonify
import pandas as pd
import os
from decimal import Decimal
from datetime import date, timedelta
from database import Database
from siniestro import Siniestro

# Instancia de la base de datos y modelos
db = Database()
siniestro = Siniestro(db)

def export_siniestro():
    print("Exportando siniestros a CSV...")
    try:
        # Obtener los datos de siniestro y convertirlos a DataFrame
        siniestro_tupla = siniestro.get_siniestros()
        print(siniestro_tupla)

        # Convertir las tuplas en un formato compatible con pandas
        formatted_data = [
            [
                field.strftime("%Y-%m-%d") if isinstance(field, date) else
                str(field) if isinstance(field, timedelta) else
                float(field) if isinstance(field, Decimal) else
                field
                for field in record
            ]
            for record in siniestro_tupla
        ]

        # Crear el DataFrame con los datos formateados
        siniestro_df = pd.DataFrame(
            formatted_data, 
            columns=['id', 'fecha', 'hora', 'franja_horaria', 'latitud', 'longitud',
                     'categoria', 'tipo', 'localidad_id', 'via_id', 'participante1',
                     'participante2', 'participante3', 'obstaculizacion1', 'obstaculizacion2',
                     'obstaculizacion3', 'flujo_transito', 'detalle_siniestro_via',
                     'ubicacion_siniestro_via', 'zona']
        )
        
        # Reemplazar valores nulos
        siniestro_df.fillna('', inplace=True)

        # Ruta temporal para guardar el CSV
        csv_path = 'siniestros.csv'
        siniestro_df.to_csv(csv_path, index=False)
        print("Exportación de siniestros completada.")

        # Enviar el archivo CSV si existe
        if os.path.exists(csv_path):
            response = send_file(csv_path, as_attachment=True, download_name="siniestros.csv", mimetype="text/csv")
            os.remove(csv_path)  # Eliminar el archivo temporal después de enviarlo
            return response

    except Exception as e:
        print(f"Error al exportar siniestros: {e}")
        return jsonify({"error": f"Error al exportar siniestros: {str(e)}"}), 500

    # Retorno adicional en caso de que ocurra un error inesperado
    return jsonify({"error": "Ocurrió un error desconocido al exportar siniestros"}), 500

