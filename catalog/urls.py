from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ZonaListView.as_view(), name='zonas'),
    path('zona/<numero>/', views.ZonaDetailView.as_view(), name='zona-detail'),
    path('cambia/', views.ZonaDetailView.as_view(), name='cambia'),
]
