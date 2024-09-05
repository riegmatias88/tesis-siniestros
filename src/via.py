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
    
