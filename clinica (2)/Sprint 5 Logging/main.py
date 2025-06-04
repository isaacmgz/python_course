from clinic import Clinic
import logging

def menu():
    clinic = Clinic()
    while True:
        print("🐾 MENÚ PRINCIPAL - VETERINARIA 🐾 \n"
              "1. Register pet \n"
              "2. Register consultation \n"
              "3. List pets \n"
              "4. Ver historial de consultas de una mascota específica. \n"
              "5. Exit")
        try:
            option = int(input("Chose one option: "))
            logging.info(f"User selected menu option: {option}")
        except ValueError:
            logging.error("Invalid menu option format - non-integer input")
            print("Invalid Format, type an integer")
            return
        match option:
            case 1:
                logging.info("Starting pet registration process")
                clinic.add_pet()
            case 2:
                logging.info("Starting consultation registration process")
                clinic.add_consultation()
            case 3:
                logging.info("Starting pet listing process")
                clinic.list_pets()
            case 4:
                logging.info("Starting consultation search process")
                clinic.search_consultation()
            case 5:
                logging.info("User chose to exit the program")
                break
            case _:
                logging.warning(f"Invalid menu option selected: {option}")
                print("invalid option")

if __name__ == "__main__":
    logging.info("Starting Veterinary Clinic Management System")
    menu()
    logging.info("Veterinary Clinic Management System terminated")