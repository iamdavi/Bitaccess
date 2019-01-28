from django.contrib import admin 
from .models import Zona,Puerto,Empleado, PermisosAula, PermisosPuerto

# Register your models here.

class PuertoInline(admin.TabularInline):
    model = Puerto
    extra = 0

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("num_zona", "ip", "modelo", "tipo", "descripcion")
    fields = ['num_zona', ('ip', 'modelo'), ('tipo', 'descripcion')]
    inlines = [PuertoInline]

@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ("ip", "num_puerto", "descripcion")

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("user", "rfid")
    fields = ['user', 'rfid']

@admin.register(PermisosAula)
class PermisosAula(admin.ModelAdmin):
    list_display = ("grupo", "zona")

@admin.register(PermisosPuerto)
class PermisosPuerto(admin.ModelAdmin):
    list_display = ("grupo", "puerto")
