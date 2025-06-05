import csv
import json
import logging
import os
import re
from datetime import datetime

from consultation import Consultation
from owner import Owner
from pet import Pet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("veterinary_clinic.log"), logging.StreamHandler()],
)


class Clinic:
    def __init__(self):
        self.owners = []
        self.pets = []
        self.consultations = []
        logging.info("Clinic system initialized")
        self.load_pets_and_owners()
        self.load_consultations()

    def add_owner(self, name, phone, address):
        o = Owner(name, phone, address)
        self.owners.append(o)
        logging.info(f"New owner registered: {name}")
        return o

    def add_pet(self):
        try:
            name = input("Pet name: ")
            species = input("Species: ")
            breed = input("Breed: ")
            owner_name = input("Owner name: ")
            self.validar_ascii_letras(
                name=name, species=species, breed=breed, owner=owner_name
            )
        except ValueError as e:
            logging.error(f"Validation error in add_pet: {str(e)}")
            print("Error: ", e)
            return
        age_input = input("Age: ")
        try:
            age = int(age_input)
        except ValueError:
            logging.error(f"Invalid age format: {age_input}")
            print("Age must contain numbers")
            return
        if age < 0:
            logging.error(f"Negative age provided: {age}")
            print("Age must be positive")
            return

        owner = None
        for o in self.owners:
            if o.name == owner_name:
                owner = o
                logging.info(f"Found existing owner: {owner_name}")
                break

        if owner is None:
            logging.info(f"Creating new owner: {owner_name}")
            phone = input("Owner phone: ")
            address = input("Owner address: ")
            owner = self.add_owner(owner_name, phone, address)

        p = Pet(name, species, breed, age, owner)
        self.pets.append(p)
        logging.info(
            f"New pet registered: {name} ({species}, {breed}) for owner {owner.name}"
        )
        return p

    def add_consultation(self):
        date_input = input("Date (YYYY-MM-DD HH:mm)")
        pet_name = input("Pet name: ")
        for p in self.pets:
            if p.name == pet_name:
                pet = p
                break
            else:
                logging.error(f"Pet not found: {pet_name}")
                self.PetNotFoundError(pet_name)
        try:
            _ = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            logging.error(f"Invalid date format provided: {date_input}")
            print("❌ Invalid date. Must be in the format YYYY-MM-DD HH:mm ❌")
            return

        reason = input("Reason: ")
        diagnosis = input("Diagnosis: ")
        try:
            self.validar_ascii_letras(reason=reason, diagnosis=diagnosis)
        except ValueError as e:
            logging.error(f"Validation error in add_consultation: {str(e)}")
            print("Error: ", e)
            return

        c = Consultation(date_input, reason, diagnosis, pet_name)
        self.consultations.append(c)
        logging.info(f"New consultation registered for pet {pet_name} on {date_input}")
        return c

    def list_pets(self):
        if not self.pets:
            logging.warning("Attempted to list pets but none are registered")
            self.NoPetsRegisteredError()
            return
        pets = []
        for p in self.pets:
            pets.append(p)
        for p in pets:
            print(p)
        logging.info(f"Listed {len(pets)} pets")

    def search_consultation(self):
        if not self.consultations:
            logging.warning("Attempted to search consultations but none are registered")
            self.NoConsultationsRegisteredError()
        pet_name = input("Pet name: ")
        found = False
        consultations = []
        for c in self.consultations:
            if c.pet_name == pet_name:
                consultations.append(c)
                found = True
            for c in consultations:
                print(c)
        if not found:
            logging.warning(f"No consultations found for pet: {pet_name}")
            self.NoConsultationPet()
        else:
            logging.info(f"Found {len(consultations)} consultations for pet {pet_name}")

    def validar_ascii_letras(self, **campos):
        patron = re.compile(r"^[A-Za-z ]+$")
        for campo, valor in campos.items():
            if not patron.fullmatch(valor):
                logging.error(f"Invalid characters in field '{campo}': {valor}")
                raise ValueError(
                    f" ❌ The field '{campo}'  must contain only letters and spaces. ❌"
                )

    def save_pets_and_owners(self):
        try:
            with open(
                "mascotas_dueños.csv", mode="w", newline="", encoding="utf-8"
            ) as file:
                fieldnames = [
                    "nombre_mascota",
                    "especie",
                    "raza",
                    "edad",
                    "nombre_dueño",
                    "teléfono_dueño",
                    "dirección_dueño",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for pet in self.pets:
                    owner = pet.owner
                    writer.writerow(
                        {
                            "nombre_mascota": pet.name,
                            "especie": pet.species,
                            "raza": pet.race,
                            "edad": pet.age,
                            "nombre_dueño": owner.name,
                            "teléfono_dueño": owner.phone,
                            "dirección_dueño": owner.address,
                        }
                    )
                logging.info(f"Guardadas {len(self.pets)} mascotas y dueños en CSV")
        except Exception as e:
            logging.error(f"Error al guardar mascotas y dueños: {e}")

    def load_pets_and_owners(self):
        if not os.path.exists("mascotas_dueños.csv"):
            logging.info("No existe archivo mascotas_dueños.csv, nada para cargar")
            return
        try:
            with open(
                "mascotas_dueños.csv", mode="r", newline="", encoding="utf-8"
            ) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Validar que campos existan y tengan el formato correcto
                    try:
                        name = row["nombre_mascota"]
                        species = row["especie"]
                        breed = row["raza"]
                        age = int(row["edad"])
                        owner_name = row["nombre_dueño"]
                        phone = row["teléfono_dueño"]
                        address = row["dirección_dueño"]
                    except (KeyError, ValueError) as e:
                        logging.error(f"Error al leer fila CSV: {row} - {e}")
                        continue

                    # Crear o buscar dueño
                    owner = None
                    for o in self.owners:
                        if o.name == owner_name:
                            owner = o
                            break
                    if owner is None:
                        owner = Owner(owner_name, phone, address)
                        self.owners.append(owner)
                        logging.info(f"Dueño cargado desde CSV: {owner_name}")

                    # Crear mascota
                    pet = Pet(name, species, breed, age, owner)
                    self.pets.append(pet)
                    logging.info(f"Mascota cargada desde CSV: {name}")
        except Exception as e:
            logging.error(f"Fallo cargando mascotas y dueños: {e}")

    def load_consultations(self):
        if not os.path.exists("consultas.json"):
            logging.info("No existe archivo consultas.json, nada para cargar")
            return

        try:
            with open("consultas.json", mode="r", encoding="utf-8") as file:
                data = json.load(file)
                for entry in data:
                    try:
                        date_str = entry["date"]
                        reason = entry["reason"]
                        diagnosis = entry["diagnosis"]
                        pet_name = entry["pet_name"]
                    except KeyError as e:
                        logging.error(
                            f"Campo faltante en JSON de consulta: {entry} - {e}"
                        )
                        continue

                    # Validar formato fecha
                    try:
                        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    except ValueError:
                        logging.error(f"Formato de fecha inválido en JSON: {date_str}")
                        continue

                    c = Consultation(date_str, reason, diagnosis, pet_name)
                    self.consultations.append(c)
                logging.info(f"{len(self.consultations)} consultas cargadas desde JSON")
        except Exception as e:
            logging.error(f"Fallo cargando consultas JSON: {e}")

    def save_consultations(self):
        try:
            data = []
            for c in self.consultations:
                data.append(
                    {
                        "date": c.date.strftime("%Y-%m-%d %H:%M"),
                        "reason": c.reason,
                        "diagnosis": c.diagnosis,
                        "pet_name": c.pet_name,
                    }
                )

            with open("consultas.json", mode="w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info(f"Guardadas {len(self.consultations)} consultas en JSON")
        except Exception as e:
            logging.error(f"Error al guardar consultas: {e}")

    class OwnerNotFoundError(Exception):
        def __init__(self, owner):
            super().__init__(f" Owner: '{owner}' not found.")

    class PetNotFoundError(Exception):
        def __init__(self, pet_name):
            super().__init__(f" Pet name:  '{pet_name}' not found.")

    class NoPetsRegisteredError(Exception):
        def __init__(self):
            super().__init__(" No pets registered ")

    class NoConsultationsRegisteredError(Exception):
        def __init__(self):
            super().__init__(" There are no registered consultations ")

    class NoConsultationPet(Exception):
        def __init__(self):
            super().__init__(" There are no registered consultations for this pet")
