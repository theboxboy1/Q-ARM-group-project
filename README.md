# Q-ARM Control & Order Processing Software

This repository contains a lightweight Python application for controlling the **Q-ARM** and demonstrating a basic order-processing workflow. The focus is on **robotic arm movement and pick-and-place logic**, not on full production features.

---

## Overview

The application supports:
- User authentication and registration
- Product lookup and order creation
- Q-ARM pick-and-pack execution
- Simple menu-based program flow

---

## Functions

- **`load_users()`**  
  Loads stored user data.

- **`authenticate()`**  
  Handles user login.

- **`sign_up()`**  
  Registers a new user.

- **`lookup_products()`**  
  Displays available products.

- **`add_order()`**  
  Creates an order from user selections.

- **`pack_products()`**  
  Executes Q-ARM pick-and-pack logic.

- **`complete_order()`**  
  Finalizes the order.

- **`customer_summary()`**  
  Displays a summary of the order.

- **`return_to_menu()`**  
  Returns program flow to the main menu.

- **`main()`**  
  Runs the main program.
