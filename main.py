"""
Team: Fri-24
Course: ENGINEER 1P13: Introduction to Programming
Term: Fall, 2025

Title: Project 1

Description: 

A command-line ordering system that connects user authentication,
product lookups, order processing, and automated packing using the Q-Arm.
The program lets users create accounts, sign in securely, place orders,
view their order history, and have selected products packed by the robot arm (Q-arm).

Features:

    - Account creation with password validation and bcrypt hashing
    - User sign-in and credential verification
    - Product retrieval from products.csv
    - Order pricing, discounts, taxes, and receipt generation
    - Order history logging and customer summaries
    - Physical packing operations via Q-Arm functions
    - Interactive menu-driven interface

Data Files:

    users.csv      Stores user IDs and hashed passwords
    products.csv   Lists product names and prices
    orders.csv     Records completed orders for all users

"""


## Imports
import random
import time
import csv
from collections import defaultdict, Counter
import bcrypt
from q_arm_code import *






def load_users():
    """ helper funcntion to authenticate(): loads existing users from csv """
    users = []  # 2D list:[[userid, hash_password],[userid, hash_password]...]
    try:
        with open("users.csv", "r", newline="") as file:
            for line in file:
                line = line.strip()  # remove \n that would interfere with the comparison
                if not line:
                    continue
                parts = line.split(",", 1)  # userid,hash (hash may contain commas)
                if len(parts) == 2:
                    userid = parts[0].strip()
                    hash_password = parts[1].strip()
                    users.append([userid, hash_password])
    except FileNotFoundError:
        # No users yet; return empty list
        pass
    return users


def authenticate():
    """ Authenticates a user by comparing entered credentials with stored data.
    If user doesn't have an account, calls sign_up() first. """
    while True:
        have_account = input("Hi there! Do you have an account? (yes/no) ").lower().strip()
        if have_account == "no":
            sign_up()
            break
        elif have_account == "yes":
            break
        else:
            print("Please answer 'yes' or 'no'!")

    # authentication loop
    while True:
        userid = input("Enter your userid: ").strip()
        password = input("Enter your password: ").strip()

        users = load_users()

        user_found = False
        for user in users:
            if user[0] == userid:
                user_found = True
                stored_hash = user[1]
                # Check if entered password matches stored hash
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                        print("Authentication successful!")
                        return userid
                    else:
                        print("Incorrect password. Please try again.")
                except Exception:
                    print("Stored password hash invalid. Contact admin.")
                break

        if not user_found:
            print("Userid not found. Please try again.")


def sign_up():

    """
    By: Zakariya Yahmad
    
    Creates a new user account by validating a unique username,
    setting and enforcing password requirements, hashing the password, and
    storing credentials in "users.csv".

    Returns:
        None
        
    """

    ## load existing user ids
    existing_users = []
    # tries to read users.csv file (do not truncate)
    try:
        with open("users.csv", "r", newline="") as file:
            for line in file:
                line = line.strip()
                if line:  # skip blank lines
                    user = line.split(",")[0].strip()
                    existing_users.append(user)
    except FileNotFoundError:
        # file doesn't exist yet
        pass

    # gets new user_id
    user_id = input("Enter a username: ").strip()
    while user_id in existing_users or user_id == "":
        if user_id == "":
            print("Username cannot be blank.")
        else:
            print("Username already exists. Try another.")
        user_id = input("Enter a username: ").strip()

    ## password rules
    legal_symbols = "!.@#$%^&*()_[]"

    while True:
        password = input("Enter a password: ")

        # length rule
        if len(password) < 6:
            print("Password must be at least 6 characters.")
            continue

        # uppercase rule
        if not any(c.isupper() for c in password):
            print("Password must contain an uppercase letter.")
            continue

        # lowercase rule
        if not any(c.islower() for c in password):
            print("Password must contain a lowercase letter.")
            continue

        # digit rule
        if not any(c.isdigit() for c in password):
            print("Password must contain a digit.")
            continue

        # symbol rule
        if not any(c in legal_symbols for c in password):
            print("Password must contain a symbol:", legal_symbols)
            continue

        break  # password is valid

    ## hash password
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # append hash to csv
    with open("users.csv", "a", newline="") as file:
        file.write(f"{user_id},{hashed}\n")

    print("Account created.")


