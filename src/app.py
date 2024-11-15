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
from siniestro import Siniestro
from recomendacion import Recomendacion
from rules import load_rules, run_assert_facts
from datetime import datetime
import logging
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria y única

db = Database()
clima = Clima(db)
via = Via(db)
localidad = Localidad(db)
siniestro = Siniestro(db)
recomendacion = Recomendacion(db)

# Configurar el registro de depuración
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/modal')
def mostrar_modal():
    return render_template('modal.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

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

#######################################################################################
#                              Endpoint load_form_data
#######################################################################################

@app.route('/load_form_data', methods=['POST'])
def load_form_data():
    # Capturar los datos del formulario
    nombre = request.form.get('nombrevia')
    altura = request.form.get('alturavia')
    entre_calle1 = request.form.get('entrecalle1')
    entre_calle2 = request.form.get('entrecalle2')
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
        via.set_via_tierra(nombre, altura, entre_calle1, entre_calle2, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_obstaculiza, estado_carteleria, senial_transitoria, vias_distinta_superficie, obstruccion_visual, reductores_velocidad_cruce, objetos_rigidos, paradas_seguras, peatones_visibles, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, senial_calle_nomenclada, polvo, zanjas, zanjas_contencion, localidad_id)
        return jsonify(status="Calle tierra cargada ")
    else:
        print("Ejecuto set_via para vias pavimentadas")
        via.set_via_pavimento(nombre, altura, entre_calle1, entre_calle2, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, carril_omnibus, senalizacion_paradas, ciclovia, chicana, bandas_reductoras, reductor_velocidad, mini_rotonda, meseta_elevada, isleta_giro, demarcacion_separacion_carriles, demarcacion_doble_sentido, demarcacion_visible, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_calle_nomenclada, senial_obstaculiza, senial_redundante, vias_distinta_superficie, interseccion_multiple, visualizacion_cruce, obstruccion_visual, peatones_visibles, iluminacion_obstaculizada, reductores_velocidad_cruce, badenes_canaletas, objetos_rigidos, sendas_peatonales, lineas_pare, cordones_pintados, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, paradas_seguras, obstruccion_carteleria, estado_carteleria, senial_transitoria, ceda_el_paso, cruces_peatonales_rot, senalizacion_rotonda, semaforo_vehicular, semaforo_peatonal, semaforo_ciclistas, localidad_id) # agregar manejo de exceptions
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
    #cluster_data = get_clusters(provincia, departamento, localidad)
    cluster_data = get_siniestros(provincia, departamento, localidad)
    print(cluster_data)

    if cluster_data:
        return jsonify(cluster_data)  # Retorna los clústeres como JSON
    else:
        return jsonify({"error": "No se encontraron clústeres"}), 404

#######################################################################################
#                              Endpoint get_siniestros
#######################################################################################

@app.route('/get_siniestros')
def get_siniestros():
    provincia = request.args.get('provincia')
    departamento = request.args.get('departamento')
    localidad = request.args.get('localidad')

    if not provincia or not departamento or not localidad:
        return jsonify({"error": "Faltan parámetros: provincia, departamento o localidad"}), 400
    
    try:
        siniestro_tupla = siniestro.get_siniestro_by_ubicacion(provincia,departamento,localidad)
        siniestro_data = [
                {
                    "Id": siniestro[0],
                    "Fecha": str(siniestro[1]),
                    "Hora": str(siniestro[2]),
                    "Tipo": siniestro[3],
                    "Categoria": siniestro[4],
                    "Calle": siniestro[5],
                    "Altura": siniestro[6],
                    "Entre_calle1": siniestro[7],
                    "Entre_calle2": siniestro[8],
                    "Analizado": recomendacion.has_recomendacion(siniestro[0])
                } 
                for siniestro in siniestro_tupla
            ]
        print(siniestro_data)
        return jsonify({"siniestros": siniestro_data}),200
    
    except Exception as e:
        return jsonify({"error": f"Error al obtener siniestros: {str(e)}"}), 500


# Cargar las reglas
load_rules()

#######################################################################################
#                              Endpoint advice
#######################################################################################

# Ruta en Flask para enviar parámetros y activar reglas
@app.route('/advice', methods=['POST'])
def advice_rule():

    siniestro_id = request.args.get('siniestro_id', type=int)
    if not siniestro_id:
        return jsonify({"error": "Faltan parámetros: siniestro_id"}), 400

    #via_id = request.args.get('via_id', type=int)
    #if not via_id:
    #    return jsonify({"error": "Faltan parámetros: via_id"}), 400

    #id_siniestro = 5 #este id luego tiene que venir en el POST
    #id_via = 2 #este id luego tiene que venir en el POST

    data = request.get_json()  # Obtener los datos enviados en el body de la petición
    
    print(data)

    # Verificar si existen los campos 'Vehiculo', 'Via', 'Siniestro', 'Clima'
    via_data = data.get('Via', {})
    siniestro_data = data.get('Siniestro', {})
    clima_data = data.get('Clima', {})

    #Busco los datos de siniestros en la base de datos
    siniestro_data = siniestro.get_siniestro_by_id(siniestro_id)
    siniestro_data = siniestro_data[0]
    #id_via = siniestro_data[9]




    # Preparar los datos para el motor de reglas, solo si existen
    post_data = {}

    if siniestro_data:
        post_data['Siniestro'] = {
            'Id': siniestro_data[0] if siniestro_data[0] is not None else '',
            'Fecha': str(siniestro_data[1]) if siniestro_data[1] is not None else '',
            'Hora': str(siniestro_data[2]) if siniestro_data[2] is not None else '',
            'Franja_horaria': siniestro_data[3] if siniestro_data[3] is not None else '',
            #'Latitud': float(siniestro_data[4]) if siniestro_data[4] is not None else '',
            #'Longitud': float(siniestro_data[5]) if siniestro_data[5] is not None else '',
            'Categoria': siniestro_data[6] if siniestro_data[6] is not None else '',
            'Tipo': siniestro_data[7] if siniestro_data[7] is not None else '',
            'Localidad_id': siniestro_data[8] if siniestro_data[8] is not None else '',
            'Via_id': siniestro_data[9] if siniestro_data[9] is not None else '',
            'Participante1': siniestro_data[10] if siniestro_data[10] is not None else '',
            'Participante2': siniestro_data[11] if siniestro_data[11] is not None else '',
            'Participante3': siniestro_data[12] if siniestro_data[12] is not None else '',
            'Obstaculizacion1': siniestro_data[13] if siniestro_data[13] is not None else '',
            'Obstaculizacion2': siniestro_data[14] if siniestro_data[14] is not None else '',
            'Obstaculizacion3': siniestro_data[15] if siniestro_data[15] is not None else '',
            'Flujo_transito': siniestro_data[16] if siniestro_data[16] is not None else '',
            'Detalle_siniestro_via': siniestro_data[17] if siniestro_data[17] is not None else '',
            'Ubicacion_siniestro_via': siniestro_data[18] if siniestro_data[18] is not None else '',
            'Zona': siniestro_data[19] if siniestro_data[19] is not None else ''
        }

    id_via = siniestro_data[9]
    print('Id de la via seleccionada:',id_via)
    via_data = via.get_via_by_id(id_via)
    via_data = via_data[0]

    if via_data:
        post_data['Via'] = {
            'Id': via_data[0] if via_data[0] is not None else '',
            'Nombre': via_data[1] if via_data[1] is not None else '',
            'Altura': via_data[2] if via_data[2] is not None else '',
            'Entre_calle1': via_data[3] if via_data[3] is not None else '-',
            'Entre_calle2': via_data[4] if via_data[4] is not None else '-',
            'Tipo': via_data[5] if via_data[5] is not None else '',
            'Material': via_data[6] if via_data[6] is not None else '',
            'Estado': via_data[7] if via_data[7] is not None else '',
            'Localidad_id': via_data[8] if via_data[8] is not None else '',
            'Ciclovia': via_data[9] if via_data[9] is not None else '0',
            'Semaforo_vehicular': via_data[10] if via_data[10] is not None else '0',
            'Semaforo_peatonal': via_data[11] if via_data[11] is not None else '0',
            'Semaforo_ciclistas': via_data[12] if via_data[12] is not None else '0',
            'Chicana': via_data[13] if via_data[13] is not None else '0',
            'Bandas_reductoras': via_data[14] if via_data[14] is not None else '0',
            'Reductor_velocidad': via_data[15] if via_data[15] is not None else '0',
            'Mini_rotonda': via_data[16] if via_data[16] is not None else '0',
            'Meseta_elevada': via_data[17] if via_data[17] is not None else '0',
            'Isleta_giro': via_data[18] if via_data[18] is not None else '0',
            'Iuminaria': via_data[19] if via_data[19] is not None else '0',
            'Limpieza': via_data[20] if via_data[20] is not None else '1',
            'Iluminacion_uniforme': via_data[21] if via_data[21] is not None else '0',
            'Veredas_optimas': via_data[22] if via_data[22] is not None else '0',
            'Carril_omnibus': via_data[23] if via_data[23] is not None else '0',
            'Senalizacion_paradas': via_data[24] if via_data[24] is not None else '0',
            'Demarcacion_separacion_carriles': via_data[25] if via_data[25] is not None else '0',
            'Demarcacion_doble_sentido': via_data[26] if via_data[26] is not None else '0',
            'Demarcacion_visible': via_data[27] if via_data[27] is not None else '0',
            'Senial_advertencia': via_data[28] if via_data[28] is not None else '0',
            'Senial_reglamentaria': via_data[29] if via_data[29] is not None else '0',
            'Senial_maximo': via_data[30] if via_data[30] is not None else '0',
            'Senial_informativa': via_data[31] if via_data[31] is not None else '0',
            'Senial_calle_nomenclada': via_data[32] if via_data[32] is not None else '0',
            'Senial_obstaculiza': via_data[33] if via_data[33] is not None else '0',
            'Senial_redundante': via_data[34] if via_data[34] is not None else '0',
            'Vias_distinta_superficie': via_data[35] if via_data[35] is not None else '0',
            'Interseccion_multiple': via_data[36] if via_data[36] is not None else '0',
            'Visualizacion_cruce': via_data[37] if via_data[37] is not None else '0',
            'Obstruccion_visual': via_data[38] if via_data[38] is not None else '0',
            'Peatones_visibles': via_data[39] if via_data[39] is not None else '0',
            'Iluminacion_obstaculizada': via_data[40] if via_data[40] is not None else '0',
            'Reductores_velocidad_cruce': via_data[41] if via_data[41] is not None else '0',
            'Badenes_canaletas': via_data[42] if via_data[42] is not None else '0',
            'Objetos_rigidos': via_data[43] if via_data[43] is not None else '0',
            'Sendas_peatonales': via_data[44] if via_data[44] is not None else '0',
            'Lineas_pare': via_data[45] if via_data[45] is not None else '0',
            'Cordones_pintados': via_data[46] if via_data[46] is not None else '0',
            'Senial_cruce_peatones': via_data[47] if via_data[47] is not None else '0',
            'Limitacion_velocidad': via_data[48] if via_data[48] is not None else '0',
            'Senial_pare': via_data[49] if via_data[49] is not None else '0',
            'Senial_cruce': via_data[50] if via_data[50] is not None else '0',
            'Senial_ciclovia': via_data[51] if via_data[51] is not None else '0',
            'Senial_reductores': via_data[52] if via_data[52] is not None else '0',
            'Paradas_seguras': via_data[53] if via_data[53] is not None else '0',
            'Obstruccion_carteleria': via_data[54] if via_data[54] is not None else '0',
            'Estado_carteleria': via_data[55] if via_data[55] is not None else '0',
            'Senial_transitoria': via_data[56] if via_data[56] is not None else '0',
            'Ceda_el_paso': via_data[57] if via_data[57] is not None else '0',
            'Cruces_peatonales_rot': via_data[58] if via_data[58] is not None else '0',
            'Senalizacion_rotonda': via_data[59] if via_data[59] is not None else '0',
            'Polvo': via_data[60] if via_data[60] is not None else '0',
            'Zanjas': via_data[61] if via_data[61] is not None else '0',
            'Zanjas_contencion': via_data[62] if via_data[62] is not None else '0',
            'Cruce_peatonal': via_data[63] if via_data[63] is not None else '0', # agregar al form
            'Esquina_cordon_amarillo': via_data[64] if via_data[64] is not None else '0', #agregar al form
            'Senalizacion_e_s_vehiculos': via_data[65] if via_data[65] is not None else '0', #agregar al form
            'SV_ferroviario': via_data[66] if via_data[66] is not None else '0' #agregar al form

        }

    #Guardo los datos de fecha y hora para buscar los datos del clima
    fecha=siniestro_data[1]
    hora=siniestro_data[2]

    clima_data = clima.get_clima(fecha,hora)
    clima_data = clima_data[0]

    if clima_data:
        post_data['Clima'] = {
            'Fecha': str(clima_data[0]) if clima_data[0] is not None else '',
            'Hora': str(clima_data[1]) if clima_data[1] is not None else '',
            'Temp': clima_data[2] if clima_data[2] is not None else '',
            'Nubosidad_porc': clima_data[3] if clima_data[3] is not None else '',
            'Precip_mm': clima_data[4] if clima_data[4] is not None else '',
            'Viento_velocidad': clima_data[5] if clima_data[5] is not None else '',
            'Viento_rafaga': clima_data[6] if clima_data[6] is not None else '',
            'Visibilidad': clima_data[7] if clima_data[7] is not None else ''
        }

    recomendaciones = []

    # Enviar los datos al motor de reglas
    try:
        print("Datos para el motor de reglas:", post_data)
        run_assert_facts(post_data)
        return jsonify({'recomendaciones': recomendaciones})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#######################################################################################
#                              Endpoint get_recomendacion
#######################################################################################

@app.route('/get_recomendacion', methods=['GET'])
def get_recomendacion():
    siniestro_id = request.args.get('siniestro_id', type=int)
    
    recomendacion_tupla = recomendacion.get_recomendacion(siniestro_id)

    print(recomendacion_tupla)

    if not siniestro_id :
        return jsonify({"error": "Faltan parámetros: siniestro_id"}), 400

    try:
        recomendacion_tupla = recomendacion.get_recomendacion(siniestro_id)
        print(recomendacion_tupla)
        recomendacion_data = [
                {
                    "Id": recomendacion[0],
                    "Fecha": str(recomendacion[1]),
                    "Siniestro_id": recomendacion[2],
                    "Accion": recomendacion[3],
                    "Via Id": recomendacion[4],
                    "Estado": recomendacion[5]
                } 
                for recomendacion in recomendacion_tupla
            ]
        print(recomendacion_data)
        return jsonify({"recomendaciones": recomendacion_data}),200
    
    except Exception as e:
        return jsonify({"error": f"Error al obtener recomendaciones: {str(e)}"}), 500

#######################################################################################
#                              Endpoint actualizar_recomendacion_estado
#######################################################################################

@app.route('/actualizar_recomendacion_estado', methods=['POST'])
def actualizar_recomendacion_estado():
    data = request.get_json()
    recomendacion_id = data.get('id')
    nuevo_estado = data.get('estado')
    print(recomendacion_id)
    print(nuevo_estado)
    
    if not recomendacion_id or not nuevo_estado:
        return jsonify({"error": "ID o estado faltante"}), 400

    try:
        # Actualiza el estado en la base de datos
        recomendacion.set_recomendacion_estado(recomendacion_id, nuevo_estado)
        return jsonify({"message": "Estado actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el estado: {str(e)}"}), 500

#######################################################################################
#                              Run Flask
#######################################################################################

if __name__ == "__main__":
    app.run(debug=True)
