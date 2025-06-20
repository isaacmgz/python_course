from django import forms
from .models import Owner, Mascota, Cita

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = "__all__"
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
