from django import forms
from .models import Owner, Mascota

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = "__all__"
