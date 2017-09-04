# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, get_object_or_404


# Create your views here.
from webService.models import Usuario


def update_uid_view(request):
    user = request.GET('user', None)
    if user is None:
        raise Http404()

    usuario = get_object_or_404(Usuario, pk=user)
    usuario.get_UUID_from_servidor()