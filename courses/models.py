from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Course(models.Model):
    Nombre = models.CharField(max_length=140)
    Fecha_inicio = models.DateTimeField()
    Fecha_fin = models.DateTimeField()
    Imagen = models.ImageField(blank=True)

def __str__(self):
        return self.Nombre