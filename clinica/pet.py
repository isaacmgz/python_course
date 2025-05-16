from owner import Owner

class Pet:
    def __init__(self, name, breed, race, age, owner: Owner):
        self.name = name
        self.species = breed
        self.race = race
        self.age = age
        self.owner = owner

    def __str__(self):
        return f"Nombre: {self.name} \n Especie: {self.species}\n Edad: {self.age} años \n Dueño: {self.owner}"