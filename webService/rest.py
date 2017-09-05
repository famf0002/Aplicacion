# -*- coding: utf-8 -*-
import datetime
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Lectore, Lectura, Usuario, Dependencia

"""
ESTADOS DE ERROR:
    ESTADOS = (
        ('1', 'OK'),
        ('2', 'ERR. LECTOR NO EXISTE'),
        ('3', 'ERR. USUARIO NO EXISTE'),
        ('4', 'ERR. USUARIO NO TIENE PERMISOS'),
        ('5', 'ERR. AFORO LLENO'),
    )
"""


@api_view(['GET'])
def comprobarAcceso(request, datos):
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

            try:

                """Se comprueba el Aforo de la dependencia"""

                if Dependencia.objects.get(id=r_lector.id_dependencia_id).aforo_maximo >= Dependencia.objects.get(id=r_lector.id_dependencia_id).aforo_actual:
                    """Error de Aforo Dependencia lleno"""
                    Lectura.save(Lectura(
                        id_lector=recibidos["id_lector"],
                        fecha_hora=fechaActual,
                        estado=5,
                        contenido=datos
                    ))

                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                else:

                    try:
                        """Se comprueba si el usuario exite"""
                        r_usuario=Usuario.objects.get(dni=recibidos["dni"],uid=recibidos["uid"])

                        try:

                            """Se comprueba si el usuario tiene permiso para acceder a la sala"""

                        except:

                            """Error usuario no tiene permisos"""
                            Lectura.save(Lectura(
                                id_lector=recibidos["id_lector"],
                                fecha_hora=fechaActual,
                                estado=4,
                                contenido=datos
                            ))

                            return Response(status=status.HTTP_401_UNAUTHORIZED)


                    except:

                        """Error usuario no Existe"""
                        Lectura.save(Lectura(
                            id_lector=recibidos["id_lector"],
                            fecha_hora=fechaActual,
                            estado=3,
                            contenido=datos
                        ))

                        return Response(status=status.HTTP_401_UNAUTHORIZED)


            except:

                """Error de Aforo Dependencia lleno"""
                Lectura.save(Lectura(
                    id_lector=recibidos["id_lector"],
                    fecha_hora=fechaActual,
                    estado=5,
                    contenido=datos
                ))

                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except:
            """Error de lector"""
            Lectura.save(Lectura(
                id_lector=recibidos["id_lector"],
                fecha_hora=fechaActual,
                estado=2,
                contenido=datos
            ))

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        """¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡BORRAR!!!!!!!!!!!!!!!!!"""
        return Response(status=status.HTTP_202_ACCEPTED)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
