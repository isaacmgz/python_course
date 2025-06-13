"""
Módulo de Gestión de Consultas para la Clínica Veterinaria

Este módulo implementa la clase Consultation que representa las consultas médicas
realizadas a las mascotas en el sistema de la clínica veterinaria. Cada consulta
tiene la siguiente información:

- ID: Identificador único en la base de datos
- Fecha: Fecha y hora de la consulta
- Motivo: Razón de la visita
- Diagnóstico: Diagnóstico realizado por el veterinario
- Nombre de la mascota: Nombre de la mascota atendida

La clase proporciona métodos para:
- Inicializar una nueva consulta
- Obtener una representación en cadena de la consulta
"""

from datetime import datetime
from pet import Pet

class Consultation:
    def __init__(self, date, reason, diagnosis, pet_name):
        """
        Inicializa una nueva consulta con sus datos básicos.
        
        Args:
            date (str): Fecha y hora en formato "YYYY-MM-DD HH:mm"
            reason (str): Motivo de la consulta
            diagnosis (str): Diagnóstico realizado
            pet_name (str): Nombre de la mascota atendida
        """
        self.id = None  # Se establecerá cuando se guarde en la base de datos
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        self.reason = reason
        self.diagnosis = diagnosis
        self.pet_name = pet_name

    def __str__(self):
        """
        Retorna una representación en cadena de la consulta.
        
        Returns:
            str: Cadena con el formato "Mascota: {nombre}, Fecha: {fecha}, Motivo: {motivo}, Diagnóstico: {diagnóstico}"
        """
        return f"Mascota: {self.pet_name}, Fecha: {self.date.strftime('%Y-%m-%d %H:%M')}, Motivo: {self.reason}, Diagnóstico: {self.diagnosis}"