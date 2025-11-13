import csv


class FoodTruck:
    def __init__(self, name, location):
        """
        Basic FoodTruck object.
        It will store information about:
        - the truck itself
        - staff
        - customers
        - schedules (work shifts)
        """

        # Basic info
        self.name = name
        self.location = location

        # Lists to store related data
        self.staff = []        # list of staff dicts
        self.customers = []    # list of customer names (for now)
        self.schedules = [] 
        self.orders = []       # list of order dicts
   # list of schedule dicts

    def intro(self):
        """
        Return a short description of this food truck.
        """
        return f"{self.name} is serving food at {self.location}!"

    # ---------- STAFF METHODS ----------

    def add_staff(self, name):
        """
        Add a staff member by name to the staff list (simple version).
        """
        self.staff.append(name)

    def list_staff(self):
        """
        Return the list of staff (simple names list).
        """
        return self.staff

    # ---------- CUSTOMER METHODS ----------

    def add_customer(self, name):
        """
        Add a customer by name to the customers list.
        """
        self.customers.append(name)

    def list_customers(self):
        """
        Return the list of customers.
        """
        return self.customers

    # ---------- STAFF CSV METHODS ----------

    def add_staff_to_csv(self, email, password, first, last, phone, address, dob, sex):
        """
        Add a staff member's full details to users.csv.
        """
        with open("data/users.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([email, password, first, last, phone, address, dob, sex])

        print(f"Saved {first} {last} to users.csv")

    def load_staff_from_csv(self):
        """
        Load all staff from users.csv into the FoodTruck object's staff list.
        Each staff member becomes a dictionary.
        """
        self.staff = []  # reset the list first

        try:
            with open("data/users.csv", mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.staff.append({
                        "email": row["Email"],
                        "password": row["Password"],
                        "first": row["First_Name"],
                        "last": row["Last_Name"],
                        "phone": row["Mobile_Number"],
                        "address": row["Address"],
                        "dob": row["DOB"],
                        "sex": row["Sex"]
                    })
            print("Loaded staff from users.csv")
        except FileNotFoundError:
            print("users.csv not found — skipping load.")

    # ---------- SCHEDULE CSV METHODS ----------

    def add_schedule_to_csv(self, manager, date, time, staff_email, staff_name, work_time):
        """
        Add a work schedule (shift) to schedules.csv.
        One row will be added with:
        Manager, Date, Time, staff_Email, staff_Name, work_Time
        """
        with open("data/schedules.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([manager, date, time, staff_email, staff_name, work_time])

        print(f"Saved schedule for {staff_name} on {date} at {time} to schedules.csv")

    def load_schedules_from_csv(self):
        """
        Load all schedules from schedules.csv into the FoodTruck object's schedules list.
        Each schedule will be stored as a dictionary.
        """
        self.schedules = []  # reset the list first

        try:
            with open("data/schedules.csv", mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.schedules.append({
                        "manager": row["Manager"],
                        "date": row["Date"],
                        "time": row["Time"],
                        "staff_email": row["staff_Email"],
                        "staff_name": row["staff_Name"],
                        "work_time": row["work_Time"]
                    })
            print("Loaded schedules from schedules.csv")
        except FileNotFoundError:
            print("schedules.csv not found — skipping load.")

    # ---------- SCHEDULE LOGIC METHODS ----------

    def is_time_slot_available(self, staff_email, date, time):
        """
        Check if a staff member is free at a given date and time.
        Returns True if available, False if there is a conflict.
        """
        for s in self.schedules:
            if (
                s["staff_email"] == staff_email and
                s["date"] == date and
                s["time"] == time
            ):
                # Found an existing schedule at this date/time for this staff
                return False
        return True

    def book_schedule(self, manager, date, time, staff_email, staff_name, work_time):
        """
        Book a schedule ONLY if the time slot is available.
        - First checks self.schedules for a conflict.
        - If free, adds it to memory and CSV.
        """
        if not self.is_time_slot_available(staff_email, date, time):
            print(f"Cannot book: {staff_name} already has a shift on {date} at {time}.")
            return False

        # Add to in-memory list
        new_schedule = {
            "manager": manager,
            "date": date,
            "time": time,
            "staff_email": staff_email,
            "staff_name": staff_name,
            "work_time": work_time
        }
        self.schedules.append(new_schedule)

        # Save to CSV file
        self.add_schedule_to_csv(manager, date, time, staff_email, staff_name, work_time)

        print(f"Booked {staff_name} on {date} at {time}.")
        return True
        # ---------- MENU / ALLERGY HELPERS ----------

    def get_menu_allergens(self):
        """
        Simple hard-coded allergen info for menu items.
        You can expand this later.
        """
        return {
            "Original Chicken Sandwich Combo": ["gluten", "wheat", "egg"],
            "Wings & Wedges Box": ["gluten", "wheat"],
            "Family Bucket": ["gluten", "wheat"],
        }

    def is_order_safe_for_allergy(self, item_name, allergy_text):
        """
        Check if an order is safe based on the customer's allergy text.
        Returns True if safe, False if potentially unsafe.
        """
        allergy_text = allergy_text.lower().strip()
        if allergy_text == "":
            # Customer reported no allergies
            return True

        menu_allergens = self.get_menu_allergens()
        item_allergens = menu_allergens.get(item_name, [])

        # If any allergen word appears in the allergy text, mark unsafe
        for allergen in item_allergens:
            if allergen in allergy_text:
                return False
        return True


        # ---------- ORDERS CSV METHODS ----------

    def add_order_to_csv(self, customer_name, customer_email, item, allergy_info):
        """
        Save a customer order to orders.csv and to self.orders.
        Automatically checks if the order is safe based on allergy.
        """
        is_safe = self.is_order_safe_for_allergy(item, allergy_info)
        is_safe_str = "YES" if is_safe else "NO"

        # Very simple order id = number of existing orders + 1
        order_id = len(self.orders) + 1

        from datetime import datetime
        timestamp = datetime.now().isoformat(timespec="seconds")

        # Append to CSV
        with open("data/orders.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                order_id,
                customer_name,
                customer_email,
                item,
                allergy_info,
                is_safe_str,
                timestamp
            ])

        # Add to in-memory list
        self.orders.append({
            "order_id": order_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "item": item,
            "allergy_info": allergy_info,
            "is_safe": is_safe_str,
            "timestamp": timestamp
        })

        return is_safe  # True = safe, False = unsafe

    def load_orders_from_csv(self):
        """
        Load all orders from orders.csv into self.orders.
        """
        self.orders = []

        try:
            with open("data/orders.csv", mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.orders.append({
                        "order_id": row["Order_ID"],
                        "customer_name": row["Customer_Name"],
                        "customer_email": row["Customer_Email"],
                        "item": row["Item"],
                        "allergy_info": row["Allergy_Info"],
                        "is_safe": row["Is_Safe"],
                        "timestamp": row["Timestamp"],
                    })
            print("Loaded orders from orders.csv")
        except FileNotFoundError:
            print("orders.csv not found — skipping load.")
