from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ZonaListView.as_view(), name='zonas'),
    url(r'^zona/(?P<pk>\d+)$', views.ZonaDetailView.as_view(), name='zona-detail'),
]
