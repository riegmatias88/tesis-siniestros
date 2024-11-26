from database import Database

class Siniestro:
    def __init__(self, db, id=None, fecha=None, hora=None, franja_horaria=None, latitud=None, longitud=None, categoria=None, tipo=None, localidad_id=None, via_id=1, participante1=None, participante2=None, participante3=None, obstaculizacion1=None, obstaculizacion2=None, obstaculizacion3=None, flujo_transito=None,  detalle_siniestro_via=None, ubicacion_siniestro_via=None, zona=None):
        self.db = db
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.franja_horaria = franja_horaria
        self.latitud = latitud
        self.longitud = longitud
        self.categoria = categoria
        self.tipo = tipo
        self.localidad_id = localidad_id
        self.via_id = via_id
        self.participante1 = participante1
        self.participante2 = participante2
        self.participante3 = participante3
        self.obstaculizacion1 = obstaculizacion1
        self.obstaculizacion2 = obstaculizacion2
        self.obstaculizacion3 = obstaculizacion3
        self.flujo_transito = flujo_transito
        self.detalle_siniestro_via = detalle_siniestro_via
        self.ubicacion_siniestro_via = ubicacion_siniestro_via
        self.zona = zona

    #Metodos Siniestro

    def get_siniestros(self):
        query = """
            SELECT * FROM siniestro_v3
        """
        params = ()
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def get_siniestro_by_id(self, id_siniestro):
        query = """
            SELECT * \
            FROM siniestro_v3 where id = %s
        """
        params = (id_siniestro,)
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def get_geo_siniestro_by_id(self, id_siniestro):
        query = """
            SELECT latitud , longitud \
            FROM siniestro_v3 \
            WHERE id = %s \
        """
        params = (id_siniestro,)
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")
    

    def get_siniestro_by_ubicacion(self, provincia, departamento, localidad):
        #query = "SELECT id , tipo_siniestro FROM siniestro_v3 where localidad_id IN (select localidad_id FROM localidad WHERE provincia_desc = %s AND departamento_desc = %s AND localidad_desc = %s)"
        query = """
            SELECT s.id, s.fecha, s.hora, st.descripcion, sc.descripcion, v.nombre, v.altura, v.entre_calle1, v.entre_calle2 \
            FROM siniestro_v3 s \
            INNER JOIN siniestro_tipo st ON (s.tipo=st.id) \
            INNER JOIN siniestro_categoria sc ON (s.categoria=sc.id) \
            INNER JOIN via v ON (s.via_id=v.id) \
            WHERE s.localidad_id IN (select id FROM localidad WHERE provincia_desc = %s AND departamento_desc = %s AND localidad_desc = %s) \
        """
        params = (provincia,departamento,localidad)
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def get_siniestro_geo(self, provincia, departamento, localidad):
        query = """
            SELECT s.latitud, s.longitud \
            FROM siniestro_v3 s \
            INNER JOIN siniestro_tipo st ON (s.tipo=st.id) \
            INNER JOIN siniestro_categoria sc ON (s.categoria=sc.id) \
            WHERE s.localidad_id IN (select id FROM localidad WHERE provincia_desc = %s AND departamento_desc = %s AND localidad_desc = %s) \
        """
        params = (provincia,departamento,localidad)
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def get_siniestro_zona(self, provincia, departamento, localidad):
        query = """
            SELECT DISTINCT s.zona \
            FROM siniestro_v3 s \
            INNER JOIN siniestro_tipo st ON (s.tipo=st.id) \
            INNER JOIN siniestro_categoria sc ON (s.categoria=sc.id) \
            INNER JOIN via v ON (s.via_id=v.id) \
            WHERE s.localidad_id IN (select id FROM localidad WHERE provincia_desc = %s AND departamento_desc = %s AND localidad_desc = %s) \
        """
        params = (provincia,departamento,localidad)
        try:
            return self.db.execute_select_queries(query,params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def get_siniestro_detalle(self, provincia_desc, departamento_desc, localidad_desc, siniestro_id):
        query = """
            SELECT 
                s.id, s.fecha, s.hora, s.franja_horaria, s.latitud, s.longitud, 
                st.descripcion AS tipo, sc.descripcion AS categoria, 
                s.participante1, s.participante2, s.flujo_transito, 
                s.ubicacion_siniestro_via, v.nombre AS via_nombre, v.altura AS via_altura, 
                v.entre_calle1, v.entre_calle2
            FROM siniestro_v3 s
            INNER JOIN siniestro_tipo st ON s.tipo = st.id
            INNER JOIN siniestro_categoria sc ON s.categoria = sc.id
            INNER JOIN via v ON s.via_id = v.id
            WHERE s.id = %s 
            AND s.localidad_id IN (
                SELECT id FROM localidad 
                WHERE provincia_desc = %s AND departamento_desc = %s AND localidad_desc = %s
            )
        """
        params = (siniestro_id, provincia_desc, departamento_desc, localidad_desc)
        return self.db.execute_select_queries(query, params)
