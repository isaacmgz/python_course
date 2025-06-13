"""
Módulo de Base de Datos para la Clínica Veterinaria "Amigos Peludos"

Este módulo implementa la persistencia de datos utilizando SQLite, permitiendo un almacenamiento
robusto y eficiente de la información de la clínica veterinaria.

Estructura de la Base de Datos:
- Tabla 'owners': Almacena información de los dueños de las mascotas
  • id: Identificador único autoincremental
  • name: Nombre del dueño
  • phone: Teléfono de contacto
  • address: Dirección del dueño

- Tabla 'pets': Almacena información de las mascotas
  • id: Identificador único autoincremental
  • name: Nombre de la mascota
  • species: Especie de la mascota
  • breed: Raza de la mascota
  • age: Edad de la mascota
  • owner_id: Referencia al dueño (clave foránea)

- Tabla 'consultations': Almacena información de las consultas
  • id: Identificador único autoincremental
  • date: Fecha y hora de la consulta
  • reason: Motivo de la consulta
  • diagnosis: Diagnóstico realizado
  • pet_id: Referencia a la mascota (clave foránea)

Características implementadas:
- Creación automática de tablas si no existen
- Gestión de conexiones a la base de datos
- Operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar)
- Manejo de transacciones y errores
- Integridad referencial mediante claves foráneas
"""

import sqlite3
import logging
from datetime import datetime

