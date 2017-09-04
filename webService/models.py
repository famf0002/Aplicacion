# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

"""
La clase emplazamientos almacena los edificios de una organización
"""


class Emplazamiento(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    direccion = models.CharField(max_length=30, null=False)
    poblacion = models.CharField(max_length=30, null=False)
    provincia = models.CharField(max_length=30, null=False)
    cp = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(99999)], null=False)
    pais = models.CharField(max_length=30, null=False)
    coordenadas = models.CharField(max_length=30, null=True)

    def __str__(self):
        return (self.nombre)


"""
La Clase dependencias, almacena los datos de las dependencias de un edificio
"""


class Dependencia(models.Model):
    id_emplazamiento = models.ForeignKey(Emplazamiento)
    nombre = models.CharField(max_length=30, null=False)
    aforo_maximo = models.PositiveIntegerField(null=False)

    def __str__(self):
        return (self.nombre)



"""
    La Clase Lectores almacenan los lectores de tarjetas que hay en cada dependencia
"""


class Lectore(models.Model):
    id_dependencia = models.ForeignKey(Dependencia)
    nombre = models.CharField(max_length=30, null=False)

    def __str__(self):
        return (self.nombre)

"""
    La Clase Lectores almacenan los lectores de tarjetas que hay en cada dependencia
"""


class Grabador(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    puerto = models.PositiveIntegerField(null=False)

    def __str__(self):
        return (self.nombre)


"""
La Clase Eventos, almacena los eventos que hay en una dependencia, reuniones, cursos....
"""


class Evento(models.Model):
    id_dependencia = models.ForeignKey(Dependencia)
    nombre = models.CharField(max_length=30, null=False)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    aforo_maximo = models.PositiveIntegerField(null=False)
    aforo_actual = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        return (self.nombre)


class Usuario(models.Model):
    uid = models.CharField(max_length=100, null=True)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)
    dni = models.CharField(max_length=9, null=True, unique=True)
    direccion = models.CharField(max_length=30, null=True)
    poblacion = models.CharField(max_length=30, null=True)
    provincia = models.CharField(max_length=30, null=True)
    cp = models.PositiveIntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(99999)], null=True)
    pais = models.CharField(max_length=30, null=True)
    grabador = models.ForeignKey(Grabador)
    permisos = models.ManyToManyField(Evento)

    @property
    def update_uid_link(self):
        return mark_safe("<a href='%s?user=%s'>Actualizar UID</a>" % (reverse('update_uid'),  self.pk))

    def get_UID_from_servidor(self):
        """Aquí se ejecuta la clase para recoger el UID"""
        uid = "056055054053052051050049098000000000000000000000"
        return uid

    def __str__(self):
        return (self.nombre)



class Lectura(models.Model):

    ESTADOS = (
        ('1', 'OK'),
        ('2', 'ERR. LECTOR NO EXISTE'),
        ('3', 'ERR. USUARIO NO EXISTE'),
        ('4', 'ERR. USUARIO NO TIENE PERMISOS'),
        ('5', 'ERR. EVENTO NO EXISTE'),
        ('6', 'ERR. EVENTO NO ACTIVO'),
        ('7', 'ERR. AFORO LLENO'),
    )

    id_lector = models.ForeignKey(Lectore)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADOS)
    contenido = models.CharField(max_length=300)

class Acceso(models.Model):
    id_usuario = models.ForeignKey(Usuario)
    id_evento = models.ForeignKey(Evento)
    id_lector = models.ForeignKey(Lectore)
    fecha_hora_entrada = models.DateTimeField(null=False, default=datetime.datetime.now())
    fecha_hora_salida = models.DateTimeField(null=True,default=None)
