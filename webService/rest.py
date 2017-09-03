from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import *
import json

@api_view(['GET'])
def comprobarAcceso(request,datos):

    if request.method == 'GET':
        print datos
        recividos = json.loads(datos)
        print recividos["id_sala"]
        print recividos["uid"]
        print recividos["dni"]
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)