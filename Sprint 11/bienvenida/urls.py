from django.urls import path
from . import views

urlpatterns = [
    path('class', views.BienvenidaView.as_view(), name='bienvenida'),
    path('servicios', views.ServiciosView.as_view(), name='servicios'),
    path('registro-dueno', views.registro_dueno, name='registro_dueno'),
    path('registro-mascota', views.registro_mascota, name='registro_mascota'),
    path('lista-duenos', views.lista_duenos, name='lista_duenos'),         # <-- Cambiado aquí
    path('lista-mascotas', views.lista_mascotas, name='lista_mascotas'),   # <-- Cambiado aquí
]