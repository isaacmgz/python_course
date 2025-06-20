from django.urls import path
from . import views

urlpatterns = [
    path('class', views.BienvenidaView.as_view(), name='bienvenida'),
    path('servicios', views.ServiciosView.as_view(), name='servicios'),
    path('cita', views.CitaView.as_view(), name='cita'),
]