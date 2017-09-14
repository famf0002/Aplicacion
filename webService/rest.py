# -*- coding: utf-8 -*-
import datetime
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Lectore, Lectura, Usuario, Dependencia, Acceso

"""
ESTADOS DE ERROR:
    ESTADOS = (
        ('1', 'OK.'),
        ('2', 'ERR. LECTOR NO EXISTE'),
        ('3', 'ERR. USUARIO NO EXISTE'),
        ('4', 'ERR. USUARIO NO TIENE PERMISOS'),
        ('5', 'ERR. AFORO LLENO'),
        ('6', 'OK. SALIDA CORRECTA'),
        ('7', 'OK. ENTRADA CORRECTA'),
    )
"""


@api_view(['GET'])
def comprobarAcceso(request, datos):
    try:
        if request.method == 'GET':
            print datos
            recibidos = json.loads(datos)
            print recibidos["id_lector"]
            print recibidos["uid"]
            print recibidos["dni"]
            fechaActual = datetime.datetime.now().replace(microsecond=0)
            print fechaActual


            try:
                """Se compruba que existe el lector"""
                r_lector = Lectore.objects.get(id=recibidos["id_lector"])
                r_dependencia = Dependencia.objects.get(id=r_lector.id_dependencia_id)

                try:
                    """Se comprueba si el usuario exite"""
                    r_usuario = Usuario.objects.get(dni=recibidos["dni"], uid=recibidos["uid"])

                    try:

                        """Se comprueba si el usuario tiene permiso para acceder a la sala"""
                        r_permiso = Usuario.objects.get(permisos__pk=r_lector.id_dependencia_id, id=r_usuario.id)

                        try:
                            """comprobar si existe registro de salida null"""
                            r_acceso = Acceso.objects.get(id_usuario_id=r_usuario.id, id_dependencia_id=r_dependencia.id, id_lector_id=r_lector.id, fecha_hora_salida=None)

                            """Disminuimos el aforo actual"""
                            r_dependencia.aforo_actual -= 1
                            r_dependencia.save()

                            """registramos la salida"""
                            r_acceso.fecha_hora_salida = fechaActual
                            r_acceso.save()

                            """Salida Correcta"""
                            Lectura.save(Lectura(
                                id_lector=recibidos["id_lector"],
                                fecha_hora=fechaActual,
                                estado=6,
                                contenido=datos
                            ))

                            return Response(status=status.HTTP_200_OK)

                        except Acceso.DoesNotExist:

                            if r_dependencia.aforo_actual < r_dependencia.aforo_maximo:

                                """registramos entrada"""

                                d_acceso=Acceso(
                                    id_lector_id=r_lector.id,
                                    id_usuario_id=r_usuario.id,
                                    id_dependencia_id=r_dependencia.id
                                )

                                d_acceso.save()

                                """Aumentamos el aforo actual"""
                                r_dependencia.aforo_actual += 1
                                r_dependencia.save()

                                """Entrada Correcta"""
                                Lectura.save(Lectura(
                                    id_lector=recibidos["id_lector"],
                                    fecha_hora=fechaActual,
                                    estado=7,
                                    contenido=datos
                                ))

                                return Response(status=status.HTTP_200_OK)

                            else:

                                """Error usuario no tiene permisos"""
                                Lectura.save(Lectura(
                                    id_lector=recibidos["id_lector"],
                                    fecha_hora=fechaActual,
                                    estado=5,
                                    contenido=datos
                                ))

                                return Response(status=status.HTTP_401_UNAUTHORIZED)


                    except Usuario.DoesNotExist:

                        """Error usuario no tiene permisos"""
                        Lectura.save(Lectura(
                            id_lector=recibidos["id_lector"],
                            fecha_hora=fechaActual,
                            estado=4,
                            contenido=datos
                        ))

                        return Response(status=status.HTTP_401_UNAUTHORIZED)

                except Usuario.DoesNotExist:

                    """Error de Usuario"""
                    Lectura.save(Lectura(
                        id_lector=recibidos["id_lector"],
                        fecha_hora=fechaActual,
                        estado=3,
                        contenido=datos
                    ))

                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Lectore.DoesNotExist:
                """Error de lector"""
                Lectura.save(Lectura(
                    id_lector=recibidos["id_lector"],
                    fecha_hora=fechaActual,
                    estado=2,
                    contenido=datos
                ))

                return Response(status=status.HTTP_401_UNAUTHORIZED)



        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)