def lookup_products(products):
    """
    products: either a comma-separated string of product names (e.g. "Bottle,Rook")
              or any other value (like an int placeholder) — in the latter case ask user.
    Returns: list of [name, price] pairs found in products.csv
    """
    if not isinstance(products, str):
        # keep same structure as main where barcode is a placeholder int
        products = input("Enter product names (comma-separated): ").strip()

    product_list = [p.strip() for p in products.split(",") if p.strip()]

    try:
        with open("products.csv", "r", newline="") as file:
            all_lines = [ln.strip() for ln in file if ln.strip()]
    except FileNotFoundError:
        print("Error: Could not open products.csv.")
        return []

    all_names = []
    all_prices = []

    for line in all_lines:
        # allow commas in product names by splitting on last comma or splitting once
        if "," in line:
            name, price = line.rsplit(",", 1)
        else:
            # unrecognized line
            continue
        name = name.strip()
        try:
            price_val = float(price.strip())
        except ValueError:
            # skip unformatted price lines
            continue
        all_names.append(name)
        all_prices.append(price_val)

    found_products = []

    for item in product_list:
        if item in all_names:
            index = all_names.index(item)
            found_products.append([all_names[index], all_prices[index]])
        else:
            print(f"error: '{item}' is deemed invalid in the database")

    return found_products


def complete_order(user_id, product_list):
    '''
    This function takes the product list and the users id as parameters and prints a recipt for the users order in the shell and records their order and userid under the order.csv file.
    '''


    print("Generating Recipt...")
    time.sleep(1.5)
    prices = []
    products = []
    order = []  # list for current order 

    try:
        orders = open("orders.csv", 'a', newline="")
    except Exception as e:
        print("Error opening orders.csv for append:", e)
        return

    ## extracts products and prices from original product list into separate lists
    for i in range(len(product_list)):
        try:
            prices.append(float(product_list[i][1]))
            products.append(product_list[i][0])
            order.append(product_list[i][0])
        except Exception:
            print("Unrecognized product entry; skipping.")
            continue

    if not prices:
        print("No valid products to order.")
        orders.close()
        return

    ## all cost calculations
    discount = (random.randint(5, 50))  # randomly generates discount from 5% to 50%
    subtotal = sum(prices)
    applied_discount = subtotal * (discount / 100)  # calculates discount applied
    discounted_cost = subtotal - applied_discount
    tax = discounted_cost * 0.13
    total = discounted_cost + tax  # total

    # updates file with new order
    # add user id and total to start of order list
    order.insert(0, user_id)
    order.insert(1, f"{total:.2f}")
    order_line = ','.join(order)
    orders.write(order_line + "\n")
    orders.close()

    # determines total number of orders specific user has made
    num_orders = 0
    try:
        with open("orders.csv", 'r', newline="") as orders_r:
            for user_order in orders_r:
                line = (user_order.strip().split(","))
                if line and line[0] == user_id:
                    num_orders += 1
    except FileNotFoundError:
        num_orders = 0

    ## Following code prints recipt to shell for user
    print(f"\n{'':=^40}")
    print(f"{'RECIPT':^40}")
    print(f"{'':=^40}")
    print(f"{'ITEM':<35}PRICE\n")

    for i in range(len(products)):
        price = f"{prices[i]:.2f}"
        # simplified formatting to avoid odd width math
        print(f"{products[i]:<30}{'$'+price:>10}")

    print()  # spacer

    print(f"{'SUBTOTAL:':>30}{f'${subtotal:.2f}':>10}")
    print(f"{f'DISCOUNT {discount}%:':>30}{f'-${applied_discount:.2f}':>10}")
    print(f"{'TAX:':>30}{f'${tax:.2f}':>10}")
    print(f"\n{'':=^40}\n{'TOTAL:':>30}{f'${total:.2f}':>10}")
    print(f"{'':=^40}")
    print(f"Number of Orders Placed: {num_orders}")
    print(f"{'':=^40}")
    print(f"\n{'Thank you for shopping!':^40}")


def customer_summary(userid):

    # ---------------------------------------------------------------
