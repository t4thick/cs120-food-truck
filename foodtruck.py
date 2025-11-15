import csv
from datetime import datetime


class FoodTruck:
    """
    Backend class for the CS120 Food Truck system.
    Handles staff, schedules, menu, orders and allergy checks using CSV files.
    """

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.staff = []
        self.schedules = []
        self.orders = []

    # ---------- MENU DATA ----------

    def get_menu_items(self):
        """
        Returns a list of menu items with details.
        Each item has: name, description, price, category, vegan flag, image, allergens.
        Image files live in static/images.
        """
        return [
            {
                "name": "Original Chicken Sandwich Combo",
                "description": "Crispy chicken sandwich, fries & drink.",
                "price": 7.99,
                "category": "Non-Veg",
                "vegan": False,
                "image": "burger.jpg",
                "allergens": ["gluten", "wheat", "egg"],
            },
            {
                "name": "Wings & Wedges Box",
                "description": "Spicy wings with seasoned potato wedges.",
                "price": 9.49,
                "category": "Non-Veg",
                "vegan": False,
                "image": "wings.jpg",
                "allergens": ["gluten", "wheat"],
            },
            {
                "name": "Family Bucket",
                "description": "12 pc chicken, large fries & slaw.",
                "price": 19.99,
                "category": "Non-Veg",
                "vegan": False,
                "image": "bucket.jpg",
                "allergens": ["gluten", "wheat"],
            },
            {
                "name": "Veggie Bowl",
                "description": "Rice bowl with crispy veggies and sauce.",
                "price": 8.49,
                "category": "Veg",
                "vegan": True,
                "image": "veggie.jpg",
                "allergens": ["soy"],
            },
        ]

    def get_menu_allergens(self):
        """
        Build a mapping from item name -> list of allergens,
        based on the menu items above.
        """
        allergens_map = {}
        for item in self.get_menu_items():
            allergens_map[item["name"]] = item["allergens"]
        return allergens_map

    def is_order_safe_for_allergy(self, items_text, allergy_text):
        """
        Check if an order (possibly multiple items) is safe based on allergy text.
        items_text can be a single item name or a combined string like
        'Original Chicken Sandwich Combo x2, Wings & Wedges Box x1'.
        Returns True if safe, False if any allergen matches.
        """
        allergy_text = allergy_text.lower().strip()
        if allergy_text == "":
            return True  # no allergy reported

        menu_allergens = self.get_menu_allergens()
        items_text_lower = items_text.lower()

        combined_allergens = set()
        for item_name, allergens in menu_allergens.items():
            if item_name.lower() in items_text_lower:
                combined_allergens.update(allergens)

        if not combined_allergens and items_text in menu_allergens:
            combined_allergens.update(menu_allergens[items_text])

        for allergen in combined_allergens:
            if allergen in allergy_text:
                return False

        return True

    # ---------- STAFF (CSV) ----------

    def load_staff_from_csv(self, path="data/users.csv"):
        self.staff = []
        try:
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.staff.append(
                        {
                            "email": row["Email"],
                            "password": row["Password"],
                            "first": row["First_Name"],
                            "last": row["Last_Name"],
                            "phone": row["Mobile_Number"],
                            "address": row["Address"],
                            "dob": row["DOB"],
                            "sex": row["Sex"],
                        }
                    )
        except FileNotFoundError:
            pass

    def add_staff_to_csv(
        self,
        email,
        password,
        first,
        last,
        phone,
        address,
        dob,
        sex,
        path="data/users.csv",
    ):
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([email, password, first, last, phone, address, dob, sex])

        self.staff.append(
            {
                "email": email,
                "password": password,
                "first": first,
                "last": last,
                "phone": phone,
                "address": address,
                "dob": dob,
                "sex": sex,
            }
        )

    # ---------- SCHEDULES (CSV) ----------

    def load_schedules_from_csv(self, path="data/schedules.csv"):
        self.schedules = []
        try:
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.schedules.append(
                        {
                            "manager": row["Manager"],
                            "date": row["Date"],
                            "time": row["Time"],
                            "staff_email": row["staff_Email"],
                            "staff_name": row["staff_Name"],
                            "work_time": row["work_Time"],
                        }
                    )
        except FileNotFoundError:
            pass

    def book_schedule(
        self,
        manager,
        date,
        time,
        staff_email,
        staff_name,
        work_time,
        path="data/schedules.csv",
    ):
        # prevent double booking
        for s in self.schedules:
            if s["staff_email"] == staff_email and s["date"] == date and s["time"] == time:
                return False  # already booked

        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([manager, date, time, staff_email, staff_name, work_time])

        self.schedules.append(
            {
                "manager": manager,
                "date": date,
                "time": time,
                "staff_email": staff_email,
                "staff_name": staff_name,
                "work_time": work_time,
            }
        )
        return True

    # ---------- ORDERS (CSV) ----------

    def load_orders_from_csv(self, path="data/orders.csv"):
        self.orders = []
        try:
            with open(path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.orders.append(
                        {
                            "order_id": row["Order_ID"],
                            "customer_name": row["Customer_Name"],
                            "customer_email": row["Customer_Email"],
                            "item": row["Item"],
                            "allergy_info": row["Allergy_Info"],
                            "is_safe": row["Is_Safe"],
                            "timestamp": row["Timestamp"],
                        }
                    )
        except FileNotFoundError:
            pass

    def add_order_to_csv(
        self,
        customer_name,
        customer_email,
        items_text,
        allergy_info,
        path="data/orders.csv",
    ):
        is_safe = self.is_order_safe_for_allergy(items_text, allergy_info)
        is_safe_str = "YES" if is_safe else "NO"

        order_id = len(self.orders) + 1
        timestamp = datetime.now().isoformat(timespec="seconds")

        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    order_id,
                    customer_name,
                    customer_email,
                    items_text,
                    allergy_info,
                    is_safe_str,
                    timestamp,
                ]
            )

        self.orders.append(
            {
                "order_id": order_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "item": items_text,
                "allergy_info": allergy_info,
                "is_safe": is_safe_str,
                "timestamp": timestamp,
            }
        )

        return is_safe
