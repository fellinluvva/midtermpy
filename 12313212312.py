import os
import csv
import json


# Welcome
def display_welcome():
    print("Welcome to the Online Bookstore Management System")


# Menu
def display_menu():
    print("Menu:")
    print("1. Login")
    print("2. Exit")


# login input from user
def login():
    username = input("Username: ")
    password = input("Password: ")

    # sample
    valid_username = "user123"
    valid_password = "password123"

    if username == valid_username and password == valid_password:
        print("Login Successful!")
        return True
    else:
        print("Invalid credentials. Please try again.")
        return False


# directory creation
def create_directory_structure():
    os.makedirs("BookstoreData/Books", exist_ok=True)
    os.makedirs("BookstoreData/Customers", exist_ok=True)


def initialize_books_csv():
    books_data = [
        ["Python Programming", "John Smith", 2020, 29.99],
        ["Data Structures in Python", "Emily Johnson", 2019, 24.95],
        # samples
    ]

    #  to add lines in csv file use writer
    with open("BookstoreData/Books/books.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Publication Year", "Price"])  # instead of writing in every line
        writer.writerows(books_data)

    print("\nBooks sample:")
    with open("BookstoreData/Books/books.csv", mode="r") as file:
        for line in file:
            print(line.strip())


def initialize_customers_csv():
    customers_data = [
        ["Customer1", "customer1@email.com", "Python Programming", 2],
        ["Customer2", "customer2@email.com", "Data Structures in Python", 1],
        # Samples can add more
    ]

    #  to add lines in csv file use writer
    with open("BookstoreData/Customers/customers.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Book Title", "Quantity"])  # same reason as in customers
        writer.writerows(customers_data)

    print("\nCustomers:")
    with open("BookstoreData/Customers/customers.csv", mode="r") as file:
        for line in file:
            print(line.strip())


# adding inventory via json
def initialize_inventory_json():
    inventory_data = {}
    with open("BookstoreData/inventory.json", mode="w") as file:
        json.dump(inventory_data, file)


# every time update data in json
def update_inventory(book_title, quantity):
    try:
        with open("BookstoreData/inventory.json", mode="r") as file:
            inventory_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        inventory_data = {}

    if book_title in inventory_data:
        inventory_data[book_title] += quantity
    else:
        inventory_data[book_title] = quantity

    with open("BookstoreData/inventory.json", mode="w") as file:
        json.dump(inventory_data, file)


def display_books():
    print("List of Books:")
    with open("BookstoreData/Books/books.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            title, author, year, price = row
            print(f"Title: {title}, Author: {author}, Price: ${price}")


def place_order():
    title = input("Book Title: ")
    quantity = int(input("Quantity: "))

    # find data in csv file
    with open("BookstoreData/Books/books.csv", mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        books_data = list(reader)

    # search and add quantity to data
    for book in books_data:
        if book[0] == title:
            stock = float(book[3])
            if stock >= quantity:
                stock -= quantity
                book[3] = str(stock)

                with open("BookstoreData/Books/books.csv", mode="w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Title", "Author", "Publication Year", "Price"])
                    writer.writerows(books_data)

                # json update data to add customer orders
                with open("BookstoreData/Customers/customers.csv", mode="a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Customer1", "customer1@email.com", title, quantity])

                update_inventory(title, quantity)

                print("Order Placed Successfully!")
            else:
                print("Not enough stock available.")
            break
    else:
        print("Invalid input, Book not found.")


def display_inventory():
    print("Inventory:")
    try:
        with open("BookstoreData/inventory.json", mode="r") as file:
            inventory_data = json.load(file)
            if not inventory_data:
                print("No items in inventory.")
            else:
                for book_title, stock in inventory_data.items():
                    print(f"- Book: {book_title}, Stock: {stock}")
    except FileNotFoundError:
        print("Inventory file not found.")
    except json.decoder.JSONDecodeError:
        print("Inventory file is empty or corrupt.")


def logout():
    print("Logout Successful!")


def main_menu():
    while True:
        print("Menu:")
        print("1. Display Books")
        print("2. Place Order")
        print("3. Display Inventory")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_books()
        elif choice == "2":
            place_order()
        elif choice == "3":
            display_inventory()
        elif choice == "4":
            logout()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def user_authentication():
    while True:
        display_welcome()
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":  # if login then run login
            if login():  # then run second menu
                break
        elif choice == "2":
            print("Goodbye! Thank you for using the Online Bookstore Management System.")
            exit()
        else:
            print("Invalid choice. Please enter 1 or 2.")


# code initialization:
user_authentication()

main_menu()
