from database import Database

class Siniestro:
    def __init__(self, db, 
                 id=None, fecha=None, hora=None, franja_horaria_desc=None, zona_de_ocurrencia_desc=None, 
                 Siniestro_tipo_via_publica_id=None, Siniestro_via=None, Siniestro_altura=None, 
                 Siniestro_inteseccion=None, latitud=None, longitud=None, categoria_del_Siniestro_id=None, 
                 tipo_Siniestro1_id=None, tipo_Siniestro2_id=None, tipo_Siniestro3_id=None, 
                 Vehiculo=None, Interviniente_Automovil=None, Interviniente_Motovehiculo=None, 
                 Interviniente_Peaton=None, Interviniente_Bicicleta=None, Interviniente_Cuatriciclo=None, 
                 Interviniente_Camioneta_Utilitario=None, Interviniente_Transporte_de_carga=None, 
                 Interviniente_Transporte_de_pasajeros=None, Interviniente_Maquinaria=None, 
                 Interviniente_Traccion_a_sangre=None, Interviniente_veh_mov_personal=None, 
                 Interviniente_tren=None, Interviniente_Vehiculo_oficial=None, 
                 Interviniente_Otro=None, Interviniente_Sin_datos=None, 
                 localidad_id=None, via_id=1):
        self.db = db
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.franja_horaria_desc = franja_horaria_desc
        self.zona_de_ocurrencia_desc = zona_de_ocurrencia_desc
        self.Siniestro_tipo_via_publica_id = Siniestro_tipo_via_publica_id
        self.Siniestro_via = Siniestro_via
        self.Siniestro_altura = Siniestro_altura
        self.Siniestro_inteseccion = Siniestro_inteseccion
        self.latitud = latitud
        self.longitud = longitud
        self.categoria_del_Siniestro_id = categoria_del_Siniestro_id
        self.tipo_Siniestro1_id = tipo_Siniestro1_id
        self.tipo_Siniestro2_id = tipo_Siniestro2_id
        self.tipo_Siniestro3_id = tipo_Siniestro3_id
        self.Vehiculo = Vehiculo
        self.Interviniente_Automovil = Interviniente_Automovil
        self.Interviniente_Motovehiculo = Interviniente_Motovehiculo
        self.Interviniente_Peaton = Interviniente_Peaton
        self.Interviniente_Bicicleta = Interviniente_Bicicleta
        self.Interviniente_Cuatriciclo = Interviniente_Cuatriciclo
        self.Interviniente_Camioneta_Utilitario = Interviniente_Camioneta_Utilitario
        self.Interviniente_Transporte_de_carga = Interviniente_Transporte_de_carga
        self.Interviniente_Transporte_de_pasajeros = Interviniente_Transporte_de_pasajeros
        self.Interviniente_Maquinaria = Interviniente_Maquinaria
        self.Interviniente_Traccion_a_sangre = Interviniente_Traccion_a_sangre
        self.Interviniente_veh_mov_personal = Interviniente_veh_mov_personal
        self.Interviniente_tren = Interviniente_tren
        self.Interviniente_Vehiculo_oficial = Interviniente_Vehiculo_oficial
        self.Interviniente_Otro = Interviniente_Otro
        self.Interviniente_Sin_datos = Interviniente_Sin_datos
        self.localidad_id = localidad_id
        self.via_id = via_id

    
    def get_siniestros(self):
        query = "SELECT * FROM siniestro"
        return self.db.execute_select_queries(query)