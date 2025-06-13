import csv
import json
import os
import unittest
from datetime import datetime

from clinic import Clinic
from consultation import Consultation
from owner import Owner
from pet import Pet


class TestOwnerPetConsultation(unittest.TestCase):
    """
    Pruebas básicas de creación y representación de objetos:
     - Owner: creación de atributos y __str__
     - Pet: creación de atributos y __str__
     - Consultation: conversión de cadena a datetime y __str__
    """

    def test_owner_creation_and_str(self):
        owner = Owner("Juan", "123456789", "Calle Falsa 123")
        self.assertEqual(owner.name, "Juan")
        self.assertEqual(owner.phone, "123456789")
        self.assertEqual(owner.address, "Calle Falsa 123")
        self.assertEqual(str(owner), "Juan")

    def test_pet_creation_and_str(self):
        owner = Owner("Ana", "987654321", "Calle 654")
        pet = Pet("Pepito", "Perro", "Labrador", 5, owner)
        self.assertEqual(pet.name, "Pepito")
        self.assertEqual(pet.species, "Perro")
        self.assertEqual(pet.race, "Labrador")
        self.assertEqual(pet.age, 5)
        self.assertIs(pet.owner, owner)

        texto = str(pet)
        # Verificar que en el __str__ de Pet aparezca el nombre del dueño
        self.assertIn("Nombre: Pepito", texto)
        self.assertIn("Dueño: Ana", texto)

    def test_consultation_creation_and_str(self):
        date_str = "2025-06-01 14:30"
        consultation = Consultation(date_str, "Vacuna", "Saludable", "Pepito")
        self.assertEqual(consultation.reason, "Vacuna")
        self.assertEqual(consultation.diagnosis, "Saludable")
        self.assertEqual(consultation.pet_name, "Pepito")
        # Se verifica que la fecha interna sea datetime
        self.assertIsInstance(consultation.date, datetime)
        self.assertEqual(consultation.date.strftime("%Y-%m-%d %H:%M"), date_str)

        texto = str(consultation)
        self.assertIn("Nombre: Pepito", texto)
        self.assertIn("Razón: Vacuna", texto)
        self.assertIn("Diagnostico Saludable", texto)


class TestValidationExceptions(unittest.TestCase):
    """
    Pruebas de la función validar_ascii_letras en Clinic:
     - Caso correcto (solo letras y espacios)
     - Caso que lanza ValueError por dígitos u otros caracteres inválidos
    """

    def test_validar_ascii_letras_correcto(self):
        clinic = Clinic()
        clinic.validar_ascii_letras(nombre="Maria", especie="Gato")

    def test_validar_ascii_letras_incorrecto(self):
        clinic = Clinic()
        with self.assertRaises(ValueError):
            # “M4ria” contiene un dígito → debe fallar
            clinic.validar_ascii_letras(nombre="M4ria", especie="Gato")


class TestSerialization(unittest.TestCase):
    """
    Pruebas de serialización y deserialización:
     - save_pets_and_owners()/load_pets_and_owners() con CSV
     - save_consultations()/load_consultations() con JSON
    """

    csv_file = "mascotas_dueños.csv"
    json_file = "consultas.json"

    def setUp(self):
        # Antes de cada prueba, eliminar cualquier archivo residual
        for f in (self.csv_file, self.json_file):
            try:
                os.remove(f)
            except OSError:
                pass

    def tearDown(self):
        # Tras cada prueba, limpiar los archivos generados
        for f in (self.csv_file, self.json_file):
            try:
                os.remove(f)
            except OSError:
                pass

    def test_save_and_load_pets_and_owners(self):
        clinic = Clinic()
        # Crear dueño y mascota manualmente (sin usar input)
        owner = clinic.add_owner("Luis", "555222333", "Calle Real 456")
        pet = Pet("Rex", "Perro", "Beagle", 3, owner)
        clinic.pets.append(pet)

        # Guardar en CSV
        clinic.save_pets_and_owners()
        self.assertTrue(os.path.exists(self.csv_file))

        # Leer el CSV y validar su contenido
        with open(self.csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        fila = rows[0]
        self.assertEqual(fila["nombre_mascota"], "Rex")
        self.assertEqual(fila["especie"], "Perro")
        self.assertEqual(fila["raza"], "Beagle")
        self.assertEqual(fila["edad"], "3")
        self.assertEqual(fila["nombre_dueño"], "Luis")
        self.assertEqual(fila["teléfono_dueño"], "555222333")
        self.assertEqual(fila["dirección_dueño"], "Calle Real 456")

        # Ahora instanciar una nueva Clinic y cargar desde CSV
        clinic2 = Clinic()
        clinic2.load_pets_and_owners()
        # Debe tener exactamente 1 mascota cargada
        self.assertEqual(len(clinic2.pets), 1)
        pet2 = clinic2.pets[0]
        self.assertEqual(pet2.name, "Rex")
        self.assertEqual(pet2.owner.name, "Luis")

    def test_save_and_load_consultations(self):
        clinic = Clinic()
        # Crear consulta manualmente (sin usar input)
        consultation = Consultation("2025-06-02 09:00", "Chequeo", "Bien", "Rex")
        clinic.consultations.append(consultation)

        # Guardar en JSON
        clinic.save_consultations()
        self.assertTrue(os.path.exists(self.json_file))

        # Leer el JSON y verificar contenido
        with open(self.json_file, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        entry = data[0]
        self.assertEqual(entry["date"], "2025-06-02 09:00")
        self.assertEqual(entry["reason"], "Chequeo")
        self.assertEqual(entry["diagnosis"], "Bien")
        self.assertEqual(entry["pet_name"], "Rex")

        # Cargar en nueva instancia y validar
        clinic2 = Clinic()
        clinic2.load_consultations()
        self.assertEqual(len(clinic2.consultations), 1)
        c2 = clinic2.consultations[0]
        self.assertEqual(c2.pet_name, "Rex")
        self.assertEqual(c2.reason, "Chequeo")


class TestLogging(unittest.TestCase):
    """
    Pruebas de logging:
     - Al crear un dueño, debe registrarse un mensaje INFO
     - Al validar caracteres inválidos, debe registrarse un ERROR
    """

    def test_logging_on_owner_creation(self):
        # Capturamos logs de nivel INFO para la creación de Owner
        with self.assertLogs(level="INFO") as cm:
            clinic = Clinic()
            clinic.add_owner("Pedro", "111222333", "Calle 1")
        logs = "\n".join(cm.output)
        self.assertIn("New owner registered: Pedro", logs)

    def test_logging_on_invalid_validation(self):
        # Capturamos logs de nivel ERROR al invocar validar_ascii_letras con valor inválido
        with self.assertLogs(level="ERROR") as cm:
            clinic = Clinic()
            try:
                clinic.validar_ascii_letras(nombre="Inv4lido")
            except ValueError:
                pass
        logs = "\n".join(cm.output)
        self.assertIn("Invalid characters in field 'nombre'", logs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
"""
# Escribir el archivo de pruebas en el directorio actual
with open('test_veterinaria.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Se creó 'test_veterinaria.py' con las pruebas unitarias.")
"""
