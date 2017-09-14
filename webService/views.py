# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


# Create your views here.
from webService.models import Usuario


def update_uid_view(request):

    user = request.GET.get('user', None)
    """if user is None: raise Http404()"""

    usuario = get_object_or_404(Usuario, pk=user)

    """No sé retornar los datos al formulario"""
    usuario.uid = usuario.get_UID_from_servidor()
    usuario.save()
    return HttpResponseRedirect(reverse('admin:webService_usuario_change', args=(usuario.pk,)))

