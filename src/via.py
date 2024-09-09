from database import Database

class Via:
    def __init__(self, db, nombre=None, altura=None, tipo=None, material=None, estado=None, localidad=None, departamento=None, ciudad=None, provincia=None, ciclovia=None, semaforo_vehicular=None, semaforo_peatonal=None, semaforo_ciclista=None, senializacion_horizontal=None, senializacion_vertical=None, senializacion_temporal=None, chicana=None, bandas_reductoras=None, lomo_de_burro=None, mini_rotonda=None, meseta_elevada=None, isleta_giro=None, luminaria=None):        
        self.db = db
        self.nombre = nombre
        self.altura = altura
        self.tipo = tipo
        self.material = material
        self.estado = estado
        self.localidad = localidad
        self.departamento = departamento
        self.ciudad = ciudad
        self.provincia = provincia
        self.ciclovia = ciclovia
        self.semaforo_vehicular = semaforo_vehicular
        self.semaforo_peatonal = semaforo_peatonal
        self.semaforo_ciclista = semaforo_ciclista
        self.senializacion_horizontal = senializacion_horizontal
        self.senializacion_vertical = senializacion_vertical
        self.senializacion_temporal = senializacion_temporal
        self.chicana = chicana
        self.bandas_reductoras = bandas_reductoras
        self.lomo_de_burro = lomo_de_burro
        self.mini_rotonda = mini_rotonda
        self.meseta_elevada = meseta_elevada
        self.isleta_giro = isleta_giro
        self.luminaria = luminaria

