"""
Programa Principal de la Clínica Veterinaria "Amigos Peludos"

Este módulo implementa la interfaz de usuario en consola para el sistema de gestión
de la clínica veterinaria. Proporciona un menú interactivo que permite al usuario
realizar las siguientes operaciones:

1. Añadir mascota
2. Listar mascotas
3. Añadir consulta
4. Buscar consultas
5. Salir del sistema

El programa mantiene un registro de todas las operaciones en el archivo de log
'veterinary_clinic.log'.
"""

import logging
from clinic import Clinic


def main():
    """
    Función principal que ejecuta el programa.
    Inicializa el sistema y muestra el menú interactivo.
    """
    clinic = Clinic()
    while True:
        print("\n=== Sistema de Gestión de Clínica Veterinaria ===")
        print("1. Añadir Mascota")
        print("2. Listar Mascotas")
        print("3. Añadir Consulta")
        print("4. Buscar Consultas")
        print("5. Salir")
        
        choice = input("\nSeleccione una opción (1-5): ")
        
        if choice == "1":
            clinic.add_pet()
        elif choice == "2":
            clinic.list_pets()
        elif choice == "3":
            clinic.add_consultation()
        elif choice == "4":
            clinic.search_consultation()
        elif choice == "5":
            print("¡Gracias por usar el Sistema de Gestión de Clínica Veterinaria!")
            break
        else:
            print("Opción inválida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    logging.info("Iniciando Sistema de Gestión de Clínica Veterinaria")
    main()
    logging.info("Sistema de Gestión de Clínica Veterinaria finalizado")
