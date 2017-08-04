# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


"""
La Clase Organización almacena los datos de las organizaciones, empresas o personas
"""


class Organizacion(models.Model):
    razon_social = models.CharField(max_length=30, null=True)
    nif_cif = models.CharField(max_length=10)
    direccion = models.CharField(max_length=30, null=False)
    poblacion = models.CharField(max_length=30, null=False)
    provincia = models.CharField(max_length=30, null=False)
    cp = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(99999)], null=False)
    pais = models.CharField(max_length=30, null=False)


"""
La clase emplazamientos almacena los edificios de una organización
"""


class Emplazamientos(models.Model):
    id_organizacion = models.ForeignKey(Organizacion)
    nombre = models.CharField(max_length=30, null=False)
    direccion = models.CharField(max_length=30, null=False)
    poblacion = models.CharField(max_length=30, null=False)
    provincia = models.CharField(max_length=30, null=False)
    cp = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(99999)], null=False)
    pais = models.CharField(max_length=30, null=False)
    coordenadas = models.CharField(max_length=30, null=True)


"""
La Clase dependencias, almacena los datos de las dependencias de un edificio
"""


class Dependencias(models.Model):
    id_emplazamiento = models.ForeignKey(Emplazamientos)
    nombre = models.CharField(max_length=30, null=False)
    aforo_maximo = models.PositiveIntegerField(null=False)


"""
La Clase Lectores almacenan los lectores de tarjetas que hay en cada dependencia
"""


class Lectores(models.Model):
    id_dependencia = models.ForeignKey(Dependencias)
    nombre = models.CharField(max_length=30, null=False)


"""
La Clase Eventos, almacena los eventos que hay en una dependencia, reuniones, cursos....
"""


class Eventos(models.Model):
    id_dependencia = models.ForeignKey(Dependencias)
    nombre = models.CharField(max_length=30, null=False)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    aforo_maximo = models.PositiveIntegerField(null=False)
    aforo_actual = models.PositiveIntegerField(null=False, default=0)

class Usuarios(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    id_organizacion = models.ForeignKey('Organizacion')
    dni = models.CharField(max_length=9, null=False, unique=True)
    direccion = models.CharField(max_length=30, null=False)
    poblacion = models.CharField(max_length=30, null=False)
    provincia = models.CharField(max_length=30, null=False)
    cp = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(99999)], null=False)
    pais = models.CharField(max_length=30, null=False)
    permisos = models.ManyToManyField(Eventos)


@receiver(post_save, sender=User)
def create_user_profiler(sender, intance, created, **kwargs):
    if created:
        Usuarios.objects.create(user=intance)


class Lecturas(models.Model):

    ESTADOS = (
        ('1', 'OK'),
        ('2', 'ERR. LECTOR NO EXISTE'),
        ('3', 'ERR. USUARIO NO EXISTE'),
        ('4', 'ERR. USUARIO NO TIENE PERMISOS'),
        ('5', 'ERR. EVENTO NO EXISTE'),
        ('6', 'ERR. EVENTO NO ACTIVO'),
    )

    id_usuario = models.ForeignKey(Usuarios)
    id_lector = models.ForeignKey(Lectores)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADOS)
    contenido = models.CharField(max_length=300)

class Accesos(models.Model):
    id_usuario = models.ForeignKey(Usuarios)
    id_eventos = models.ForeignKey(Eventos)
    id_lector = models.ForeignKey(Lectores)
    fecha_hora_entrada = models.DateTimeField(null=False, default=datetime.datetime.now())
    fecha_hora_salida = models.DateTimeField(null=True,default=None)
