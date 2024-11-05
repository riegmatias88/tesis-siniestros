from database import Database
from recomendacion import Recomendacion
from siniestro import Siniestro
from via import Via
from clima import Clima
from durable.lang import *

db = Database()
recomendacion = Recomendacion(db)

def run_assert_facts(post_data):
    assert_fact('recomendacion', post_data)

def load_rules():

    recomendaciones = []

    with ruleset('recomendacion'):

        # Regla 0: Si contiene Accion_Recomendada, imprimirla
        @when_all(m.Accion_Recomendada)
        def ejecutar_regla0(c):
            print('Entrando en la regla de acción recomendada')
            if 'Accion_Recomendada' in c.m:
                print(f'POST REGLAS: Acción Recomendada: {c.m.Accion_Recomendada}')
            else:
                print('POST REGLAS: No se encontró Accion_Recomendada')

        #Regla 0bis
        @when_all(
            (m.Via.Estado == 'bueno')
        )
        def ejecutar_regla0bis(c):
            mensaje = 'REGLA 0 Bis - Recomendación: Test'
            print(mensaje)
            recomendaciones.append(mensaje)
            print(recomendaciones)
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': recomendaciones
                }
            })
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SH_Precaucion'
                }
            })

        #Regla 1
        @when_all(
            ((m.Siniestro.Participante1 == 'bicicleta') | 
            (m.Siniestro.Participante2 == 'bicicleta') | 
            (m.Siniestro.Participante3 == 'bicicleta')) & 
            (m.Via.Ciclovia == 0)
        )
        def ejecutar_regla1(c):
            mensaje = 'REGLA 1 - Recomendación: Ciclovia'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Ciclovia'
                }
            })

        #Regla 2
        @when_all(
            (m.Vehiculo.Tipo == 'bicicleta') &
            (m.Via.Ciclovia == 1) &
            (m.Siniestro.Ubicación_siniestro_via == 'intersecciion') &
            (m.Via.Semaforo_vehicular == 1) &
            (m.Via.Semaforo_ciclista == 0)
        )
        def ejecutar_regla2(c):
            mensaje = 'REGLA 2 - Recomendación: Semaforo_ciclista'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_ciclista'
                }
            })

        #Regla 3
        @when_all(
            (m.Siniestro.Flujo_de_transito == 'alto') &
            ((m.Via.Zona == 'comercial') |
            (m.Via.Zona == 'residencial')) &
            (m.Via.Cruce_peatonal == 0) & 
            (m.Via.Semaforo_peatonal == 0)
        )
        def ejecutar_regla3(c):
            mensaje = 'REGLA 3 - Recomendación: Cruce_peatonal'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Cruce_peatonal'
                }
            })

        #Regla 4
        @when_all(
            (m.Siniestro.Tipo == 'atropello') &
            (m.Siniestro.Ubicacion_siniestro_via == 'cruce_peatonal') &
            (m.Via.Cruce_peatonal == 1) &
            (m.Via.Semaforo_peatonal == 0)
        )
        def ejecutar_regla4(c):
            mensaje = 'REGLA 4 - Recomendación: Semaforo_peatonal'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_peatonal'
                }
            })

        #Regla 5
        @when_all(
            (m.Siniestro.Tipo == 'atropello') &
            (m.Via.Zona == 'escolar') &
            (m.Via.Senializacion_zona_escolar == 0) &
            (m.Via.Senializacion_velocidad_maxima == 0)
        )
        def ejecutar_regla5(c):
            mensaje = 'REGLA 5 - Recomendación: Senialización_velocidad_maxima y Senialización_zona_escolar'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Senialización_zona_escolar'
                }
            })
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Senialización_velocidad_maxima'
                }
            })

        #Regla 6
        @when_all(
            ((m.Via.Zona == 'residencial') |
            (m.Via.Zona == 'comercial'))  &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Via.Reductor_velocidad == 0)
        )
        def ejecutar_regla6(c):
            mensaje = 'REGLA 6 - Recomendación: Reductor_velocidad y SV_reductor_de_velocidad'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Reductor_velocidad'
                }
            })
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_reductor_de_velocidad'
                }
            })
        
        #Regla 7
        @when_all(
            (m.Siniestro.Tipo == 'lateral') &
            (m.Via.Zona == 'comercial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            (m.Via.Tipo == 'avenida') &
            (m.Via.Sentido == 'doble') &
            (m.Siniestro.Flujo_de_transito == 'alto') &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Via.Reductor_velocidad == 0)
        )
        def ejecutar_regla7(c):
            mensaje = 'REGLA 7 - Recomendación: Semaforo_vehicular'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_vehicular'
                }
            })

        #Regla 8
        @when_all(
            (m.Siniestro.Tipo == 'lateral') &
            (m.Via.Zona == 'comercial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'rotonda')
        )
        def ejecutar_regla8(c):
            print('REGLA 8 - Recomendación: SV_ceda_el_paso')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_ceda_el_paso'
                }
            })

        #Regla 9
        @when_all(
            ((m.Siniestro.Participante1 == 'bicicleta') |
            (m.Siniestro.Participante2 == 'bicicleta') |
            (m.Siniestro.Participante3 == 'bicicleta')) &
            (m.Siniestro.Detalle_siniestro_via == 'mitad_de_via') &
            (m.Via.Estrechamiento_calzada == 0) &
            (m.Via.Ciclovia == 0) &
            (m.Via.Tipo == 0) &
            (m.Siniestro.Flujo_de_transito == 0)
        )
        def ejecutar_regla9(c):
            print('REGLA 9 Recomendación: Implementar Estrechamiento de Calzada y Ciclovía.')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Estrechamiento_calzada'
                }
            })
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Ciclovia'
                }
            })

        #Regla 10
        @when_all(
            (m.Siniestro.Tipo == 'alcance') &
            (m.Siniestro.Detalle_siniestro_via == 'mitad_de_via') &
            (m.Via.Estrechamiento_calzada == 0) &
            (m.Via.Tipo == 'calle') &
            (m.Siniestro.Flujo_de_transito == 'bajo')
        )
        def ejecutar_regla10(c):
            print('REGLA 10 - Recomendación: Estrechamiento_calzada')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Estrechamiento_calzada'
                }
            })

        #Regla 11
        @when_all(
            (m.Via.Tipo == 'ruta') &
            (m.Siniestro.Tipo == 'frontal') &
            (m.Via.Senializacion_horizontal == 0) &
            (m.Siniestro.Ubicacion_siniestro_via == 'curva')
        )
        def ejecutar_regla11(c):
            print('REGLA 11 - Recomendación: SH_doble_linea_amarilla')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SH_doble_linea_amarilla'
                }
            })

        #Regla 12
        @when_all(
            ((m.Via.Material == 'tierra') |
            (m.Via.Material == 'ripio')) &
            (m.Via.Tipo != 'camino_rural')
        )
        def ejecutar_regla12(c):
            print('REGLA 12 - Recomendación: Pavimentar_via')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Pavimentar_via'
                }
            })

        #Regla 13
        @when_all(
            (m.Siniestro.Tipo == 'alcance') &
            ((m.Via.Tipo == 'calle') | (m.Via.Tipo == 'ruta')) &
            (m.Via.Bandas_reductoras == 'no') &
            (m.Via.Senializacion_velocidad_maxima == 0)
        )
        def ejecutar_regla13(c):
            print('REGLA 13 - Recomendación: Bandas_reductoras_optico_sonoras y SV_velocidad_maxima')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Bandas_reductoras_optico_sonoras'
                }
            })
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_velocidad_maxima'
                }
            })

        #Regla 14
        @when_all(
            (m.Siniestro.Tipo == 'lateral') &
            (m.Siniestro.Detalle_siniestro_via == 'interseccion') &
            (m.Via.Mini_rotonda == 0)
        )
        def ejecutar_regla14(c):
            print('REGLA 14 - Recomendación: Mini_rotonda')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Mini_rotonda'
                }
            })

        #Regla 15
        @when_all(
            (m.Via.Luminaria == 'halogena') &
            (m.Siniestro.Franja_horaria == 'nocturno') &
            (m.Clima.Visibilidad == 'mala')
        )
        def ejecutar_regla15(c):
            print('REGLA 15 - Recomendación: luminaria_led')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'luminaria_led'
                }
            })

        #Regla 16
        @when_all(
            (m.Via.Reductor_velocidad == 1) & 
            (m.Via.Senializacion_vertical == 0)
        )
        def ejecutar_regla16(c):
            print('REGLA 16 - Recomendación: SV_Reductor_velocidad')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_Reductor_velocidad'
                }
            })

        #Regla 17
        @when_all(
            (m.Siniestro.Obstaculizacion1 == 'arbol') |
            (m.Siniestro.Obstaculizacion2 == 'arbol') |
            (m.Siniestro.Obstaculizacion3 == 'arbol')
        )
        def ejecutar_regla17(c):
            print('REGLA 17 - Recomendación: Podar_arboles')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Podar_arboles'
                }
            }) 

        #Regla 18
        @when_all(
            ((m.Siniestro.Obstaculizacion1 == 'vehiculo') |
            (m.Siniestro.Obstaculizacion2 == 'vehiculo') |
            (m.Siniestro.Obstaculizacion3 == 'vehiculo')) & 
            (m.Siniestro.Detalle_siniestro_via == 'interseccion') & 
            (m.Via.Esquina_cordon_amarillo == 0)
        )
        def ejecutar_regla18(c):
            print('REGLA 18 - Recomendación: Pintar_esquina_cordon_amarillo')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Pintar_esquina_cordon_amarillo'
                }
            })

        #Regla 19
        @when_all(
            (m.Via.Estado == 'hundimiento') |
            (m.Via.Estado == 'grieta') | 
            (m.Via.Estado == 'bache')
        )
        def ejecutar_regla19(c):
            print('REGLA 19 - Recomendación: Reparar_via')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Reparar_via'
                }
            })

        #Regla 20
        @when_all(
            (m.Via.Cruce_peatonal == 1) & 
            (m.Via.Senializacion_vertical == 0)
        )
        def ejecutar_regla20(c):
            print('REGLA 20 - Recomendación: SV_Cruce_peatonal')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_Cruce_peatonal'
                }
            })  

        #Regla 21
        @when_all(
            ((m.Siniestro.Tipo == 'frontal') |
            (m.Siniestro.Tipo == 'alcance') |
            (m.Siniestro.Tipo == 'atropello')) &
            (m.Via.Zona == 'residencial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'recta') &
            (m.Via.Senializacion_vertical == 0) &
            (m.Siniestro.Flujo_de_transito == 'alto')
        )
        def ejecutar_regla21(c):
            print('REGLA 21 - Recomendación: SV_Limite_velocidad_maxima')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_Limite_velocidad_maxima'
                }
            })  

        #Regla 22
        @when_all(
            (m.Siniestro.Tipo == 'lateral') &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            ((m.Via.Estado == 'grieta') | (m.Via.Estado == 'bache')) &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Clima.Visibilidad == 'mala')
        )
        def ejecutar_regla22(c):
            print('REGLA 22 - Recomendación: SV_Cruce_peligroso')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SV_Cruce_peligroso'
                }
            })

        #Regla 24
        @when_all(
            (m.Via.Limpieza == 'sucia')
        )
        def ejecutar_regla24(c):
            print('REGLA 24 - Recomendación: Limpiar_via')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'Limpiar_via'
                }
            })

        #Regla 25
        @when_all(
            (m.Via.Tipo == 'e_s_vehiculos') &
            (m.Via.Senializacion_vertical == 0) &
            (m.Via.Senializacion_horizontal == 0)
        )
        def ejecutar_regla25(c):
            print('REGLA 25 - Recomendación: SV_e_s_vehiculos y SH_e_s_vehiculos')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SV_e_s_vehiculos'
                }
            })
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SH_e_s_vehiculos'
                }
            })

        #Regla 26
        @when_all(
            (m.Via.Ferrovia == 'si') &
            (m.Via.Senializacion_vertical == 0)
        )
        def ejecutar_regla26(c):
            print('REGLA 26 - Recomendación: SV_Cartel_ferroviario')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SV_Cartel_ferroviario'
                }
            })
        
        #Regla 27
        @when_all(
            ((m.Via.Material == 'ripio') |
            (m.Via.Material =='tierra')) &
            (m.Via.Cuneta == 0)
        )
        def ejecutar_regla27(c):
            print('REGLA 27 - Recomendación: Cuneta')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'Cuneta'
                }
            })

        #Regla 28
        @when_all(
            (m.Via.Estado == 'grieta') &
            (m.Via.Senializacion_temporal == 0) &
            (m.Via.Senializacion_vertical == 0) &
            (m.Via.Senializacion_horizontal == 0)
        )
        def ejecutar_regla28(c):
            print('REGLA 28 - Recomendación: Señalización de Precaución (SV y SH)')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SV_Precaucion'
                }
            })
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SH_Precaucion'
                }
            })