class Database:
    def __init__(self, db_name="clinica_veterinaria.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_name (str): Nombre del archivo de base de datos SQLite
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()

    def connect(self):
        """
        Establece la conexión con la base de datos SQLite.
        Crea el archivo de base de datos si no existe.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Conectado a la base de datos: {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn:
            self.conn.close()
            logging.info("Conexión a la base de datos cerrada")

    def initialize_database(self):
        """
        Inicializa la estructura de la base de datos.
        Crea las tablas necesarias si no existen.
        """
        try:
            self.connect()
            
            # Crear tabla de dueños
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS owners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT NOT NULL
                )
            ''')

            # Crear tabla de mascotas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    species TEXT NOT NULL,
                    breed TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    owner_id INTEGER NOT NULL,
                    FOREIGN KEY (owner_id) REFERENCES owners (id)
                )
            ''')

            # Crear tabla de consultas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS consultations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    diagnosis TEXT NOT NULL,
                    pet_id INTEGER NOT NULL,
                    FOREIGN KEY (pet_id) REFERENCES pets (id)
                )
            ''')

            self.conn.commit()
            logging.info("Tablas de la base de datos inicializadas correctamente")
        except sqlite3.Error as e:
            logging.error(f"Error al inicializar la base de datos: {e}")
            raise
        finally:
            self.close()

    def add_owner(self, name, phone, address):
        """
        Añade un nuevo dueño a la base de datos.
        
        Args:
            name (str): Nombre del dueño
            phone (str): Teléfono del dueño
            address (str): Dirección del dueño
            
        Returns:
            int: ID del dueño creado
        """
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO owners (name, phone, address) VALUES (?, ?, ?)",
                (name, phone, address)
            )
            self.conn.commit()
            owner_id = self.cursor.lastrowid
            logging.info(f"Nuevo dueño añadido: {name} con ID: {owner_id}")
            return owner_id
        except sqlite3.Error as e:
            logging.error(f"Error al añadir dueño: {e}")
            raise
        finally:
            self.close()

    def add_pet(self, name, species, breed, age, owner_id):
        """
        Añade una nueva mascota a la base de datos.
        
        Args:
            name (str): Nombre de la mascota
            species (str): Especie de la mascota
            breed (str): Raza de la mascota
            age (int): Edad de la mascota
            owner_id (int): ID del dueño
            
        Returns:
            int: ID de la mascota creada
        """
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO pets (name, species, breed, age, owner_id) VALUES (?, ?, ?, ?, ?)",
                (name, species, breed, age, owner_id)
            )
            self.conn.commit()
            pet_id = self.cursor.lastrowid
            logging.info(f"Nueva mascota añadida: {name} con ID: {pet_id}")
            return pet_id
        except sqlite3.Error as e:
            logging.error(f"Error al añadir mascota: {e}")
            raise
        finally:
            self.close()

    def add_consultation(self, date, reason, diagnosis, pet_id):
        """
        Añade una nueva consulta a la base de datos.
        
        Args:
            date (str): Fecha y hora de la consulta
            reason (str): Motivo de la consulta
            diagnosis (str): Diagnóstico realizado
            pet_id (int): ID de la mascota
            
        Returns:
            int: ID de la consulta creada
        """
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO consultations (date, reason, diagnosis, pet_id) VALUES (?, ?, ?, ?)",
                (date, reason, diagnosis, pet_id)
            )
            self.conn.commit()
            consultation_id = self.cursor.lastrowid
            logging.info(f"Nueva consulta añadida para mascota ID: {pet_id}")
            return consultation_id
        except sqlite3.Error as e:
            logging.error(f"Error al añadir consulta: {e}")
            raise
        finally:
            self.close()

    def get_owner_by_name(self, name):
        """
        Obtiene los detalles de un dueño por su nombre.
        
        Args:
            name (str): Nombre del dueño
            
        Returns:
            tuple: Datos del dueño o None si no se encuentra
        """
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM owners WHERE name = ?", (name,))
            owner = self.cursor.fetchone()
            return owner
        except sqlite3.Error as e:
            logging.error(f"Error al obtener dueño: {e}")
            raise
        finally:
            self.close()

    def get_pet_by_name(self, name):
        """
        Obtiene los detalles de una mascota por su nombre.
        
        Args:
            name (str): Nombre de la mascota
            
        Returns:
            tuple: Datos de la mascota o None si no se encuentra
        """
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM pets WHERE name = ?", (name,))
            pet = self.cursor.fetchone()
            return pet
        except sqlite3.Error as e:
            logging.error(f"Error al obtener mascota: {e}")
            raise
        finally:
            self.close()

    def get_consultations_by_pet_id(self, pet_id):
        """
        Obtiene todas las consultas de una mascota específica.
        
        Args:
            pet_id (int): ID de la mascota
            
        Returns:
            list: Lista de consultas de la mascota
        """
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM consultations WHERE pet_id = ?", (pet_id,))
            consultations = self.cursor.fetchall()
            return consultations
        except sqlite3.Error as e:
            logging.error(f"Error al obtener consultas: {e}")
            raise
        finally:
            self.close()

    def get_all_pets(self):
        """
        Obtiene todas las mascotas con la información de sus dueños.
        
        Returns:
            list: Lista de mascotas con información de dueños
        """
        try:
            self.connect()
            self.cursor.execute('''
                SELECT p.*, o.name as owner_name, o.phone, o.address 
                FROM pets p 
                JOIN owners o ON p.owner_id = o.id
            ''')
            pets = self.cursor.fetchall()
            return pets
        except sqlite3.Error as e:
            logging.error(f"Error al obtener todas las mascotas: {e}")
            raise
        finally:
            self.close()

    def update_owner(self, owner_id, name, phone, address):
        """
        Actualiza la información de un dueño.
        
        Args:
            owner_id (int): ID del dueño
            name (str): Nuevo nombre
            phone (str): Nuevo teléfono
            address (str): Nueva dirección
        """
        try:
            self.connect()
            self.cursor.execute(
                "UPDATE owners SET name = ?, phone = ?, address = ? WHERE id = ?",
                (name, phone, address, owner_id)
            )
            self.conn.commit()
            logging.info(f"Dueño actualizado con ID: {owner_id}")
        except sqlite3.Error as e:
            logging.error(f"Error al actualizar dueño: {e}")
            raise
        finally:
            self.close()

    def update_pet(self, pet_id, name, species, breed, age, owner_id):
        """
        Actualiza la información de una mascota.
        
        Args:
            pet_id (int): ID de la mascota
            name (str): Nuevo nombre
            species (str): Nueva especie
            breed (str): Nueva raza
            age (int): Nueva edad
            owner_id (int): Nuevo ID del dueño
        """
        try:
            self.connect()
            self.cursor.execute(
                "UPDATE pets SET name = ?, species = ?, breed = ?, age = ?, owner_id = ? WHERE id = ?",
                (name, species, breed, age, owner_id, pet_id)
            )
            self.conn.commit()
            logging.info(f"Mascota actualizada con ID: {pet_id}")
        except sqlite3.Error as e:
            logging.error(f"Error al actualizar mascota: {e}")
            raise
        finally:
            self.close()

    def delete_owner(self, owner_id):
        """
        Elimina un dueño y sus mascotas asociadas.
        
        Args:
            owner_id (int): ID del dueño a eliminar
        """
        try:
            self.connect()
            # Primero eliminar mascotas asociadas
            self.cursor.execute("DELETE FROM pets WHERE owner_id = ?", (owner_id,))
            # Luego eliminar el dueño
            self.cursor.execute("DELETE FROM owners WHERE id = ?", (owner_id,))
            self.conn.commit()
            logging.info(f"Dueño eliminado con ID: {owner_id}")
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar dueño: {e}")
            raise
        finally:
            self.close()

    def delete_pet(self, pet_id):
        """
        Elimina una mascota y sus consultas asociadas.
        
        Args:
            pet_id (int): ID de la mascota a eliminar
        """
        try:
            self.connect()
            # Primero eliminar consultas asociadas
            self.cursor.execute("DELETE FROM consultations WHERE pet_id = ?", (pet_id,))
            # Luego eliminar la mascota
            self.cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
            self.conn.commit()
            logging.info(f"Mascota eliminada con ID: {pet_id}")
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar mascota: {e}")
            raise
        finally:
            self.close() 