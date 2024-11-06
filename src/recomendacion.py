class Recomendacion:
    def __init__(self, db, fecha=None, accion_id=None, via_id=None, estado=None, nombre=None, altura=None, accion_recomendada=None):        
        self.db = db
        self.fecha = fecha
        self.accion_id = accion_id
        self.via_id = via_id
        self.estado = estado

    def get_recomendacion(self,siniestro_id):
        query = """
            SELECT r.id, r.fecha, r.siniestro_id, ra.descripcion, r.via_id, r.estado \
            FROM recomendacion r INNER JOIN recomendacion_accion ra ON (r.accion_id=ra.id) \
            WHERE r.siniestro_id = %s
        """
        params = (siniestro_id,)
        try:
            return self.db.execute_select_queries(query, params)
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")


    def set_recomendacion(self, fecha, siniestro_id, accion_id, via_id, estado):
        query = """
            INSERT INTO recomendacion (fecha, siniestro_id, accion_id, via_id, estado) 
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute_write_query(query, (fecha, siniestro_id , accion_id, via_id, estado))

        except Exception as e:
            print(f"Error al actualizar la tabla: {e}")
