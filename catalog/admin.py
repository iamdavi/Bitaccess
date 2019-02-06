from django.contrib import admin 
from .models import Zona,Puerto,Empleado, RegistroAula, ConjuntoZona, ConjuntoPuerto

# Register your models here.

class PuertoInline(admin.TabularInline):
    model = Puerto
    extra = 0

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ("id_zona", "descripcion")
    fieldsets = (
        ('Zona', {
            'fields': ['id_zona','descripcion']
        }),
        ('Dispositivo', {
            'fields': ('ip', 'modelo')
        }),
    )
    inlines = [PuertoInline]

@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ("zona", "num_puerto", "descripcion")

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("user", "rfid")
    fields = ['user', 'rfid', 'dentro', 'grupo']

@admin.register(RegistroAula)
class RegistroAula(admin.ModelAdmin):
    list_display=("rfid", "ip",  "f_entrada", "f_salida")
    fields = ['rfid', 'ip', 'f_entrada', 'f_salida']

@admin.register(ConjuntoZona)
class ConjuntoZona(admin.ModelAdmin):
    list_display=("conjunto_zona",)
    fields = ['conjunto_zona', ('zona', 'grupos_con_acceso')]

@admin.register(ConjuntoPuerto)
class ConjuntoZona(admin.ModelAdmin):
    list_display=("conjunto_puerto",)
    fields = ['conjunto_puerto', ('puertos', 'grupos_con_acceso')]
