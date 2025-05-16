from clinic import Clinic

def menu():
    clinic = Clinic()
    while True:
        print("1. Register pet \n"
              "2. Register consultation \n"
              "3. List pets \n"
              "4. Ver historial de consultas de una mascota específica. \n"
              "5. Exit")
        option = int(input("Chose one option: "))
        match option:
            case 1:
                clinic.add_pet()
            case 2:
                clinic.add_consultation()
            case 3:
                clinic.list_pets()
            case 4:
                clinic.search_consultation()
            case 5:
                break
            case _:
                print("invalid option")



menu()

