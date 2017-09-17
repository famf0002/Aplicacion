# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import *

# Register your models here.
from webService.forms import UsuarioForm


class admin_emplazamiento(admin.ModelAdmin):
    list_display = ['id','nombre','direccion','poblacion','provincia','cp','pais']
    list_filter = ['id','nombre','direccion','poblacion','provincia','cp','pais','coordenadas']

admin.site.register(Emplazamiento, admin_emplazamiento)


class admin_dependencia(admin.ModelAdmin):
    list_display = ['id', 'id_emplazamiento','nombre']
    list_filter = ['id', 'id_emplazamiento', 'nombre']


admin.site.register(Dependencia, admin_dependencia)

class admin_lectore(admin.ModelAdmin):
    list_display = ['id', 'id_dependencia', 'nombre']
    list_filter = ['id', 'id_dependencia', 'nombre']


admin.site.register(Lectore, admin_lectore)

class admin_grabador(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    list_filter = ['id', 'nombre']


admin.site.register(Grabador, admin_grabador)

class admin_usuario(admin.ModelAdmin):
    readonly_fields = ['update_uid_link']
    list_display = ['id', 'nombre', 'apellido', 'dni', 'direccion', 'poblacion', 'provincia', 'cp', 'pais']
    list_filter = ['id', 'nombre', 'apellido', 'dni', 'direccion', 'poblacion', 'provincia', 'cp', 'pais', 'permisos']
    form = UsuarioForm

admin.site.register(Usuario, admin_usuario)


class admin_lectura(admin.ModelAdmin):
    list_display = ['id',  'id_lector', 'fecha_hora', 'estado', 'contenido']
    list_filter = ['id',  'id_lector', 'fecha_hora', 'estado', 'contenido']


admin.site.register(Lectura,admin_lectura)


class admin_acceso(admin.ModelAdmin):
    list_display = ['id_usuario', 'id_dependencia', 'id_lector', 'fecha_hora_entrada', 'fecha_hora_salida']
    list_filter = ['id_usuario', 'id_dependencia', 'id_lector', 'fecha_hora_entrada', 'fecha_hora_salida']


admin.site.register(Acceso, admin_acceso)