"""
Módulo Principal de la Clínica Veterinaria "Amigos Peludos"

Este módulo implementa la lógica principal del sistema de gestión de la clínica veterinaria,
integrando la persistencia de datos con SQLite y manteniendo la compatibilidad con el
sistema anterior de archivos CSV y JSON.

Características implementadas:
- Gestión completa de mascotas, dueños y consultas
- Validación de datos de entrada
- Manejo de excepciones y logging
- Integración con base de datos SQLite
- Mantenimiento de datos en memoria para mejor rendimiento

Estructura de clases:
- Clinic: Clase principal que gestiona todas las operaciones
  • Manejo de mascotas y dueños
  • Gestión de consultas
  • Validación de datos
  • Integración con base de datos
"""

import csv
import json
import logging
import os
import re
from datetime import datetime

from consultation import Consultation
from owner import Owner
from pet import Pet
from database import Database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("veterinary_clinic.log"), logging.StreamHandler()],
)


class Clinic:
    def __init__(self):
        """
        Inicializa el sistema de la clínica.
        Crea las estructuras de datos necesarias y carga la información desde la base de datos.
        """
        self.owners = []
        self.pets = []
        self.consultations = []
        self.db = Database()
        logging.info("Sistema de clínica inicializado")
        self.load_pets_and_owners()
        self.load_consultations()

    def add_owner(self, name, phone, address):
        """
        Añade un nuevo dueño al sistema.
        
        Args:
            name (str): Nombre del dueño
            phone (str): Teléfono del dueño
            address (str): Dirección del dueño
            
        Returns:
            Owner: Objeto dueño creado
        """
        try:
            owner_id = self.db.add_owner(name, phone, address)
            o = Owner(name, phone, address)
            o.id = owner_id
            self.owners.append(o)
            logging.info(f"Nuevo dueño registrado: {name}")
            return o
        except Exception as e:
            logging.error(f"Error al añadir dueño a la base de datos: {e}")
            raise

    def add_pet(self):
        """
        Añade una nueva mascota al sistema.
        Solicita la información necesaria al usuario y valida los datos.
        
        Returns:
            Pet: Objeto mascota creado o None si hay error
        """
        try:
            name = input("Nombre de la mascota: ")
            species = input("Especie: ")
            breed = input("Raza: ")
            owner_name = input("Nombre del dueño: ")
            self.validar_ascii_letras(
                name=name, species=species, breed=breed, owner=owner_name
            )
        except ValueError as e:
            logging.error(f"Error de validación en add_pet: {str(e)}")
            print("Error: ", e)
            return

        age_input = input("Edad: ")
        try:
            age = int(age_input)
        except ValueError:
            logging.error(f"Formato de edad inválido: {age_input}")
            print("La edad debe contener números")
            return
        if age < 0:
            logging.error(f"Edad negativa proporcionada: {age}")
            print("La edad debe ser positiva")
            return

        owner = None
        for o in self.owners:
            if o.name == owner_name:
                owner = o
                logging.info(f"Dueño existente encontrado: {owner_name}")
                break

        if owner is None:
            logging.info(f"Creando nuevo dueño: {owner_name}")
            phone = input("Teléfono del dueño: ")
            address = input("Dirección del dueño: ")
            owner = self.add_owner(owner_name, phone, address)

        try:
            pet_id = self.db.add_pet(name, species, breed, age, owner.id)
            p = Pet(name, species, breed, age, owner)
            p.id = pet_id
            self.pets.append(p)
            logging.info(
                f"Nueva mascota registrada: {name} ({species}, {breed}) para dueño {owner.name}"
            )
            return p
        except Exception as e:
            logging.error(f"Error al añadir mascota a la base de datos: {e}")
            raise

    def add_consultation(self):
        """
        Añade una nueva consulta al sistema.
        Solicita la información necesaria al usuario y valida los datos.
        
        Returns:
            Consultation: Objeto consulta creado o None si hay error
        """
        date_input = input("Fecha (YYYY-MM-DD HH:mm): ")
        pet_name = input("Nombre de la mascota: ")
        
        pet = None
        for p in self.pets:
            if p.name == pet_name:
                pet = p
                break
        
        if pet is None:
            logging.error(f"Mascota no encontrada: {pet_name}")
            self.PetNotFoundError(pet_name)
            return

        try:
            _ = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        except ValueError:
            logging.error(f"Formato de fecha inválido: {date_input}")
            print("❌ Fecha inválida. Debe estar en formato YYYY-MM-DD HH:mm ❌")
            return

        reason = input("Motivo: ")
        diagnosis = input("Diagnóstico: ")
        try:
            self.validar_ascii_letras(reason=reason, diagnosis=diagnosis)
        except ValueError as e:
            logging.error(f"Error de validación en add_consultation: {str(e)}")
            print("Error: ", e)
            return

        try:
            consultation_id = self.db.add_consultation(date_input, reason, diagnosis, pet.id)
            c = Consultation(date_input, reason, diagnosis, pet_name)
            c.id = consultation_id
            self.consultations.append(c)
            logging.info(f"Nueva consulta registrada para mascota {pet_name} en {date_input}")
            return c
        except Exception as e:
            logging.error(f"Error al añadir consulta a la base de datos: {e}")
            raise

    def list_pets(self):
        """
        Lista todas las mascotas registradas en el sistema.
        Muestra la información detallada de cada mascota y su dueño.
        """
        try:
            pets = self.db.get_all_pets()
            if not pets:
                logging.warning("No se encontraron mascotas en la base de datos")
                self.NoPetsRegisteredError()
                return
            
            for pet in pets:
                print(f"ID: {pet[0]}")
                print(f"Nombre: {pet[1]}")
                print(f"Especie: {pet[2]}")
                print(f"Raza: {pet[3]}")
                print(f"Edad: {pet[4]}")
                print(f"Dueño: {pet[6]}")
                print(f"Teléfono del dueño: {pet[7]}")
                print(f"Dirección del dueño: {pet[8]}")
                print("-" * 50)
            
            logging.info(f"Listadas {len(pets)} mascotas de la base de datos")
        except Exception as e:
            logging.error(f"Error al listar mascotas de la base de datos: {e}")
            raise

    def search_consultation(self):
        """
        Busca y muestra las consultas de una mascota específica.
        Solicita el nombre de la mascota y muestra todas sus consultas.
        """
        pet_name = input("Nombre de la mascota: ")
        
        # Buscar mascota en la lista local primero
        pet = None
        for p in self.pets:
            if p.name == pet_name:
                pet = p
                break
        
        if pet is None:
            logging.warning(f"Mascota no encontrada: {pet_name}")
            self.PetNotFoundError(pet_name)
            return

        try:
            consultations = self.db.get_consultations_by_pet_id(pet.id)
            if not consultations:
                logging.warning(f"No se encontraron consultas para la mascota: {pet_name}")
                self.NoConsultationPet()
                return

            for consultation in consultations:
                print(f"Fecha: {consultation[1]}")
                print(f"Motivo: {consultation[2]}")
                print(f"Diagnóstico: {consultation[3]}")
                print("-" * 50)

            logging.info(f"Encontradas {len(consultations)} consultas para mascota {pet_name}")
        except Exception as e:
            logging.error(f"Error al buscar consultas en la base de datos: {e}")
            raise

    def validar_ascii_letras(self, **campos):
        """
        Valida que los campos contengan solo letras y espacios.
        
        Args:
            **campos: Diccionario de campos a validar
            
        Raises:
            ValueError: Si algún campo contiene caracteres no permitidos
        """
        patron = re.compile(r"^[A-Za-z ]+$")
        for campo, valor in campos.items():
            if not patron.fullmatch(valor):
                logging.error(f"Caracteres inválidos en campo '{campo}': {valor}")
                raise ValueError(
                    f" ❌ El campo '{campo}' debe contener solo letras y espacios. ❌"
                )

    def save_pets_and_owners(self):
        """
        Método mantenido por compatibilidad con versiones anteriores.
        Los datos ya están guardados en la base de datos.
        """
        logging.info("Guardando mascotas y dueños en la base de datos")
        # Los datos ya están en la base de datos, solo registramos la acción
        pass

    def load_pets_and_owners(self):
        """
        Carga mascotas y dueños desde la base de datos.
        Mantiene los objetos en memoria para mejor rendimiento.
        """
        try:
            pets = self.db.get_all_pets()
            for pet in pets:
                # Crear dueño si no existe
                owner = None
                for o in self.owners:
                    if o.name == pet[6]:  # nombre_dueño del join
                        owner = o
                        break
                
                if owner is None:
                    owner = Owner(pet[6], pet[7], pet[8])  # nombre, teléfono, dirección
                    owner.id = pet[5]  # owner_id
                    self.owners.append(owner)

                # Crear mascota
                p = Pet(pet[1], pet[2], pet[3], pet[4], owner)  # nombre, especie, raza, edad, dueño
                p.id = pet[0]  # pet_id
                self.pets.append(p)

            logging.info(f"Cargadas {len(self.pets)} mascotas y {len(self.owners)} dueños de la base de datos")
        except Exception as e:
            logging.error(f"Error al cargar mascotas y dueños de la base de datos: {e}")
            raise

    def load_consultations(self):
        """
        Carga las consultas desde la base de datos.
        Mantiene los objetos en memoria para mejor rendimiento.
        """
        try:
            for pet in self.pets:
                consultations = self.db.get_consultations_by_pet_id(pet.id)
                for consultation in consultations:
                    c = Consultation(consultation[1], consultation[2], consultation[3], pet.name)
                    c.id = consultation[0]
                    self.consultations.append(c)
            
            logging.info(f"Cargadas {len(self.consultations)} consultas de la base de datos")
        except Exception as e:
            logging.error(f"Error al cargar consultas de la base de datos: {e}")
            raise

    class OwnerNotFoundError(Exception):
        """Excepción lanzada cuando no se encuentra un dueño"""
        def __init__(self, owner):
            self.message = f"❌ Dueño {owner} no encontrado ❌"
            super().__init__(self.message)

    class PetNotFoundError(Exception):
        """Excepción lanzada cuando no se encuentra una mascota"""
        def __init__(self, pet_name):
            self.message = f"❌ Mascota {pet_name} no encontrada ❌"
            super().__init__(self.message)

    class NoPetsRegisteredError(Exception):
        """Excepción lanzada cuando no hay mascotas registradas"""
        def __init__(self):
            self.message = "❌ No hay mascotas registradas ❌"
            super().__init__(self.message)

    class NoConsultationsRegisteredError(Exception):
        """Excepción lanzada cuando no hay consultas registradas"""
        def __init__(self):
            self.message = "❌ No hay consultas registradas ❌"
            super().__init__(self.message)

    class NoConsultationPet(Exception):
        """Excepción lanzada cuando no hay consultas para una mascota específica"""
        def __init__(self):
            self.message = "❌ No se encontraron consultas para esta mascota ❌"
            super().__init__(self.message)
