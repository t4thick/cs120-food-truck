# CS120 Food Truck — Documentation & Backend

A small backend utility used by the CS120 Food Truck project. It provides basic in-memory models and CSV-backed persistence for staff, schedules, and customer orders, and includes a simple menu and allergy-safety checking logic.

This README summarizes the project purpose, setup, data formats, and examples of how to use the FoodTruck class (foodtruck.py).

## Table of Contents

- Project Overview
- Features
- Repository layout
- Requirements
- CSV data formats
- Usage examples
- Menu & allergens
- Allergy check behavior
- Contributing
- License

## Project Overview

The `FoodTruck` class (in `foodtruck.py`) is a lightweight backend for handling:

- Staff records (CSV-backed)
- Schedules and bookings (CSV-backed)
- Customer orders (CSV-backed)
- A hardcoded menu (with allergens) and an allergy safety checker

It is designed as a teaching/example codebase for reading/writing CSV data and simple domain logic.

## Features

- Read and append user (staff) records to `data/users.csv`
- Read and append schedule bookings to `data/schedules.csv` with double-book prevention
- Read and append orders to `data/orders.csv`
- Built-in menu items and allergens mapping
- A function to check whether a customer's allergy text makes a given order unsafe

## Repository layout

(Only the important files are listed — adjust to actual repository contents.)

- foodtruck.py         — Main backend class for the project
- data/
  - users.csv          — Staff CSV (not included by default)
  - schedules.csv      — Schedule CSV (not included by default)
  - orders.csv         — Orders CSV (not included by default)
- static/images/       — Example image files for menu items (referenced by name)
- README.md            — This file
- LICENSE              — MIT License (this file)

## Requirements

- Python 3.7+ (uses standard library: csv, datetime)
- No external packages required

## CSV data formats

To use the read/append functions, ensure the CSV files exist (or the code will handle missing files gracefully when loading).

Recommended header rows for each CSV:

- data/users.csv (headers used by load_staff_from_csv)
  - Email,Password,First_Name,Last_Name,Mobile_Number,Address,DOB,Sex

- data/schedules.csv (headers used by load_schedules_from_csv)
  - Manager,Date,Time,staff_Email,staff_Name,work_Time

- data/orders.csv (headers used by load_orders_from_csv)
  - Order_ID,Customer_Name,Customer_Email,Item,Allergy_Info,Is_Safe,Timestamp


## Usage examples

Basic usage from a Python interpreter:

```python
from foodtruck import FoodTruck

ft = FoodTruck(name="Campus FoodTruck", location="Quad")
# Load existing data (if present)
ft.load_staff_from_csv("data/users.csv")
ft.load_schedules_from_csv("data/schedules.csv")
ft.load_orders_from_csv("data/orders.csv")

# Check menu
menu = ft.get_menu_items()
for item in menu:
    print(item["name"], "-", item["price"])

# Add a staff member
ft.add_staff_to_csv(
    email="jane.doe@example.com",
    password="s3cret",
    first="Jane",
    last="Doe",
    phone="555-1234",
    address="123 Main St",
    dob="2000-01-01",
    sex="F",
    path="data/users.csv"
)

# Book a schedule (returns True if booking succeeded)
success = ft.book_schedule(
    manager="manager@example.com",
    date="2025-12-01",
    time="10:00",
    staff_email="jane.doe@example.com",
    staff_name="Jane Doe",
    work_time="10:00-14:00",
    path="data/schedules.csv"
)

# Place an order and check safety
items_text = "Original Chicken Sandwich Combo x1, Veggie Bowl x1"
allergy_info = "I am allergic to soy"
is_safe = ft.add_order_to_csv(
    customer_name="Sam",
    customer_email="sam@example.com",
    items_text=items_text,
    allergy_info=allergy_info,
    path="data/orders.csv"
)
print("Order safe:", is_safe)
```

## Menu & allergens

The project includes a built-in menu. Example entries:

- Original Chicken Sandwich Combo — allergens: gluten, wheat, egg
- Wings & Wedges Box — allergens: gluten, wheat
- Family Bucket — allergens: gluten, wheat
- Veggie Bowl — allergens: soy

get_menu_items() returns the full menu with name, description, price, category, vegan flag, image filename, and allergens list.

## Allergy check behavior

- Method: is_order_safe_for_allergy(items_text, allergy_text)
- items_text may be a single item name, or a combined string like:
  "Original Chicken Sandwich Combo x2, Wings & Wedges Box x1"
- allergy_text is a free-text description of the customer's allergy; the function lower-cases and substring-matches allergens against the allergy text.
- If any allergen present in the matched menu items appears inside the allergy_text, the order is considered unsafe (returns False).
- If the allergy text is blank, the order is considered safe (returns True).

Notes and limitations:
- Matching is substring-based and thus simple; e.g., "soy" will match "soy" but more complex allergy descriptions might require normalization.
- The function checks menu item names by substring matching in the items_text. Ambiguities in item naming could lead to false negatives/positives.



## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Contact / Credits


- Created by the above listed contributors for CS120 course work.

---