#Métodos Via

    def get_material(self, nombre, altura, ciudad):
        query = "SELECT via_material.descripcion FROM via INNER JOIN via_material ON (via.material=via_material.id) WHERE via.nombre = %s AND via.altura = %s AND via.ciudad = %s"
        result = self.db.execute_select_queries(query, (nombre, altura, ciudad))
        if result:
            return result[0][0]
        else:
            return None
    
    def set_via(self, nombre, altura, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, carril_omnibus, senalizacion_paradas, ciclovia, chicana, bandas_reductoras, reductor_velocidad, mini_rotonda, meseta_elevada, isleta_giro, demarcacion_separacion_carriles, demarcacion_doble_sentido, demarcacion_visible, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_calle_nomenclada, senial_obstaculiza, senial_redundante, vias_distinta_superficie, interseccion_multiple, visualizacion_cruce, obstruccion_visual, peatones_visibles, iluminacion_obstaculizada, reductores_velocidad_cruce, badenes_canaletas, objetos_rigidos, sendas_peatonales, lineas_pare, cordones_pintados, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, paradas_seguras, obstruccion_carteleria, estado_carteleria, senial_transitoria, ceda_el_paso, cruces_peatonales_rot, senalizacion_rotonda, semaforo_vehicular, semaforo_peatonal, semaforo_ciclistas, localidad_id):
        if nombre: self.nombre = nombre
        if altura: self.altura = altura
        if tipo: self.tipo = tipo
        if material: self.material = material
        if estado: self.estado = estado
        if limpieza: self.limpieza = limpieza
        if luminaria: self.iluminacion = luminaria
        if iluminacion_uniforme: self.iluminacion_uniforme = iluminacion_uniforme
        if veredas_optimas: self.veredas_optimas = veredas_optimas
        if carril_omnibus: self.carril_omnibus = carril_omnibus
        if senalizacion_paradas: self.senalizacion_paradas = senalizacion_paradas
        if ciclovia: self.ciclovia = ciclovia
        if chicana: self.chicana = chicana
        if bandas_reductoras: self.bandas_reductoras = bandas_reductoras
        if reductor_velocidad: self.reductor_velocidad = reductor_velocidad
        if mini_rotonda: self.mini_rotonda = mini_rotonda
        if meseta_elevada: self.meseta_elevada = meseta_elevada
        if isleta_giro: self.isleta_giro = isleta_giro
        if demarcacion_separacion_carriles: self.demarcacion_separacion_carriles= demarcacion_separacion_carriles
        if demarcacion_doble_sentido: self.demarcacion_doble_sentido= demarcacion_doble_sentido
        if demarcacion_visible: self.demarcacion_visible= demarcacion_visible
        if senial_advertencia: self.senial_advertencia= senial_advertencia
        if senial_reglamentaria: self.senial_reglamentaria= senial_reglamentaria
        if senial_maximo: self.senial_maximo= senial_maximo
        if senial_informativa : self.senial_informativa = senial_informativa 
        if senial_calle_nomenclada : self.senial_calle_nomenclada = senial_calle_nomenclada 
        if senial_obstaculiza: self.senial_obstaculiza= senial_obstaculiza
        if senial_redundante: self.senial_redundante= senial_redundante
        if vias_distinta_superficie: self.vias_distinta_superficie = vias_distinta_superficie
        if interseccion_multiple: self.interseccion_multiple = interseccion_multiple
        if visualizacion_cruce: self.visualizacion_cruce = visualizacion_cruce
        if obstruccion_visual: self.obstruccion_visual = obstruccion_visual
        if peatones_visibles: self.peatones_visibles = peatones_visibles
        if iluminacion_obstaculizada: self.iluminacion_obstaculizada = iluminacion_obstaculizada
        if reductores_velocidad_cruce: self.reductores_velocidad_cruce = reductores_velocidad_cruce
        if badenes_canaletas: self.badenes_canaletas = badenes_canaletas
        if objetos_rigidos: self.objetos_rigidos = objetos_rigidos
        if sendas_peatonales: self.sendas_peatonales = sendas_peatonales
        if lineas_pare: self.lineas_pare = lineas_pare
        if cordones_pintados: self.cordones_pintados = cordones_pintados
        if senial_cruce_peatones: self.senial_cruce_peatones = senial_cruce_peatones
        if limitacion_velocidad: self.limitacion_velocidad = limitacion_velocidad
        if senial_pare: self.senial_pare = senial_pare
        if senial_cruce: self.senial_cruce = senial_cruce
        if senial_ciclovia: self.senial_ciclovia = senial_ciclovia
        if senial_reductores: self.senial_reductores = senial_reductores
        if paradas_seguras: self.paradas_seguras = paradas_seguras
        if obstruccion_carteleria: self.obstruccion_carteleria = obstruccion_carteleria
        if estado_carteleria: self.estado_carteleria = estado_carteleria
        if senial_transitoria: self.senial_transitoria = senial_transitoria
        if ceda_el_paso: self.ceda_el_paso = ceda_el_paso
        if cruces_peatonales_rot: self.cruces_peatonales_rot = cruces_peatonales_rot
        if senalizacion_rotonda: self.senalizacion_rotonda = senalizacion_rotonda
        if semaforo_vehicular: self.semaforo_vehicular = semaforo_vehicular
        if semaforo_peatonal: self.semaforo_peatonal = semaforo_peatonal
        if semaforo_ciclistas: self.semaforo_ciclistas = semaforo_ciclistas
        if localidad_id: self.localidad_id = localidad_id

        query = """
            INSERT INTO via (nombre, altura, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, carril_omnibus, senalizacion_paradas, ciclovia, chicana, bandas_reductoras, reductor_velocidad, mini_rotonda, meseta_elevada, isleta_giro, demarcacion_separacion_carriles, demarcacion_doble_sentido, demarcacion_visible, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_calle_nomenclada, senial_obstaculiza, senial_redundante, vias_distinta_superficie, interseccion_multiple, visualizacion_cruce, obstruccion_visual, peatones_visibles, iluminacion_obstaculizada, reductores_velocidad_cruce, badenes_canaletas, objetos_rigidos, sendas_peatonales, lineas_pare, cordones_pintados, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, paradas_seguras, obstruccion_carteleria, estado_carteleria, senial_transitoria, ceda_el_paso, cruces_peatonales_rot, senalizacion_rotonda, semaforo_vehicular, semaforo_peatonal, semaforo_ciclistas, localidad_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            #self.db.execute_write_query(query, (nombre, altura, tipo, material, estado, localidad_id))
            self.db.execute_write_query(query, (nombre, altura, tipo, material, estado, limpieza, luminaria, iluminacion_uniforme, veredas_optimas, carril_omnibus, senalizacion_paradas, ciclovia, chicana, bandas_reductoras, reductor_velocidad, mini_rotonda, meseta_elevada, isleta_giro, demarcacion_separacion_carriles, demarcacion_doble_sentido, demarcacion_visible, senial_advertencia, senial_reglamentaria, senial_maximo, senial_informativa, senial_calle_nomenclada, senial_obstaculiza, senial_redundante, vias_distinta_superficie, interseccion_multiple, visualizacion_cruce, obstruccion_visual, peatones_visibles, iluminacion_obstaculizada, reductores_velocidad_cruce, badenes_canaletas, objetos_rigidos, sendas_peatonales, lineas_pare, cordones_pintados, senial_cruce_peatones, limitacion_velocidad, senial_pare, senial_cruce, senial_ciclovia, senial_reductores, paradas_seguras, obstruccion_carteleria, estado_carteleria, senial_transitoria, ceda_el_paso, cruces_peatonales_rot, senalizacion_rotonda, semaforo_vehicular, semaforo_peatonal, semaforo_ciclistas, localidad_id))

        except Exception as e:
            print(f"Error al actualizar la tabla: {e}") 
        

