from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.ZonaListView.as_view(), name='zonas'),
    path('zona/<pk>/', views.ZonaDetailView.as_view(), name='zona-detail'),
    path('cambia/', views.ZonaDetailView.as_view(), name='cambia'),
]
