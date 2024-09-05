from flask import Flask, render_template, request, jsonify, url_for, session
from database import Database
from clima import Clima
from heatmap import run_heatmap
from georeference import run_georeference
from clustering_perimetro import run_clustering_zonas
from get_recomendation import get_clusters
from via import Via
from localidad import Localidad
import logging
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria y única

db = Database()
clima = Clima(db)
via = Via(db)
localidad = Localidad(db)

# Configurar el registro de depuración
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_clima', methods=['POST'])
def get_clima():
    data = request.get_json()
    app.logger.debug(f'Recibido get_clima: {data}')
    fecha = data['fecha']
    hora = data['hora']
    temperatura = clima.get_temp(fecha, hora)
    precip = clima.get_precip_mm(fecha, hora)
    return jsonify(temperatura=temperatura, precip=precip)

### Cargo provincias, departamentos y localidades en los combos

@app.route('/get_provincias', methods=['GET'])
def get_provincias():
    provincias = ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Ciudad Autónoma de Buenos Aires", "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego"]
    return jsonify({"provincias": provincias})

@app.route('/get_departamentos', methods=['GET'])
def get_departamentos():
    provincia = request.args.get('provincia')
    if provincia:
        departamentos = localidad.get_departamentos(provincia)
        return jsonify({"departamentos": departamentos})
    else:
        return jsonify({"departamentos": []})

@app.route('/get_localidades', methods=['GET'])
def get_localidades():
    provincia = request.args.get('provincia')
    departamento = request.args.get('departamento')
    
    if provincia and departamento:
        localidades = localidad.get_localidades(provincia, departamento)
        return jsonify({"localidades": localidades})
    else:
        return jsonify({"localidades": []})


### Mapa de calor

@app.route('/formheatmap')
def formheatmap():
    return render_template('formheatmap.html')

@app.route('/run_heatmap', methods=['POST'])
def run_heatmap_route():
    data = request.get_json()
    app.logger.debug(f'Recibido run_heatmap: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    localidad = data['localidad']
    run_heatmap(provincia, departamento, localidad)
    return jsonify(status="Mapa generado", file_url=url_for('static', filename='heatmap.html'))

### Georreferencia

@app.route('/formgeoreference')
def formgeolocalizacion():
    return render_template('formgeoreference.html')

@app.route('/run_georeference', methods=['POST'])
def georreferenciar():
    data = request.get_json()
    app.logger.debug(f'Recibido run_georeference: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    localidad = data['localidad']
    run_georeference(provincia, departamento, localidad)
    return jsonify(status="Mapa generado", file_url=url_for('static', filename='georeferencemap.html'))

### Agrupar zonas

@app.route('/formagruparzonas')
def formagruparzonas():
    return render_template('formagruparzonas.html')

@app.route('/run_clustering_zonas', methods=['POST'])
def clustering_zonas():
    data = request.get_json()
    app.logger.debug(f'Recibido run_clustering_zonas: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    localidad = data['localidad']
    run_clustering_zonas(provincia, departamento, localidad)
    return jsonify(status="Mapa generado", file_url=url_for('static', filename='clusteringmap_perimetro.html'))

### get material via

@app.route('/get_material', methods=['POST'])
def get_material():
    data = request.get_json()
    app.logger.debug(f'Recibido get_material: {data}')
    calle = data['calle']
    altura = data['altura']
    ciudad = data['ciudad']
    material = via.get_material(calle, altura, ciudad)
    return jsonify(material=material)

### Form in-situ

@app.route('/forminsitu_menu')
def forminsitu_menu():
    session.clear()
    return render_template('forminsitu_menu.html')

@app.route('/forminsitu')
def forminsitu():
    session.clear()
    return render_template('forminsitu.html')

@app.route('/forminsitu2')
def forminsitu2():
    session.clear()
    return render_template('forminsitu2.html')

### Recomendacion

@app.route('/formrecomendacion')
def formrecomendacion():
    session.clear()
    return render_template('formrecomendacion.html')

@app.route('/get_clusters', methods=['GET'])
def get_clusters_route():
    provincia = request.args.get('provincia')
    departamento = request.args.get('departamento')
    localidad = request.args.get('localidad')

    if not provincia or not departamento or not localidad:
        return jsonify({"error": "Faltan parámetros: provincia, departamento, localidad"}), 400

    # Llama a la función get_clusters con los parámetros recibidos
    cluster_data = get_clusters(provincia, departamento, localidad)
    print(cluster_data)

    if cluster_data:
        return jsonify(cluster_data)  # Retorna los clústeres como JSON
    else:
        return jsonify({"error": "No se encontraron clústeres"}), 404

### Logout

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)
