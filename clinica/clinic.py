from owner import Owner
from pet import Pet
from consultation import Consultation

class Clinic:

    def __init__(self):
        self.owners = []
        self.pets = []
        self.consultations = []

    def add_owner(self, name, phone, address):
        o = Owner(name, phone, address)
        self.owners.append(o)
        return o

    def add_pet(self):
        name = input("Pet name: ")
        species = input("Species: ")
        breed = input("Breed: ")
        age = int(input("Age: "))
        owner = input("Owner name: ")
        for o in self.owners:
            if o.name == owner:
                owner = o
                break
        if owner is None:
            print(f"Owner {owner} not found.")
            return None
        p = Pet(name, species, breed, age, owner)
        self.pets.append(p)
        return p

    def add_consultation(self):
        pet_name = input("Pet name: ")
        for p in self.pets:
            if p.name == pet_name:
                pet = p
                break
            else:
                print(f"pet {pet_name} not found.")
                return None
        date_str = input("Date (YYYY-MM-DD HH:mm): ")
        reason = input("Reason: ")
        diagnosis = input("Diagnosis: ")
        
        c = Consultation(date_str, reason, diagnosis, pet_name)
        self.consultations.append(c)
        return c 
    def list_pets(self):
        if not self.pets:
            print("No hay mascotas registradas")
            return
        pets = []
        for p in self.pets:
            pets.append(p)
        for p in pets:
            print(p)
    def search_consultation(self):
        if not self.consultations:
            print("No hay consultas registradas")
            return
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
            print("No hay consultas para esta mascota")
            