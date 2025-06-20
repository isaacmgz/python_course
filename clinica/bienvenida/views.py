from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Owner, Mascota, Cita
from datetime import date, timedelta, time, datetime

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
        mascota = Mascota.objects.create(name=name, species=species, breed=breed, age=age, owner=owner)
        # Crear la cita
        dia = request.session.get('cita_dia')
        horario = request.session.get('cita_horario')
        if dia and horario:
            # Convertir horario a objeto time si es string
            if isinstance(horario, str):
                try:
                    horario_obj = datetime.strptime(horario, "%H:%M").time()
                except ValueError:
                    horario_obj = datetime.strptime(horario, "%I %p").time()  # fallback por si acaso
            else:
                horario_obj = horario
            cita = Cita.objects.create(date=dia, time=horario_obj, owner=owner, mascota=mascota)
            # Limpia la sesión
            del request.session['cita_dia']
            del request.session['cita_horario']
        del request.session['owner_id']
        return redirect('confirmacion_cita', cita_id=cita.id)
    return render(request, 'bienvenida/registro_mascota.html')

def lista_duenos(request):
    duenos = Owner.objects.all()
    cita_id = request.GET.get('cita_id')
    return render(request, 'bienvenida/lista_duenos.html', {'duenos': duenos, 'cita_id': cita_id})

def lista_mascotas(request):
    mascotas = Mascota.objects.select_related('owner').all()
    cita_id = request.GET.get('cita_id')  # o de la sesión, según tu flujo
    return render(request, 'bienvenida/lista_mascotas.html', {'mascotas': mascotas, 'cita_id': cita_id})

def seleccionar_dia(request):
    dias = [date.today() + timedelta(days=i) for i in range(7)]
    return render(request, 'bienvenida/seleccionar_dia.html', {'dias': dias})

def seleccionar_horario(request):
    dia = request.GET.get('dia')
    horarios = [time(10,0), time(11,0), time(12,0), time(14,0), time(15,0), time(16,0)]
    ocupados = Cita.objects.filter(date=dia).values_list('time', flat=True)
    disponibles = [h for h in horarios if h not in ocupados]
    return render(request, 'bienvenida/seleccionar_horario.html', {'dia': dia, 'horarios': disponibles})

def elegir_horario(request):
    if request.method == 'POST':
        dia = request.POST['dia']
        horario = request.POST['horario']
        request.session['cita_dia'] = dia
        request.session['cita_horario'] = horario
        return redirect('registro_dueno')  # Ahora sí existe esta URL

def conoce_mas(request):
    fechas = [(date.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    return render(request, 'bienvenida/conoce_mas.html', {'fechas': fechas})

def confirmacion_cita(request, cita_id):
    cita = Cita.objects.select_related('owner', 'mascota').get(id=cita_id)
    return render(request, 'bienvenida/confirmacion_cita.html', {'cita': cita})

