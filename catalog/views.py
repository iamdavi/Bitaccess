from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Zona, Puerto
from django.views.generic.detail import DetailView


# Create your views here.

class ZonaListView(generic.ListView):
    """
    Clase para listar todas las Zonas
    """
    model = Zona
    paginate_by = 10

class ZonaDetailView(generic.DetailView):
    """
    Clase para mostrar la informazión de una zona (puertos,descripcion...)
    """
    model = Zona

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
            puerto.encendido = int(estado)
            puerto.save()
