import sqlite3
import os

conn = sqlite3.connect('store_inventory.db')
cursor = conn.cursor()

cursor.execute('''
    
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )   
''')

conn.commit()

def checkReturn():
    choice = input("\nType 'return' to return to the main menu: ")
    if choice.lower() != "return":
        print("Invalid input, try again. ")
        checkReturn()
    else:
        os.system('clear')
        main_menu()

def view_inventory():
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    if products:
        print("\n--- Inventory List ---")
        for product in products:
            print(f"ID: {product[0]} | Name: {product[1]} | Price: ${product[2]:.2f} | Stock: {product[3]}")
        checkReturn()
    else:
        choice = input("\nInventory is empty.")
        checkReturn()

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter the stock quantity: "))

    cursor.execute('INSERT INTO products (name, price, stock) VALUES (?,?,?)', (name,price,stock))
    conn.commit()
    print(f"\nProduct '{name}' added successfully!")
    checkReturn()


def update_stock():
    product_id = int(input("Enter the product ID to update: "))
    new_stock = int(input("Enter the new stock quantity: "))

    cursor.execute('UPDATE products SET stock = ? WHERE product_id = ?', (new_stock, product_id))
    conn.commit()

    if cursor.rowcount > 0:
        print("\nStock updated successfully!")
        checkReturn()

    else:
        print("\nProduct not found.")
        update_stock()

def delete_product():
    product_id = int(input("Enter the product ID to delete: "))

    cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("\nProduct deleted successfully!")
        checkReturn()

    else:
        print("\nProduct not found.")
        delete_product()

def purchase_product():
    product_id = int(input("Enter the product ID to purchase: "))
    quantity = int(input("Enter the quantity to purchase: "))

    cursor.execute('SELECT stock FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()

    if product and product[0] >= quantity:
        new_stock = product[0] - quantity
        cursor.execute('UPDATE products SET stock = ? WHERE product_id = ?', (new_stock, product_id))
        conn.commit()
        print("\nPurchase successful!")
        checkReturn()

    else:
        print("\nPurchase failed. Not enough stock or product not found.")
        purchase_product()

def main_menu():
    print("\n--- Welcome to the Store ---")
    print("1. View Inventory")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Delete Product")
    print("5. Purchase Product")
    print("6. Exit")
    
    def checkChoice(choice):

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            purchase_product()
        elif choice == "6":
            print("Exiting . . .")
        else:
            choice = input("Invalid option, please try again: ")
            checkChoice(choice)

    choice = input("Select an option 1-6: ")
    checkChoice(choice)

main_menu()

