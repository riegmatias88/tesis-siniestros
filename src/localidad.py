from database import Database

class Localidad:
    def __init__(self, db, provincia_desc=None, departamento_desc=None, localidad_desc=None):
        self.provincia_desc = provincia_desc
        self.departamento_desc = departamento_desc
        self.localidad_desc = localidad_desc
    
    db = Database()

    def get_departamentos(self, provincia):
        query = "SELECT DISTINCT departamento_desc FROM localidad WHERE provincia_desc = %s"
        result = self.db.execute_select_queries(query, (provincia,))
        if result:
            return [row[0] for row in result]
        else:
            return []
        
    def get_localidades(self, provincia, departamento):
        query = "SELECT DISTINCT localidad_desc FROM localidad WHERE provincia_desc = %s AND departamento_desc = %s"
        result = self.db.execute_select_queries(query, (provincia, departamento))
        if result:
            return [row[0] for row in result]
        else:
            return []