# -*- coding: utf-8 -*-
import datetime
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Evento, Lectore, Lectura, Usuario

"""
ESTADOS DE ERROR:
    ESTADOS = (
        ('1', 'OK'),
        ('2', 'ERR. LECTOR NO EXISTE'),
        ('3', 'ERR. USUARIO NO EXISTE'),
        ('4', 'ERR. USUARIO NO TIENE PERMISOS'),
        ('5', 'ERR. EVENTO NO EXISTE'),
        ('6', 'ERR. EVENTO NO ACTIVO'),
        ('7', 'ERR. AFORO LLENO'),
    )
"""

@api_view(['GET'])
def comprobarAcceso(request,datos):

    if request.method == 'GET':
        print datos
        recibidos = json.loads(datos)
        print recibidos["id_sala"]
        print recibidos["uid"]
        print recibidos["dni"]
        fechaActual = datetime.datetime.now().replace(microsecond=0)
        print fechaActual



        try:
            """Recoge los eventos de la sala asociada al lector en ese momento"""
            evento = Evento.objects.get(id_dependencia=
                                       Lectore.objects.get(id=int(recibidos["id_sala"])).id_dependencia_id,
                                       fecha_hora_inicio__lt=fechaActual,
                                       fecha_hora_fin__gt=fechaActual
                                       )
            print "ok"
            """Vemos si hay aforo disponible"""
            if evento.aforo_actual >= evento.aforo_maximo:
                """
                Si no hay aforo se retorna un error 400 al lector RFID y guardamos en la tabla lectura un log 
                con los datos que llegan en la petición GET
                """
                estado = 7
                Lectura.save(Lectura(fecha_hora=fechaActual,estado=estado,contenido=recibidos,id_lector_id=recibidos["id_sala"]))
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Evento.DoesNotExist:
            print "Evento no existe 5"

            """
            si no existe evento se retorna un error 400 al lector RFID y guardamos en la tabla lectura un log 
            con los datos que llegan en la petición GET
            """
            estado = 5
            Lectura.save(Lectura(fecha_hora=fechaActual, estado=estado, contenido=recibidos, id_lector_id=recibidos["id_sala"]))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(dni=recibidos["dni"])

        except Usuario.DoesNotExist:
            print "Usuario no existe"
            """
            si no existe evento se retorna un error 400 al lector RFID y guardamos en la tabla lectura un log 
            con los datos que llegan en la petición GET
            """
            estado = 3
            Lectura.save(
                Lectura(fecha_hora=fechaActual, estado=estado, contenido=recibidos, id_lector_id=recibidos["id_sala"]))
            return Response(status=status.HTTP_400_BAD_REQUEST)




        try:

            consulta6 = Usuario.objects.get(dni=recibidos["dni"])
            evento = consulta6.permisos
            try:
             consulta7 = Evento.objects.filter(id_dependencia=consulta6.permisos)
            except Evento.DoesNotExist:
                print 'Prueba evento no existe 1'
                estado = 4
                # evento=consulta7.ecoger l
                print "----------------------"
                print evento
                print "----------------------"
                print consulta7
                print "----------------------"
                consulta8 = Usuario.objects.filter(evento__pk=evento.id)
                print consulta8

                print 'Prueba'
                print consulta7


            print "----------------------"
            for obj in Usuario.objects.get(dni=recibidos["dni"]).permisos:
                for obj2 in obj:
                    print obj2

            print "----------------------"
        except Usuario.DoesNotExist:
            estado = 4
            Lectura.save(
                Lectura(fecha_hora=fechaActual, estado=estado, contenido=recibidos, id_lector_id=recibidos["id_sala"]))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)