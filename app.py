from flask import Flask, render_template, request, redirect, url_for, session
from foodtruck import FoodTruck

app = Flask(__name__)

# Secret key for sessions (demo only)
app.secret_key = "cs120-foodtruck-secret"

# Hardcoded admin login
ADMIN_EMAIL = "admin@foodtruck.com"
ADMIN_PASSWORD = "admin123"

# Backend instance
my_truck = FoodTruck("CS120 Food Truck", "GSU Campus")
my_truck.load_staff_from_csv()
my_truck.load_schedules_from_csv()
my_truck.load_orders_from_csv()


# ---------- HELPERS ----------

def require_admin():
    if "admin" not in session:
        return redirect(url_for("login"))
    return None


def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart


@app.context_processor
def inject_globals():
    cart = get_cart()
    cart_count = sum(item["qty"] for item in cart.values())
    return dict(
        is_admin=("admin" in session),
        admin_email=session.get("admin"),
        cart_count=cart_count,
        truck=my_truck,
    )


# ---------- CUSTOMER FLOW: HOME → MENU → CART → CHECKOUT ----------

@app.route("/")
def home():
    featured_items = my_truck.get_menu_items()[:3]
    return render_template(
        "home.html",
        featured_items=featured_items,
        staff_count=len(my_truck.staff),
        schedule_count=len(my_truck.schedules),
        title="Home - CS120 Food Truck",
    )


@app.route("/menu")
def menu_page():
    menu_items = my_truck.get_menu_items()
    return render_template("menu.html", menu_items=menu_items, title="Menu")


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    item_name = request.form["item_name"]
    price = float(request.form["price"])
    redirect_to = request.form.get("redirect_to", url_for("menu_page"))

    cart = get_cart()
    if item_name in cart:
        cart[item_name]["qty"] += 1
    else:
        cart[item_name] = {"price": price, "qty": 1}
    save_cart(cart)

    return redirect(redirect_to)


@app.route("/cart")
def cart_page():
    cart = get_cart()
    total = sum(item["price"] * item["qty"] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total, title="Your Cart")


@app.route("/cart/clear")
def clear_cart():
    save_cart({})
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    if not cart:
        return redirect(url_for("menu_page"))

    total = sum(item["price"] * item["qty"] for item in cart.values())
    items_summary = ", ".join(
        f"{name} x{item['qty']}" for name, item in cart.items()
    )

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        customer_email = request.form["customer_email"]
        allergy_info = request.form["allergy_info"]

        my_truck.add_order_to_csv(
            customer_name, customer_email, items_summary, allergy_info
        )
        my_truck.load_orders_from_csv()

        save_cart({})

        return render_template(
            "checkout_success.html",
            customer_name=customer_name,
            total=total,
            title="Order Confirmed",
        )

    return render_template(
        "checkout.html",
        cart=cart,
        total=total,
        items_summary=items_summary,
        title="Checkout",
    )


# ---------- AUTH (MANAGER LOGIN) ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["admin"] = email
            return redirect(url_for("home"))
        else:
            error = "Invalid email or password."

    return render_template("login.html", error=error, title="Manager Login")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


# ---------- STAFF (ADMIN) ----------

@app.route("/staff")
def staff_page():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    my_truck.load_staff_from_csv()
    return render_template("staff.html", staff=my_truck.staff, title="Staff")


@app.route("/add_staff", methods=["GET"])
def add_staff_form():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    return render_template("add_staff.html", title="Add Staff")


@app.route("/add_staff", methods=["POST"])
def add_staff_submit():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    email = request.form["email"]
    password = request.form["password"]
    first = request.form["first"]
    last = request.form["last"]
    phone = request.form["phone"]
    address = request.form["address"]
    dob = request.form["dob"]
    sex = request.form["sex"]

    my_truck.add_staff_to_csv(email, password, first, last, phone, address, dob, sex)
    my_truck.load_staff_from_csv()

    return redirect(url_for("staff_page"))


# ---------- SCHEDULES (ADMIN) ----------

@app.route("/schedules")
def schedules_page():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    my_truck.load_schedules_from_csv()
    return render_template("schedules.html", schedules=my_truck.schedules, title="Schedules")


@app.route("/book_schedule", methods=["GET"])
def book_schedule_form():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    my_truck.load_staff_from_csv()
    return render_template("book_schedule.html", staff=my_truck.staff, title="Book Schedule")


@app.route("/book_schedule", methods=["POST"])
def book_schedule_submit():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    manager = request.form["manager"]
    date = request.form["date"]
    time = request.form["time"]
    staff_email = request.form["staff_email"]
    work_time = request.form["work_time"]

    my_truck.load_staff_from_csv()
    staff_name = None
    for s in my_truck.staff:
        if s["email"] == staff_email:
            staff_name = f"{s['first']} {s['last']}"
            break

    if staff_name is None:
        return "Staff not found. <a href='/book_schedule'>Back</a>"

    my_truck.load_schedules_from_csv()
    success = my_truck.book_schedule(
        manager=manager,
        date=date,
        time=time,
        staff_email=staff_email,
        staff_name=staff_name,
        work_time=work_time,
    )

    if not success:
        return (
            "That staff member is already booked at that date/time. "
            "<a href='/book_schedule'>Back</a>"
        )

    return redirect(url_for("schedules_page"))


# ---------- ADMIN DASHBOARD + ORDERS ----------

@app.route("/admin")
def admin_dashboard():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    my_truck.load_staff_from_csv()
    my_truck.load_schedules_from_csv()
    my_truck.load_orders_from_csv()

    unsafe_count = sum(1 for o in my_truck.orders if o["is_safe"] == "NO")

    return render_template(
        "admin_dashboard.html",
        staff_count=len(my_truck.staff),
        schedule_count=len(my_truck.schedules),
        orders_count=len(my_truck.orders),
        unsafe_orders_count=unsafe_count,
        title="Admin Dashboard",
    )


@app.route("/admin/orders")
def admin_orders_page():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    my_truck.load_orders_from_csv()
    return render_template("admin_orders.html", orders=my_truck.orders, title="Admin Orders")


if __name__ == "__main__":
    app.run(debug=True)
