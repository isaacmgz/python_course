"""
Módulo de Gestión de Mascotas para la Clínica Veterinaria

Este módulo implementa la clase Pet que representa a las mascotas en el sistema
de la clínica veterinaria. Cada mascota tiene la siguiente información:

- ID: Identificador único en la base de datos
- Nombre: Nombre de la mascota
- Especie: Tipo de animal (perro, gato, etc.)
- Raza: Raza específica de la mascota
- Edad: Edad en años
- Dueño: Referencia al objeto Owner que es dueño de la mascota

La clase proporciona métodos para:
- Inicializar una nueva mascota
- Obtener una representación en cadena de la mascota
"""

from owner import Owner


class Pet:
    def __init__(self, name, species, breed, age, owner):
        """
        Inicializa una nueva mascota con sus datos básicos.
        
        Args:
            name (str): Nombre de la mascota
            species (str): Especie del animal
            breed (str): Raza de la mascota
            age (int): Edad en años
            owner (Owner): Objeto Owner que es dueño de la mascota
        """
        self.id = None  # Se establecerá cuando se guarde en la base de datos
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner = owner

    def __str__(self):
        """
        Retorna una representación en cadena de la mascota.
        
        Returns:
            str: Cadena con el formato "Nombre: {nombre}, Especie: {especie}, Raza: {raza}, Edad: {edad}, Dueño: {nombre_dueño}"
        """
        return f"Nombre: {self.name}, Especie: {self.species}, Raza: {self.breed}, Edad: {self.age}, Dueño: {self.owner.name}"
