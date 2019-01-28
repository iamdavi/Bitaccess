from django.shortcuts import render
from django.views import generic
from .models import Zona

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
