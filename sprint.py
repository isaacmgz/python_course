import re

# Lists to store emails
students = []
professors = []


def main():
    option = 0  # initialize menu option

    # loop until Exit is selected (4)
    while option != 4:
        menu = (
            "Choose one option:\n"
            " 1. Sign up new email\n"
            " 2. View registered emails\n"
            " 3. Search an email\n"
            " 4. Exit\n"
        )
        option = int(input(menu))  # get user choice
        if option == 1:
            add_email(students, professors)  # register new email
        elif option == 2:
            show_emails(students, professors)  # display stored emails
        elif option == 3:
            search_email(students + professors)  # search in combined list
        elif option == 4:
            print("Exiting...")
        else:
            print("Invalid option")  # handle wrong input


def add_email(students, professors):
    email = input("Enter your email: ")
    validator = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(validator, email):
        print("Invalid syntax")
        return
    parts = email.split("@")  # split into user and domain
    if len(parts) != 2:
        print("Invalid format")
        return
    domain = parts[1]  # domain part
    if domain == "estudiante.utv.edu.co":
        students.append(email)
    elif domain == "utv.edu.co":
        professors.append(email)
    else:
        print("Invalid email domain")  # domain not recognized
        return
    print("Email registered successfully")


def show_emails(students, professors):
    print("Students:")
    for student in students:
        print(student)

    print("Professors:")
    for prof in professors:
        print(prof)


def search_email(email_list):
    query = input("Enter user name or full email to search: ")
    for email in email_list:
        if re.search(query, email):  # regex matches anywhere
            print("Email found:", email)
            return
    print("Email not found")  # no matches found


if __name__ == "__main__":
    main()
