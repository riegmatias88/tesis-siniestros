from database import Database

class Clima:
    def __init__(self, db, fecha=None, hora=None, temp=None, viento_rafaga=None, viento_velocidad=None, nubosidad_porc=None, precip_mm=None):
        self.fecha = fecha
        self.hora = hora
        self.temp = temp
        self.viento_rafaga = viento_rafaga
        self.viento_velocidad = viento_velocidad
        self.nubosidad_porc = nubosidad_porc
        self.precip_mm = precip_mm

    db = Database()

#Métodos Clima

    def get_temp(self, fecha, hora):
        query = "SELECT temp FROM clima WHERE fecha = %s AND hora = %s"
        result = self.db.execute_select_queries(query, (fecha, hora))
        if result:
            return result[0][0]
        else:
            return None
        
    def get_viento_rafaga(self, fecha, hora):
        query = "SELECT viento_rafaga FROM clima WHERE fecha = %s AND hora = %s"
        result = self.db.execute_select_queries(query, (fecha, hora))
        if result:
            return result[0][0]
        else:
            return None
        
    def get_viento_velocidad(self, fecha, hora):
        query = "SELECT viento_velocidad FROM clima WHERE fecha = %s AND hora = %s"
        result = self.db.execute_select_queries(query, (fecha, hora))
        if result:
            return result[0][0]
        else:
            return None
        
    def get_nubosidad_porc(self, fecha, hora):
        query = "SELECT nubosidad_porc FROM clima WHERE fecha = %s AND hora = %s"
        result = self.db.execute_select_queries(query, (fecha, hora))
        if result:
            return result[0][0]
        else:
            return None
        
    def get_precip_mm(self, fecha, hora):
        query = "SELECT precip_mm FROM clima WHERE fecha = %s AND hora = %s"
        result = self.db.execute_select_queries(query, (fecha, hora))
        if result:
            return result[0][0]
        else:
            return None