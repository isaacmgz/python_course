from owner import Owner
from pet import Pet
from consultation import Consultation
import logging
import re
from datetime import datetime
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('veterinary_clinic.log'),
        logging.StreamHandler()
    ]
)

class Clinic:

    def __init__(self):
        self.owners = []
        self.pets = []
        self.consultations = []
        logging.info("Clinic system initialized")

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
                name=name,
                species=species,
                breed=breed,
                owner=owner_name
            )
        except ValueError as e:
            logging.error(f"Validation error in add_pet: {str(e)}")
            print ("Error: ", e)
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
        logging.info(f"New pet registered: {name} ({species}, {breed}) for owner {owner.name}")
        return p

    def add_consultation(self):
        pet_name = input("Pet name: ")
        for p in self.pets:
            if p.name == pet_name:
                pet = p
                break
            else:
                logging.error(f"Pet not found: {pet_name}")
                self.PetNotFoundError(pet_name)
        try:
            date_str = input("Date (YYYY-MM-DD HH:mm): ")
            date_str = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            logging.error(f"Invalid date format provided: {date_str}")
            print("❌ Invalid date. Must be in the format YYYYY-MM-DD HH:mm ❌")
            return
        reason = input("Reason: ")
        diagnosis = input("Diagnosis: ")
        try:
            self.validar_ascii_letras(
                reason=reason,
                diagnosis=diagnosis
            )
        except ValueError as e:
            logging.error(f"Validation error in add_consultation: {str(e)}")
            print ("Error: ", e)
            return
        c = Consultation(date_str, reason, diagnosis, pet_name)
        self.consultations.append(c)
        logging.info(f"New consultation registered for pet {pet_name} on {date_str}")
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

    def validar_ascii_letras(self,**campos):
        patron = re.compile(r'^[A-Za-z ]+$')
        for campo, valor in campos.items():
            if not patron.fullmatch(valor):
                logging.error(f"Invalid characters in field '{campo}': {valor}")
                raise ValueError(f" ❌ The field '{campo}'  must contain only letters and spaces. ❌")

    class OwnerNotFoundError(Exception):
        def __init__(self, owner):
            super().__init__(f" Owner: '{owner}' not found.")

    class PetNotFoundError(Exception):
        def __init__(self,pet_name):
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