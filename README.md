# Q-ARM Control & Order Processing Software

## Overview

The application supports:
- User authentication and registration
- Product lookup and order creation
- Q-ARM pick-and-pack execution
- Simple menu-based program flow

---

## Functions (main.py)

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

  ##  q_arm_code.py includes robot movement commands and functions only
