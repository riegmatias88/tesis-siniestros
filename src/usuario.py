from database import Database

class Usuario:
    def __init__(self, db, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    db = Database()

    #Métodos Usuario

    def has_username(self, username):
        query = """
            SELECT 1 \
            FROM usuario \
            WHERE username = %s \
        """
        params = (username,)
        try:
            resultados = self.db.execute_select_queries(query, params)
            return bool(resultados)  # Devuelve True si hay resultados, False si está vacío
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")

    def validate_password(self, username, password):
        query = """
            SELECT 1 \
            FROM usuario \
            WHERE username = %s \
            AND password = %s \
        """
        params = (username,)
        try:
            resultados = self.db.execute_select_queries(query, params)
            return bool(resultados) # Devuelve True si la password es correcta resultados, False si está vacío
        except Exception as e:
            print(f"Error al consultar la tabla: {e}")