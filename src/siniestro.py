class Siniestro:
    def __init__(self, tipo, categoria, detalle_siniestro_via, ubicacion_siniestro_via, geolocalizacion, fecha, hora, zona, obstaculizacion):
        self.tipo = tipo
        self.categoria = categoria
        self.detalle_siniestro_via = detalle_siniestro_via
        self.ubicacion_siniestro_via = ubicacion_siniestro_via
        self.geolocalizacion = geolocalizacion
        self.fecha = fecha
        self.hora = hora
        self.zona = zona
        self.obstaculizacion = obstaculizacion

    def descripcion(self):
        return f"{self.tipo} {self.categoria} ({self.detalle_siniestro_via})"