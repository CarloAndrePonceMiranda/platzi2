from django.contrib import admin
from .models import Course

# Register your models here.
@admin.register(Course)
class AdminPlayera(admin.ModelAdmin):
	list_display = ('Nombre', 'Fecha_inicio', 'Fecha_fin')
	list_filter = ('Fecha_inicio',)