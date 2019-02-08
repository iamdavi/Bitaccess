from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Zona, Puerto, Empleado, RegistroAula, ConjuntoZona, ConjuntoPuerto
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Usado para enviar orden al arduino
from socket import *
import time
from django.http import HttpResponse, JsonResponse

# Create your views here.

class ZonaListView(LoginRequiredMixin, generic.ListView):
    """
    Clase para listar todas las Zonas
    """
    model = Zona
    paginate_by = 10

    def get_queryset(self):
        """
        Método usado para saber el estado de la zona
        """
        empleado = Empleado.objects.get(user=self.request.user) # Obtener usuario logeado
        zonas = get_zonas_user(self.request.user) # Obtener zonas de la class ConjuntoZona
        zonas = zonas.distinct() # Eliminar los objetos duplicado
        return zonas

class ZonaDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Clase para mostrar la informazión de una zona (puertos,descripcion...)
    """
    model = Zona

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupos = Empleado.objects.get(user=self.request.user).grupo.all() 
        # Obtener los conjuntos a los que tiene acceso todos los grupos del usuario
        conjuntos = ConjuntoPuerto.objects.filter(grupos_con_acceso__in=grupos)
        puertos = Puerto.objects.none()

        for conjunto in conjuntos:
            puertos |= conjunto.puertos.filter(zona=self.object)
            # Extraer todos los puertos a los que se tiene permiso en la zona 
        puertos = puertos.distinct()
        context['puertos'] = puertos
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            # Recogida de datos enviados por Ajax en el template
            id_zona = request.POST['aulaId']
            num_puerto = request.POST['numPuerto']
            estado = request.POST['estado']
            # Extraer el puerto del que se quiere cambiar el estado
            puerto = Puerto.objects.get(zona__ip=id_zona, num_puerto=num_puerto)
            puerto.encendido = int(estado)
            puerto.save()

            #Envio de la orden de cambio al arduino
            address= ( id_zona, 5001) # Definimos la IP del arduino y del puerto
            client_socket = socket(AF_INET, SOCK_DGRAM) # Preparamos el socket
            client_socket.settimeout(1) # Only wait 1 second for a response

            if estado == '1':
                valor_arduino = num_puerto + "on"
                # mensaje que va a ser leido por el arduino
            else:
                valor_arduino = num_puerto + "off"

            client_socket.sendto(valor_arduino.encode(), address) # Enviar orden al arduino

            return JsonResponse({})

def get_zonas_user(user):
    """
    Método para extraer las zonas a las que tiene acceso
    un usuario mediante la class ConjuntoZona
    """
    grupos = Empleado.objects.get(user=user).grupo.all()
    zonas = Zona.objects.none()
    for grupo in grupos:
        conjuntos_zona = ConjuntoZona.objects.filter(grupos_con_acceso=grupo)
        for conjunto in conjuntos_zona:
            zonas |= conjunto.zona.all()
    return zonas
