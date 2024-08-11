class Recomendacion:
    def __init__(self, fecha, estado):
        self.calle = fecha
        self.ciudad = estado

    def descripcion(self):
        return f"{self.fecha} {self.estado}"