# Function: customer_summary(userid)
# Description:
#     Reads order records from "orders.csv" and generates a 
#     detailed summary for a specific customer. The summary 
#     includes:
#         - Total number of orders made by the user
#         - Total amount spent
#         - A breakdown of all products purchased and quantities
#
#     The CSV format is expected to follow:
#         column 0 : user ID
#         column 1 : order amount (float)
#         column 2+: product names purchased in the order
#
#     The function prints a formatted summary table. If the 
#     orders file is missing, it notifies the user and returns.
#
# Parameters:
#     userid (str) – the customer ID to look up
#
# Dependencies:
#     - csv module
#     - collections.Counter
#
# ---------------------------------------------------------------

    
    orders_file = "orders.csv"
    total_orders = 0
    total_spent = 0.0
    product_counter = Counter()

    try:
        with open(orders_file, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row or row[0] != userid:
                    continue
                total_orders += 1
                try:
                    total_spent += float(row[1])
                except Exception:
                    pass
                products = row[2:]  # remaining columns are product names
                product_counter.update(products)
    except FileNotFoundError:
        print("No orders found.")
        return

    # Print professional summary
    print("\n" + "=" * 50)
    print(f"{'CUSTOMER SUMMARY':^50}")
    print("=" * 50)
    print(f"Customer: {userid}")
    print(f"Total Orders: {total_orders}")
    print(f"Total Spent: ${total_spent:,.2f}")
    print("-" * 50)
    print(f"{'Product':<35} {'Qty':>5}")
    print("-" * 50)
    for product, qty in product_counter.items():
        print(f"{product:<35} {qty:>5}")
    print("=" * 50 + "\n")



def pack_products(product_list):
    """
    Packs products using the QArm.
    product_list format: [[name, price], ...]
    """

    for product in product_list:
        name = product[0]  # product name

        # map product names to the correct arm function
        if name.lower() == "sponge":
            lvl_1()
        elif name.lower() == "bottle":  
            lvl_2()
        elif name.lower() == "rook":  
            lvl_3()
        elif name.lower() == "d12":
            lvl_3a()
        elif name.lower() == "witchhat":
            lvl_4a()
        elif name.lower() == "bowl":
            lvl_4b

        else:
            print(f"Product not found.")

        print(f"Packed {name}")




## Main/Menu related functions
def return_to_menu(menu_choice):
    '''This function takes the users menu choice as a parameter and asks the user if they wish to return to menu. If not they remain in their originally chosen menu choice '''
    menu_return = input("\nReturn to menu?(yes/no):")

    # if user wishes to return the menu_run loop is bt=roken and user returns to main menu.
    if menu_return.lower() == "yes":
        print(f"\n{'Returning to menu...':^50}\n")
        time.sleep(1)
        return None, False  # returned to menu_choice, menu_run, in that order

    # if user doesnt wish to return to menu or inputs an invalid input threy remian in their origninal menu choice and are asked if they wish to return again.
    elif menu_return.lower() == "no":
        return menu_choice, True

    else:
        print(f"\n{'INVALID ENTRY':*^50}\n")
        return menu_choice, True


def add_order():
    '''This function allows user to make an additional order during the same ordering session '''
    add_order_input = input("Would you like to place another order?(yes/no):")
    # if user wants to make an additional order:
    if add_order_input.lower() == "yes":
        return 1  # returned to menu_choice variable

    # if user doesnt make an additional order they proceed to customer_summary
    elif add_order_input.lower() == "no":
        return 2

    else:
        print(f"\n{'INVALID ENTRY':*^50}\n")
        time.sleep(0.5)
        return add_order()  # recurse until valid


def main():
    barcode = 1  # placeholder:delete later

    user_id = authenticate()

    print(f"{'':-^50}\n")
    print(f"{f'Welcome {user_id}!':^50}\n")

    main_loop = True  # main loop condition
    while main_loop:
        # menu options:
        print(f"{'':-^50}\n")
        print(f"{'MENU':^50}\n")
        print(f"{'1.':>20}" + "Place Order")
        print(f"{'2.':>20}" + "Order History")
        print(f"{'3.':>20}" + "Exit")

        try:
            menu_choice = int(input("\nPlease enter a menu option number:"))
        except ValueError:
            print("Invalid menu entry. Try again.")
            continue

        menu_run = True  # menu_run loop condition
        while menu_run:
            if menu_choice == 1:
                product_list = lookup_products(barcode)  # placeholder:change to scan_barcode()
                pack_products(product_list)
                complete_order(user_id, product_list)

                menu_choice = add_order()

            elif menu_choice == 2:
                customer_summary(user_id)

                menu_choice, menu_run = return_to_menu(menu_choice)
            elif menu_choice == 3:
                print(f"\n{'Goodbye! Come again soon...':^50}\n")
                time.sleep(1)
                exit()  # exit function; allows a clean exit from program
            else:
                print(f"\n{'INVALID ENTRY':*^50}\n")
                time.sleep(0.5)
                menu_run = False  # breaks menu_run loop and loops back to main loop


if __name__ == "__main__":
    main()
