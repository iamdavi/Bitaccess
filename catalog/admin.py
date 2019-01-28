from django.contrib import admin

# Register your models here.

from .models import Zona,Puerto,Empleado, PermisosAula, PermisosPuerto

# @admin.register(Puerto)
# class PuertoInline(admin.TabularInline):
#     model=Puerto
#     extra = 0

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display=("num_aula","ip","modelo","tipo","descripcion")
    fields=['num_aula',('ip','modelo'),('tipo','descripcion')]
    # inlines=[PuertoInline]

@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display=("ip","num_puerto","descripcion")

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display=("user","rfid")

@admin.register(PermisosAula)
class PermisosAula(admin.ModelAdmin):
    list_display=("grupo","zona")

@admin.register(PermisosPuerto)
class PermisosPuerto(admin.ModelAdmin):
    list_display=("grupo","puerto")
