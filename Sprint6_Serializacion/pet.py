from owner import Owner


class Pet:
    def __init__(self, name, breed, race, age, owner: Owner):
        self.name = name
        self.species = breed
        self.race = race
        self.age = age
        self.owner = owner

    def __str__(self):
        return (
            f"🐾 Mascota\n"
            f" Nombre: {self.name} \n"
            f" Especie: {self.species}\n"
            f" Edad: {self.age} años \n"
            f" Dueño: {self.owner.name}"
        )
