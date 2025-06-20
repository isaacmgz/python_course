from django.urls import path
from . import views

urlpatterns = [
    path('class', views.BienvenidaView.as_view(), name='bienvenida'),
    path('servicios', views.ServiciosView.as_view(), name='servicios'),
    path('registro-dueno', views.registro_dueno, name='registro_dueno'),
    path('registro-mascota', views.registro_mascota, name='registro_mascota'),
    path('lista-duenos', views.lista_duenos, name='lista_duenos'),
    path('lista-mascotas', views.lista_mascotas, name='lista_mascotas'),
    path('cita/seleccionar-dia', views.seleccionar_dia, name='seleccionar_dia'),
    path('cita/seleccionar-horario', views.seleccionar_horario, name='seleccionar_horario'),
    path('cita/elegir-horario', views.elegir_horario, name='elegir_horario'),
    path('conoce-mas', views.conoce_mas, name='conoce_mas'),
    path('cita/confirmacion/<int:cita_id>/', views.confirmacion_cita, name='confirmacion_cita'),
]