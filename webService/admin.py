# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import *

# Register your models here.


class admin_emplazamiento(admin.ModelAdmin):
    list_display = ['id','nombre','direccion','poblacion','provincia','cp','pais']
    list_filter = ['id','nombre','direccion','poblacion','provincia','cp','pais','coordenadas']

admin.site.register(Emplazamiento, admin_emplazamiento)


class admin_dependencia(admin.ModelAdmin):
    list_display = ['id', 'id_emplazamiento','nombre']
    list_filter = ['id', 'id_emplazamiento', 'nombre']


admin.site.register(Dependencia, admin_dependencia)


class admin_evento(admin.ModelAdmin):
    list_display = ['id', 'id_dependencia', 'nombre', 'fecha_hora_inicio', 'fecha_hora_fin', 'aforo_maximo',
                    'aforo_actual']
    list_filter = ['id', 'id_dependencia', 'nombre', 'fecha_hora_inicio', 'fecha_hora_fin', 'aforo_maximo',
                     'aforo_actual']


admin.site.register(Evento, admin_evento)


class admin_lectore(admin.ModelAdmin):
    list_display = ['id', 'id_dependencia', 'nombre']
    list_filter = ['id', 'id_dependencia', 'nombre']


admin.site.register(Lectore, admin_lectore)

class admin_grabador(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    list_filter = ['id', 'nombre']


admin.site.register(Grabador, admin_grabador)

class admin_usuario(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'dni', 'direccion', 'poblacion', 'provincia', 'cp', 'pais']
    list_filter = ['id', 'nombre', 'apellido', 'dni', 'direccion', 'poblacion', 'provincia', 'cp', 'pais', 'permisos']


admin.site.register(Usuario, admin_usuario)


class admin_lectura(admin.ModelAdmin):
    list_display = ['id', 'id_usuario', 'id_lector', 'fecha_hora', 'estado', 'contenido']
    list_filter = ['id', 'id_usuario', 'id_lector', 'fecha_hora', 'estado', 'contenido']


admin.site.register(Lectura,admin_lectura)


class admin_acceso(admin.ModelAdmin):
    list_display = ['id_usuario', 'id_evento', 'id_lector', 'fecha_hora_entrada', 'fecha_hora_salida']
    list_filter = ['id_usuario', 'id_evento', 'id_lector', 'fecha_hora_entrada', 'fecha_hora_salida']


admin.site.register(Acceso, admin_acceso)