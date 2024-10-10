from flask import Flask, render_template, request, jsonify, url_for, session
#from requests import post
from durable.lang import post
from database import Database
from clima import Clima
from heatmap import run_heatmap
from georeference import run_georeference
from clustering_perimetro import run_clustering_zonas
from get_recomendation import get_clusters
from via import Via
from localidad import Localidad
from rules import load_rules, run_assert_facts
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
logger = logging.getLogger(__name__)

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

@app.route('/forminsitu1')
def forminsitu1():
    session.clear()
    return render_template('forminsitu1.html')

@app.route('/forminsitu2')
def forminsitu2():
    session.clear()
    return render_template('forminsitu2.html')

@app.route('/load_form_data', methods=['POST'])
def load_form_data():
    # Capturar los datos del formulario
    nombre = request.form.get('nombrevia')
    altura = request.form.get('alturavia')
    tipo = request.form.get('tipovia')
    material = request.form.get('materialvia')
    estado = request.form.get('estadovia')
    limpieza = request.form.get('limpieza')    
    luminaria = request.form.get('luminaria')
    iluminacion_uniforme = request.form.get('iluminacion-uniforme')
    veredas_optimas = request.form.get('veredas-optimas')
    carril_omnibus = request.form.get('carril-omnibus')
    senalizacion_paradas = request.form.get('senalizacion-paradas')
    ciclovia = request.form.get('ciclovia')
    chicana = request.form.get('chicana')
    bandas_reductoras = request.form.get('bandas-reductoras')
    reductor_velocidad = request.form.get('reductor-velocidad')
    mini_rotonda = request.form.get('mini-rotonda')
    meseta_elevada = request.form.get('meseta-elevada')
    isleta_giro = request.form.get('isleta-giro')
    demarcacion_separacion_carriles = request.form.get('demarcacion-separacion-carriles')
    demarcacion_doble_sentido = request.form.get('demarcacion-doble-sentido')
    demarcacion_visible = request.form.get('demarcacion-visible')
    senial_advertencia = request.form.get('senial-advertencia')
    senial_reglamentaria = request.form.get('senial-reglamentaria')
    senial_maximo = request.form.get('senial-maximo')
    senial_informativa = request.form.get('senial-informativa')
    senial_calle_nomenclada = request.form.get('senial-calle-nomenclada')
    senial_obstaculiza = request.form.get('senial-obstaculizada')
    senial_redundante = request.form.get('senial-redundante')
    vias_distinta_superficie = request.form.get('vias-distinta-superficie')
    interseccion_multiple = request.form.get('interseccion-multiple')
    visualizacion_cruce = request.form.get('visualizacion-cruce')
    obstruccion_visual = request.form.get('obstruccion-visual')
    peatones_visibles = request.form.get('peatones-visibles')
    iluminacion_obstaculizada = request.form.get('iluminacion-obstaculizada')
    reductores_velocidad_cruce = request.form.get('reductores-velocidad-cruce')
    badenes_canaletas = request.form.get('badenes-canaletas')
    objetos_rigidos = request.form.get('objetos-rigidos')
    sendas_peatonales = request.form.get('sendas-peatonales')
    lineas_pare = request.form.get('lineas-pare')
    cordones_pintados = request.form.get('cordones-pintados')
    senial_cruce_peatones = request.form.get('senial-cruce-peatones')
    limitacion_velocidad = request.form.get('limitacion-velocidad')
    senial_pare = request.form.get('senial-pare')
    senial_cruce = request.form.get('senial-cruce')
    senial_ciclovia = request.form.get('senial-ciclovia')
    senial_reductores = request.form.get('senial-reductores')
    paradas_seguras = request.form.get('paradas-seguras')
    obstruccion_carteleria = request.form.get('obstruccion-carteleria')
    estado_carteleria = request.form.get('estado-carteleria')
    senial_transitoria = request.form.get('senial-transitoria')
    ceda_el_paso = request.form.get('ceda-el-paso')
    cruces_peatonales_rot = request.form.get('cruces-peatonales-rot')
    senalizacion_rotonda = request.form.get('senalizacion-rotonda')
    semaforo_vehicular = request.form.get('semaforo-vehicular')
    semaforo_peatonal = request.form.get('semaforo-peatonal')
    semaforo_ciclistas = request.form.get('semaforo-ciclistas')
    polvo = request.form.get('polvo')
    zanjas = request.form.get('zanjas')
    zanjas_contencion = request.form.get('zanjas_contencion')

    localidad_id = 1 # queda pendiente buscar localidad_id

    #muestro todos los valores capturados en el form
    print(request.form)

    if not nombre or not altura or not tipo or not material or not estado:
        return "Faltan especificar campos", 400
    
    if material == "4" or material == "5": 
        print("Ejecuto set_via para vias de tierra o ripio")
        via.set_via_tierra(nombre, altura, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_obstaculiza, estado_carteleria, senial_transitoria, vias_distinta_superficie, obstruccion_visual, reductores_velocidad_cruce, objetos_rigidos, paradas_seguras, peatones_visibles, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, senial_calle_nomenclada, polvo, zanjas, zanjas_contencion, localidad_id)
        return jsonify(status="Calle tierra cargada ")
    else:
        print("Ejecuto set_via para vias pavimentadas")
        via.set_via_pavimento(nombre, altura, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, carril_omnibus, senalizacion_paradas, ciclovia, chicana, bandas_reductoras, reductor_velocidad, mini_rotonda, meseta_elevada, isleta_giro, demarcacion_separacion_carriles, demarcacion_doble_sentido, demarcacion_visible, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_calle_nomenclada, senial_obstaculiza, senial_redundante, vias_distinta_superficie, interseccion_multiple, visualizacion_cruce, obstruccion_visual, peatones_visibles, iluminacion_obstaculizada, reductores_velocidad_cruce, badenes_canaletas, objetos_rigidos, sendas_peatonales, lineas_pare, cordones_pintados, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, paradas_seguras, obstruccion_carteleria, estado_carteleria, senial_transitoria, ceda_el_paso, cruces_peatonales_rot, senalizacion_rotonda, semaforo_vehicular, semaforo_peatonal, semaforo_ciclistas, localidad_id) # agregar manejo de exceptions
        return jsonify(status="Registro cargado")
    
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



