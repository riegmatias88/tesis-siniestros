class Recomendacion:
    def __init__(self, db, fecha=None, accion_id=None, via_id=None, estado=None, nombre=None, altura=None, accion_recomendada=None):        
        self.db = db
        self.fecha = fecha
        self.accion_id = accion_id
        self.via_id = via_id
        self.estado = estado

    def guardar_recomendacion(self, recomendacion_data):
        query = "INSERT INTO recomendacion (fecha, accion_id, via_id, estado) VALUES (%s, %s, %s, %s)"
        self.db.execute_write_query(query, recomendacion_data)
    

    