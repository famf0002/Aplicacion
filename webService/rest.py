import datetime
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Evento, Dependencia,Lectore


@api_view(['GET'])
def comprobarAcceso(request,datos):

    if request.method == 'GET':
        print datos
        recibidos = json.loads(datos)
        print recibidos["id_sala"]
        fechaActual = datetime.datetime.now().replace(microsecond=0)
        print fechaActual

        consulta1=Lectore.objects.get(id=int(recividos["id_sala"]))
        consulta2=Evento.objects.get(id_dependencia=consulta1.id_dependencia)
        print consulta2
        if consulta2.fecha_hora_inicio.replace(tzinfo=None) < fechaActual < consulta2.fecha_hora_fin.replace(tzinfo=None):
            #evento = Evento.objects.get(
            #   id=Dependencia.objects.get(
            #      id=int(Lectore.objects.get(id=int(recividos["id_sala"])).id_dependencia)
            # )
            #).filter(fecha_hora_inicio__gt=fechaActual, fecha_hora_fin__lt=fechaActual)

            print "evento: " + str(consulta2.id)



        print recibidos["uid"]
        print recibidos["dni"]
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)