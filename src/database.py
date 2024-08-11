import mysql.connector
from mysql.connector import Error
import pandas as pd  # Asegúrate de que pandas esté importado
from decimal import Decimal  # Asegúrate de que Decimal está importado

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'siniestros'
        self.user = 'siniestros_USER'
        self.password = 'user123'
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conexión exitosa a la base de datos")
        except Error as e:
            print("Error al conectar a MySQL", e)

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Conexión cerrada")

    def execute_query(self, query):
        try:
            self.connect()
            self.cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                # Convertir Decimal a float con más mensajes de depuración
                #print("Resultados obtenidos de la consulta:", result)
                data = []
                for row in result:
                    row_data = []
                    for value in row:
                        if isinstance(value, Decimal):
                            row_data.append(float(value))
                        else:
                            row_data.append(value)
                    data.append(row_data)
                df = pd.DataFrame(data, columns=columns)
                print(f"Consulta ejecutada, número de filas obtenidas: {len(df)}")
                return df
            else:
                self.connection.commit()
                print("Consulta ejecutada exitosamente")
        except Error as e:
            print("Error al ejecutar la consulta", e)
            return None
        finally:
            self.disconnect()

    def execute_many_queries(self, queries):
        try:
            self.connect()
            for query in queries:
                self.cursor.execute(query)
            self.connection.commit()
            print("Todas las consultas se ejecutaron exitosamente")
        except Error as e:
            print("Error al ejecutar las consultas", e)
        finally:
            self.disconnect()

    def execute_select_queries(self, query, params=None):
        #result = []
        try:
            self.connect()
            self.cursor.execute(query, params if params is not None else ())
            result = self.cursor.fetchall()
            if result:
                print(f"Consulta ejecutada, número de resultados obtenidos: {len(result)}")
            else:
                print("Consulta ejecutada, no se obtuvieron resultados.")
            return result  # Devuelve directamente la lista de tuplas
        except Error as e:
            print("Error al ejecutar la consulta", e)
            return []  # Devuelve una lista vacía en caso de error
        finally:
            self.disconnect()
