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
        empleado = Empleado.objects.get(user=self.request.user)
        zonas = get_zonas_user(self.request.user)

        for zona in zonas:
            if zona.dentro:
                resgistros = RegistroAula.objects.filter(rfid=empleado.rfid)
                for registro in resgistros:
                    if registro.dentro:
                        zona.usuario_dentro = True
        return zonas

class ZonaDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Clase para mostrar la informazión de una zona (puertos,descripcion...)
    """
    model = Zona
    paginate_by = 10

    def get_queryset(self):
        """
        Método para listar puertos
        """
        empleado = Empleado.objects.get(user=self.request.user)
        puertos = get_puertos_user(self.request.user)
        return puertos


    def get_object(self, queryset=None):
        zona = get_object_or_404(Zona, num_zona=self.kwargs['numero'])
        self.kwargs['pk'] = zona.ip
        return super(ZonaDetailView, self).get_object(queryset=queryset)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id_zona = request.POST['aulaId']
            num_puerto = request.POST['numPuerto']
            estado = request.POST['estado']
            puerto = Puerto.objects.get(ip=id_zona, num_puerto=num_puerto)
            cambio_realizado = {
                'ip_dispositivo': id_zona,
                'numero_puerto': num_puerto,
                'nuevo_estado': estado
            }
            puerto.encendido = int(estado)
            puerto.save()

            address= ( id_zona, 5001) #define server IP and port
            client_socket = socket(AF_INET, SOCK_DGRAM) #Set up the Socket
            client_socket.settimeout(1) #Only wait 1 second for a response

            if estado == '1':
                valor_arduino = num_puerto + "on"
            else:
                valor_arduino = num_puerto + "off"

            client_socket.sendto(valor_arduino.encode(), address) #Send the data request

            return JsonResponse({})

def get_zonas_user(user):
    grupos = user.groups.all()
    zonas = Zona.objects.none()
    for grupo in grupos:
        conjuntos_zona = ConjuntoZona.objects.filter(grupos_con_acceso=grupo)
        for conjunto in conjuntos_zona:
            zonas |= conjunto.zona.all()
    return zonas

def get_puertos_user(user):
    grupos = user.groups.all()
    puertos = Puerto.objects.none()
    for grupo in grupos:
        conjuntos_puerto = ConjuntoPuerto.objects.filter(grupos_con_acceso=grupo)
        for conjunto in conjuntos_puerto:
            puertos |= conjunto.puerto.all()
    return puertos
