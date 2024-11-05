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

    def get_clima(self, fecha, hora):
        query = "SELECT * FROM clima WHERE fecha = %s AND TIME_FORMAT(hora,'%H:00:00') = TIME_FORMAT(%s,'%H:00:00')"
        params = (fecha,hora)
        return self.db.execute_select_queries(query, params)