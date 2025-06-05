from datetime import datetime
from pet import Pet

class Consultation:
    def __init__(self, date_str, reason, diagnosis, pet_name):
        self.date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        self.reason = reason
        self.diagnosis = diagnosis
        self.pet_name = pet_name

    def __str__(self):
        return f"📋 Consulta \n Nombre: {self.pet_name} \n Razón: {self.reason}\n Diagnostico {self.diagnosis} \n Fecha: {self.date}"