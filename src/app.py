from flask import Flask, render_template, request, jsonify, url_for, session
from database import Database
from clima import Clima
from heatmap import run_heatmap
from clustering import run_clustering
from clustering_perimetro import run_clustering_zonas
from via import Via
import logging
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria y única

db = Database()
clima = Clima(db)
via = Via(db)

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

@app.route('/formheatmap')
def formheatmap():
    return render_template('formheatmap.html')

@app.route('/run_heatmap', methods=['POST'])
def run_heatmap_route():
    data = request.get_json()
    app.logger.debug(f'Recibido run_heatmap: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    run_heatmap(provincia, departamento)
    return jsonify(status="Mapa de calor generado", file_url=url_for('static', filename='heatmap.html'))


@app.route('/run_clustering', methods=['POST'])
def clustering():
    data = request.get_json()
    app.logger.debug(f'Recibido run_clustering: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    run_clustering(provincia, departamento)
    return jsonify(status="Clustering generado", file_url=url_for('static', filename='clusteringmap.html'))

@app.route('/run_clustering_zonas', methods=['POST'])
def clustering_zonas():
    data = request.get_json()
    app.logger.debug(f'Recibido run_clustering_zonas: {data}')
    provincia = data['provincia']
    departamento = data['departamento']
    run_clustering_zonas(provincia, departamento)
    return jsonify(status="Clustering zonas generado", file_url=url_for('static', filename='clusteringmap_perimetro.html'))

@app.route('/get_material', methods=['POST'])
def get_material():
    data = request.get_json()
    app.logger.debug(f'Recibido get_material: {data}')
    calle = data['calle']
    altura = data['altura']
    ciudad = data['ciudad']
    material = via.get_material(calle, altura, ciudad)
    return jsonify(material=material)

@app.route('/forminsitu')
def forminsitu():
    session.clear()
    return render_template('forminsitu.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)
