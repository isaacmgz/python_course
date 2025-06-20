from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Owner, Mascota

class BienvenidaView(View):
    def get(self, request):
        return render(request, 'bienvenida/bienvenida.html')

class ServiciosView(View):
    def get(self, request):
        return render(request, 'bienvenida/servicios.html')

def registro_dueno(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        owner = Owner.objects.create(name=name, phone=phone, address=address)
        request.session['owner_id'] = owner.id  # Guardar el dueño en sesión
        return redirect('registro_mascota')
    return render(request, 'bienvenida/registro_dueno.html')

def registro_mascota(request):
    owner_id = request.session.get('owner_id')
    if not owner_id:
        return redirect('registro_dueno')
    if request.method == 'POST':
        name = request.POST['name']
        species = request.POST['species']
        breed = request.POST['breed']
        age = request.POST['age']
        owner = Owner.objects.get(id=owner_id)
        Mascota.objects.create(name=name, species=species, breed=breed, age=age, owner=owner)
        del request.session['owner_id']
        return redirect('servicios')
    return render(request, 'bienvenida/registro_mascota.html')

def lista_duenos(request):
    duenos = Owner.objects.all()
    return render(request, 'bienvenida/lista_duenos.html', {'duenos': duenos})

def lista_mascotas(request):
    mascotas = Mascota.objects.select_related('owner').all()
    return render(request, 'bienvenida/lista_mascotas.html', {'mascotas': mascotas})

