from django.contrib import admin 
from .models import Zona,Puerto,Empleado, RegistroAula, ConjuntoZona

# Register your models here.

class PuertoInline(admin.TabularInline):
    model = Puerto
    extra = 0

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("num_zona", "descripcion", "ip", "modelo", "tipo")
    fieldsets = (
        ('Zona', {
            'fields': ['num_zona', ('tipo', 'descripcion'),'dentro']
        }),
        ('Dispositivo', {
            'fields': ('ip', 'modelo')
        }),
    )
    inlines = [PuertoInline]

@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ("ip", "num_puerto", "descripcion")

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("user", "rfid","dentro")
    fields = ['user', 'rfid', 'dentro']

@admin.register(RegistroAula)
class RegistroAula(admin.ModelAdmin):
    list_display=("rfid", "ip",  "f_salida", "dentro")
    fields = ['rfid', 'ip', 'f_entrada', 'f_salida', 'dentro']

@admin.register(ConjuntoZona)
class ConjuntoZona(admin.ModelAdmin):
    list_display=("conjunto_zona",)
    fields = ['conjunto_zona', ('zona', 'grupos_con_acceso')]
