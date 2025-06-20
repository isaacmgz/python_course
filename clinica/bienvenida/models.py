from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
class Mascota(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='mascotas')

class Cita(models.Model):
    date = models.DateField()
    time = models.TimeField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='citas')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    description = models.TextField()