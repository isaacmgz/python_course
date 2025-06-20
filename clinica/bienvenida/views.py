from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class BienvenidaView(View):
    def get(self, request):
        return render(request, 'bienvenida/bienvenida.html')

class ServiciosView(View):
    def get(self, request):
        return render(request, 'bienvenida/servicios.html')

class CitaView(View):
    def get(self, request):
        return render(request, 'bienvenida/cita.html')