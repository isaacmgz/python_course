"""
Módulo de Gestión de Dueños para la Clínica Veterinaria

Este módulo implementa la clase Owner que representa a los dueños de las mascotas
en el sistema de la clínica veterinaria. Cada dueño tiene la siguiente información:

- ID: Identificador único en la base de datos
- Nombre: Nombre completo del dueño
- Teléfono: Número de contacto
- Dirección: Dirección física del dueño

La clase proporciona métodos para:
- Inicializar un nuevo dueño
- Obtener una representación en cadena del dueño
"""

class Owner:
    def __init__(self, name, phone, address):
        """
        Inicializa un nuevo dueño con sus datos básicos.
        
        Args:
            name (str): Nombre completo del dueño
            phone (str): Número de teléfono
            address (str): Dirección física
        """
        self.id = None  # Se establecerá cuando se guarde en la base de datos
        self.name = name
        self.phone = phone
        self.address = address

    def __str__(self):
        """
        Retorna una representación en cadena del dueño.
        
        Returns:
            str: Cadena con el formato "Nombre: {nombre}, Teléfono: {teléfono}, Dirección: {dirección}"
        """
        return f"Nombre: {self.name}, Teléfono: {self.phone}, Dirección: {self.address}"
