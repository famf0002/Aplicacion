# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from webService.grabarRFID import grabarRFID


# Create your views here.
from webService.models import Usuario, Grabador


def update_uid_view(request):

    user = request.GET.get('user', None)
    usuario = get_object_or_404(Usuario, pk=user)

    try:
        puerto=Grabador.objects.get(id=usuario.grabador_id).puerto
        print puerto
        usuario.uid=grabarRFID().grabar(
            puerto= puerto,
            dni= usuario.dni)

        if usuario.uid != None:
            usuario.save()
            return HttpResponseRedirect( reverse('admin:webService_usuario_change', args=(usuario.pk,)))
        else:
            return HttpResponseRedirect(reverse('admin:webService_usuario_change',
                                                args=(usuario.pk,),), ValidationError("Error al grabar la tarjeta"))

    except:
        return HttpResponseRedirect(reverse('admin:webService_usuario_change',
                                            args=(usuario.pk, )), ),ValidationError("Error al grabar la tarjeta")

