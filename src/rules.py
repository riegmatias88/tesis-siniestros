from database import Database
from recomendacion import Recomendacion
from siniestro import Siniestro
from via import Via
from clima import Clima
from durable.lang import *
from datetime import datetime

db = Database()
recomendacion = Recomendacion(db)

def run_assert_facts(post_data):
    assert_fact('recomendacion', post_data)

def load_rules():

    recomendaciones = []

    now = datetime.now().strftime("%Y-%m-%d")
    print (now)
    estado = 'pendiente'

    with ruleset('recomendacion'):

        #Regla 0bis
        #@when_all(
        #    (m.Via.Estado == 'bueno')
        #)
        #def ejecutar_regla0bis(c):
        #    print("Regla 0bis activada: Estado de la vía es 'bueno'")
        #    accion = 'REGLA 0 Bis - Recomendación: Test'
        #    accion_id = 100
        #    recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
        #    #recomendaciones.append(accion)
        #    #print(recomendaciones)
        #    recomendaciones.append({
        #        "Id": accion_id,
        #        "Fecha": now,
        #        "Accion": accion,
        #        "Via_Id": c.m.Via.Id,
        #        "Estado": "pendiente"
        #    })
        #    c.assert_fact({
        #        'Recomendacion': {
        #            'Accion_Recomendada': accion
        #        }
        #    })
        #    c.assert_fact({
        #        'Recomendacion': {
        #            'Accion_Recomendada': 'SH_Precaucion'
        #        }
        #    })

        #Regla 1
        @when_all(
            ((m.Siniestro.Participante1 == 'bicicleta') | 
            (m.Siniestro.Participante2 == 'bicicleta') | 
            (m.Siniestro.Participante3 == 'bicicleta')) & 
            (m.Via.Ciclovia == 0)
        )
        def ejecutar_regla1(c):
            accion_id = 8
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Ubicación_siniestro_via == 'interseccion') &
            (m.Via.Semaforo_vehicular == 1) &
            (m.Via.Semaforo_ciclista == 0)
        )
        def ejecutar_regla2(c):
            accion_id = 16
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            mensaje = 'REGLA 2 - Recomendación: Semaforo_ciclista'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_ciclista'
                }
            })

        #Regla 3
        @when_all(
            (m.Siniestro.Flujo_transito == 'alto') &
            ((m.Siniestro.Zona == 'comercial') |
            (m.Siniestro.Zona == 'residencial')) &
            (m.Via.Cruce_peatonal == 0) & 
            (m.Via.Semaforo_peatonal == 0)
        )
        def ejecutar_regla3(c):
            accion_id = 1
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            mensaje = 'REGLA 3 - Recomendación: Cruce_peatonal'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Cruce_peatonal'
                }
            })

        #Regla 4
        @when_all(
            (m.Siniestro.Tipo == 1) &
            (m.Siniestro.Ubicacion_siniestro_via == 'cruce_peatonal') &
            (m.Via.Cruce_peatonal == 1) &
            (m.Via.Semaforo_peatonal == 0)
        )
        def ejecutar_regla4(c):
            accion_id = 7
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            mensaje = 'REGLA 4 - Recomendación: Semaforo_peatonal'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_peatonal'
                }
            })

        #Regla 5
        @when_all(
            (m.Siniestro.Tipo == 1) &
            (m.Siniestro.Zona == 'escolar') &
            (m.Via.Senializacion_zona_escolar == 0) &
            (m.Via.Senializacion_velocidad_maxima == 0)
        )
        def ejecutar_regla5(c):
            accion_id = 19
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            accion_id = 20
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            ((m.Siniestro.Zona == 'residencial') |
            (m.Siniestro.Zona == 'comercial'))  &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Via.Reductor_velocidad == 0)
        )
        def ejecutar_regla6(c):
            accion_id = 6
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            accion_id = 2
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Tipo == 15) &
            (m.Siniestro.Zona == 'comercial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            (m.Via.Tipo == 'avenida') &
            (m.Via.Sentido == 'doble') &
            (m.Siniestro.Flujo_de_transito == 'alto') &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Via.Reductor_velocidad == 0)
        )
        def ejecutar_regla7(c):
            accion_id = 18
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            mensaje = 'REGLA 7 - Recomendación: Semaforo_vehicular'
            print(mensaje)
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Semaforo_vehicular'
                }
            })

        #Regla 8
        @when_all(
            ((m.Siniestro.Tipo == 15) | 
            (m.Siniestro.Tipo == 16)) &
            (m.Siniestro.Zona == 'comercial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'rotonda')
        )
        def ejecutar_regla8(c):
            accion_id = 21
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Ubicacion_siniestro_via == 'mitad_via') &
            (m.Via.Estrechamiento_calzada == 0) &
            (m.Via.Ciclovia == 0) &
            (m.Via.Tipo == 4) &
            (m.Siniestro.Flujo_de_transito == 'bajo')
        )
        def ejecutar_regla9(c):
            accion_id = 8
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            accion_id = 22
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Tipo == 13) &
            (m.Siniestro.Detalle_siniestro_via == 'mitad_via') &
            (m.Via.Estrechamiento_calzada == 0) &
            (m.Via.Tipo == 4) &
            (m.Siniestro.Flujo_de_transito == 'bajo')
        )
        def ejecutar_regla10(c):
            accion_id = 22
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 10 - Recomendación: Estrechamiento_calzada')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Estrechamiento_calzada'
                }
            })

        #Regla 11
        @when_all(
            ((m.Via.Tipo == 6) | 
            (m.Via.Tipo == 7) |
            (m.Via.Tipo == 8)) &
            (m.Siniestro.Tipo == 14) &
            (m.Via.Senializacion_horizontal == 0) &
            (m.Siniestro.Ubicacion_siniestro_via == 'curva')
        )
        def ejecutar_regla11(c):
            accion_id = 23
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 11 - Recomendación: SH_doble_linea_amarilla')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SH_doble_linea_amarilla'
                }
            })

        #Regla 12
        @when_all(
            ((m.Via.Material == 4) |
            (m.Via.Material == 5)) &
            (m.Via.Tipo != 5)
        )
        def ejecutar_regla12(c):
            accion_id = 13
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 12 - Recomendación: Pavimentar_via')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Pavimentar_via'
                }
            })

        #Regla 13
        @when_all(
            (m.Siniestro.Tipo == 13) &
            ((m.Via.Tipo == 4) | (m.Via.Tipo == 6) | (m.Via.Tipo == 7) | (m.Via.Tipo == 8)) &
            (m.Via.Bandas_reductoras == 0) &
            (m.Via.Senializacion_velocidad_maxima == 0)
        )
        def ejecutar_regla13(c):
            accion_id = 19
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            accion_id = 24
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Tipo == 15) &
            (m.Siniestro.Detalle_siniestro_via == 'interseccion') &
            (m.Via.Mini_rotonda == 0)
        )
        def ejecutar_regla14(c):
            accion_id = 25
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 14 - Recomendación: Mini_rotonda')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'Mini_rotonda'
                }
            })

        #Regla 15
        @when_all(
            (m.Via.Luminaria == 'halogena') &
            (m.Siniestro.Franja_horaria == 'Noche') &
            (m.Clima.Visibilidad == 'mala')
        )
        def ejecutar_regla15(c):
            accion_id = 26
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 15 - Recomendación: luminaria_led')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'luminaria_led'
                }
            })

        #Regla 16
        @when_all(
            (m.Via.Reductor_velocidad == 1) & 
            (m.Via.Senial_reductores == 0)
        )
        def ejecutar_regla16(c):
            accion_id = 2
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            accion_id = 3
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') & 
            (m.Via.Esquina_cordon_amarillo == 0)
        )
        def ejecutar_regla18(c):
            accion_id = 4
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            accion_id = 9
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            accion_id = 27
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 20 - Recomendación: SV_Cruce_peatonal')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_Cruce_peatonal'
                }
            })  

        #Regla 21
        @when_all(
            ((m.Siniestro.Tipo == 1) |
            (m.Siniestro.Tipo == 13) |
            (m.Siniestro.Tipo == 14)) &
            (m.Siniestro.Zona == 'residencial') &
            (m.Siniestro.Ubicacion_siniestro_via == 'recta') &
            (m.Via.Senializacion_vertical == 0) &
            (m.Siniestro.Flujo_de_transito == 'alto')
        )
        def ejecutar_regla21(c):
            accion_id = 19
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 21 - Recomendación: SV_Limite_velocidad_maxima')
            c.assert_fact({
                'recomendacion': {
                    'Accion_Recomendada': 'SV_Limite_velocidad_maxima'
                }
            })  

        #Regla 22
        @when_all(
            (m.Siniestro.Tipo == 15) &
            (m.Siniestro.Ubicacion_siniestro_via == 'interseccion') &
            ((m.Via.Estado == 'grieta') | (m.Via.Estado == 'bache')) &
            (m.Via.Semaforo_vehicular == 0) &
            (m.Clima.Visibilidad == 'mala')
        )
        def ejecutar_regla22(c):
            accion_id = 28
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 22 - Recomendación: SV_Cruce_peligroso')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'SV_Cruce_peligroso'
                }
            })

        #Regla 24
        @when_all(
            (m.Via.Limpieza == 0)
        )
        def ejecutar_regla24(c):
            accion_id = 7
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            print('REGLA 24 - Recomendación: Limpiar_via')
            c.assert_fact({
                'Recomendacion': {
                    'Accion_Recomendada': 'Limpiar_via'
                }
            })

        #Regla 25
        @when_all(
            (m.Siniestro.Ubicacion_siniestro_via == 'e_s_vehiculos') &
            (m.Via.Senalizacion_e_s_vehiculos == 0)
        )
        def ejecutar_regla25(c):
            accion_id = 10
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
            accion_id = 11
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            (m.Via.Ferrovia == 1) &
            (m.Via.SV_ferroviario == 0)
        )
        def ejecutar_regla26(c):
            accion_id = 12
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            accion_id = 14
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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
            accion_id = 15
            recomendacion.set_recomendacion(now, c.m.Siniestro.Id, accion_id, c.m.Via.Id, estado)
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