# Cargar las reglas
load_rules()

# Ruta en Flask para enviar parámetros y activar reglas
@app.route('/advice', methods=['POST'])
def advice_rule():

    data = request.get_json()  # Obtener los datos enviados en el body de la petición
    
    # Verificar si existen los campos 'Vehiculo', 'Via', 'Siniestro'
    vehiculo_data = data.get('Vehiculo', {})
    via_data = data.get('Via', {})
    siniestro_data = data.get('Siniestro', {})
    clima_data = data.get('Clima', {})

    # Preparar los datos para el motor de reglas, solo si existen
    post_data = {}

    if vehiculo_data:
        post_data['Vehiculo'] = {
            'Tipo': vehiculo_data.get('Tipo') if vehiculo_data.get('Tipo') is not None else ''
        }

    if siniestro_data:
        post_data['Siniestro'] = {
            'Flujo_de_transito': siniestro_data.get('Flujo_de_transito') if siniestro_data.get('Flujo_de_transito') is not None else '',
            'Obstaculizacion1': siniestro_data.get('Obstaculizacion1') if siniestro_data.get('Obstaculizacion1') is not None else '',
            'Obstaculizacion2': siniestro_data.get('Obstaculizacion2') if siniestro_data.get('Obstaculizacion2') is not None else '',
            'Obstaculizacion3': siniestro_data.get('Obstaculizacion3') if siniestro_data.get('Obstaculizacion3') is not None else '',
            'Detalle_siniestro_via': siniestro_data.get('Detalle_siniestro_via') if siniestro_data.get('Detalle_siniestro_via') is not None else '',
            'Ubicacion_siniestro_via': siniestro_data.get('Ubicacion_siniestro_via') if siniestro_data.get('Ubicacion_siniestro_via') is not None else '',
            'Tipo': siniestro_data.get('Tipo') if siniestro_data.get('Tipo') is not None else '',
            'Zona': siniestro_data.get('Zona') if siniestro_data.get('Zona') is not None else '',
            'Franja_horaria': siniestro_data.get('Franja_horaria') if siniestro_data.get('Franja_horaria') is not None else ''
        }

    if via_data:
        post_data['Via'] = {
            'Ciclovia': via_data.get('Ciclovia') if via_data.get('Ciclovia') is not None else 'no',
            'Cruce_peatonal': via_data.get('Cruce_peatonal') if via_data.get('Cruce_peatonal') is not None else 'no',
            'Semaforo_peatonal': via_data.get('Semaforo_peatonal') if via_data.get('Semaforo_peatonal') is not None else 'no',
            'Reductor_velocidad': via_data.get('Reductor_velocidad') if via_data.get('Reductor_velocidad') is not None else 'no',
            'Senializacion_vertical': via_data.get('Senializacion_vertical') if via_data.get('Senializacion_vertical') is not None else 'no',
            'Senializacion_horizontal': via_data.get('Senializacion_horizontal') if via_data.get('Senializacion_horizontal') is not None else 'no',
            'Senializacion_temporal': via_data.get('Senializacion_temporal') if via_data.get('Senializacion_temporal') is not None else 'no',
            'Ferrovia': via_data.get('Ferrovia') if via_data.get('Ferrovia') is not None else 'no',
            'Esquina_cordon_amarillo': via_data.get('Esquina_cordon_amarillo') if via_data.get('Esquina_cordon_amarillo') is not None else 'no',
            'Semaforo_vehicular': via_data.get('Semaforo_vehicular') if via_data.get('Semaforo_vehicular') is not None else 'no',
            'Visibilidad': via_data.get('Visibilidad') if via_data.get('Visibilidad') is not None else '',
            'Limpieza': via_data.get('Limpieza') if via_data.get('Limpieza') is not None else '',
            'Tipo': via_data.get('Tipo') if via_data.get('Tipo') is not None else '',
            'Material': via_data.get('Material') if via_data.get('Material') is not None else '',
            'Cuneta': via_data.get('Cuneta') if via_data.get('Cuneta') is not None else '',
            'Estado': via_data.get('Estado') if via_data.get('Estado') is not None else '',
            'Zona': via_data.get('Zona') if via_data.get('Zona') is not None else ''
        }

    if clima_data:
        post_data['Clima'] = {
            'Visibilidad': clima_data.get('Visibilidad') if clima_data.get('Visibilidad') is not None else '',
            'Precipitaciones': clima_data.get('Precipitaciones') if clima_data.get('Precipitaciones') is not None else '',
            'Viento': clima_data.get('Viento') if clima_data.get('Viento') is not None else '',
            'Temperatura': clima_data.get('Temperatura') if clima_data.get('Temperatura') is not None else ''            
        }

    # Enviar los datos al motor de reglas
    try:
        print(post_data)
        run_assert_facts(post_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "Reglas evaluadas correctamente"})

### Logout

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)
