# make_data.py
#
# This script builds pretend data for the Babson Bean Cafe database and
# writes one CSV file per table into projects/db/data/.
#
# New ideas used here that the course has not covered yet:
#   - "def", to write our own functions so the same steps can run for
#     many rows instead of being typed out each time.
#   - the "random" module, to pick realistic-looking values.
#   - the "datetime" module, to work with dates and times.
#   - the "csv" module, to write each table out as a CSV file.
#   - a dictionary holding a whole record: you have read one field from
#     a record before (like row["price"]); here we build the whole
#     record, field by field, before writing it out.

import csv
import os
import random
from datetime import date, datetime, timedelta

random.seed(2026)  # fixed seed: running this script again writes the same files

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# the scenario's 12 months, ending 9/30/2026
START_DATE = date(2025, 10, 1)
END_DATE = date(2026, 9, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days


def random_order_datetime():
    """Pick a random date in range and a random time during cafe hours."""
    offset = random.randint(0, TOTAL_DAYS)
    day = START_DATE + timedelta(days=offset)
    hour = random.randint(7, 19)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(day.year, day.month, day.day, hour, minute, second)


def write_csv(filename, fieldnames, rows):
    """Write a list of dictionaries (records) out as one CSV file."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"wrote {len(rows)} rows to {filename}")


# ---------------------------------------------------------------------
# members
# ---------------------------------------------------------------------

first_names = [
    "Olivia", "Liam", "Emma", "Noah", "Ava", "Ethan", "Sophia", "Mason",
    "Isabella", "Lucas", "Mia", "Logan", "Amelia", "Elijah", "Harper",
    "James", "Evelyn", "Benjamin", "Abigail", "Jack", "Emily", "Henry",
    "Ella", "Daniel", "Scarlett", "Matthew", "Grace", "Sebastian", "Chloe",
    "Jackson", "Victoria", "Owen", "Riley", "Samuel", "Zoey", "David",
    "Lily", "Joseph", "Hannah", "Carter", "Layla", "Wyatt", "Nora", "John",
    "Addison", "Luke", "Aubrey", "Jayden", "Ellie", "Dylan",
]

NUM_MEMBERS = 50
members = []
for i in range(NUM_MEMBERS):
    member_id = f"M{i + 1:04d}"
    name = first_names[i % len(first_names)]
    mobile_number = f"617-555-{1000 + i:04d}"

    # about 1 in 5 members have no email on file (email is optional)
    if i % 5 == 0:
        email = ""
    else:
        email = name.lower() + str(i) + "@example.com"

    join_offset = random.randint(0, TOTAL_DAYS)
    join_date = START_DATE + timedelta(days=join_offset)
    points_balance = random.randint(0, 500)

    members.append({
        "member_id": member_id,
        "first_name": name,
        "mobile_number": mobile_number,
        "email": email,
        "join_date": join_date.isoformat(),
        "points_balance": points_balance,
    })

write_csv(
    "members.csv",
    ["member_id", "first_name", "mobile_number", "email", "join_date", "points_balance"],
    members,
)

# members who joined but never place an order, on purpose: the last 6
members_never_order = set(m["member_id"] for m in members[-6:])

# ---------------------------------------------------------------------
# products
# ---------------------------------------------------------------------

product_catalog = [
    ("Drip Coffee", "coffee"), ("Latte", "coffee"), ("Cappuccino", "coffee"),
    ("Americano", "coffee"), ("Cold Brew", "coffee"), ("Espresso", "coffee"),
    ("Mocha", "coffee"), ("Macchiato", "coffee"),
    ("Green Tea", "tea"), ("Black Tea", "tea"), ("Chai Latte", "tea"), ("Herbal Tea", "tea"),
    ("Croissant", "food"), ("Blueberry Muffin", "food"), ("Bagel", "food"),
    ("Avocado Toast", "food"), ("Banana Bread", "food"), ("Granola Bar", "food"),
    ("Bottled Water", "other"), ("Orange Juice", "other"),
    ("Hot Chocolate", "other"), ("Iced Tea", "other"),
]

products = []
for i, (name, category) in enumerate(product_catalog):
    product_id = f"PR{i + 1:03d}"
    if category == "coffee":
        cost = round(random.uniform(0.60, 1.80), 2)
    elif category == "tea":
        cost = round(random.uniform(0.40, 1.20), 2)
    elif category == "food":
        cost = round(random.uniform(0.80, 2.50), 2)
    else:
        cost = round(random.uniform(0.30, 1.50), 2)
    price = round(cost * random.uniform(1.6, 2.6), 2)

    available_today = True
    if i in (3, 17):  # a couple of items off the menu today (not a broken rule)
        available_today = False

    products.append({
        "product_id": product_id,
        "product_name": name,
        "category": category,
        "price": price,
        "cost": cost,
        "available_today": available_today,
    })

# BROKEN RULE 1, on purpose: "a product's price is never below its cost"
# exactly two rows (0-based row numbers in products.csv, header excluded)
broken_price_rows = [2, 15]
for row_index in broken_price_rows:
    products[row_index]["price"] = round(products[row_index]["cost"] - 0.50, 2)

print("BROKEN RULE: price < cost, rows", broken_price_rows, "of products.csv")
for row_index in broken_price_rows:
    print("  ", products[row_index])

write_csv(
    "products.csv",
    ["product_id", "product_name", "category", "price", "cost", "available_today"],
    products,
)

# products that never sell at all, on purpose (nothing attached to them)
products_never_ordered = {products[20]["product_id"], products[21]["product_id"]}

# ---------------------------------------------------------------------
# options
# ---------------------------------------------------------------------

option_catalog = [
    ("Extra Shot", 0.75, 0.25),
    ("Oat Milk", 0.60, 0.20),
    ("Almond Milk", 0.60, 0.20),
    ("Vanilla Syrup", 0.50, 0.10),
    ("Caramel Syrup", 0.50, 0.10),
    ("Whipped Cream", 0.50, 0.15),
    ("Decaf", 0.00, 0.00),
    ("Extra Hot", 0.00, 0.00),
]

options = []
for i, (name, price, cost) in enumerate(option_catalog):
    options.append({
        "option_id": f"OP{i + 1:02d}",
        "option_name": name,
        "price": price,
        "cost": cost,
    })

write_csv("options.csv", ["option_id", "option_name", "price", "cost"], options)

# an option that is never used on any line, on purpose (nothing attached to it)
option_never_used = options[-1]["option_id"]

# ---------------------------------------------------------------------
# orders, order_lines, line_options, payments
# ---------------------------------------------------------------------

channels = ["counter", "app"]
payment_methods = ["cash", "card", "app", "points"]

available_member_ids = [
    m["member_id"] for m in members if m["member_id"] not in members_never_order
]
orderable_products = [
    p for p in products if p["product_id"] not in products_never_ordered
]

orders = []
order_lines = []
line_options = []
payments = []

NUM_ORDERS = 1000
order_line_counter = 0
payment_counter = 0

for order_num in range(NUM_ORDERS):
    order_id = f"OR{order_num + 1:05d}"
    order_datetime = random_order_datetime()
    channel = random.choice(channels)

    # about 55% of orders are placed by a member; the rest are guest orders
    # with no member attached, which the scenario allows
    if random.random() < 0.55:
        member_id = random.choice(available_member_ids)
    else:
        member_id = ""

    orders.append({
        "order_id": order_id,
        "order_datetime": order_datetime.isoformat(sep=" "),
        "member_id": member_id,
        "channel": channel,
    })

    # each order has 1 to 4 lines, as the scenario requires at least one
    num_lines = random.randint(1, 4)
    order_total = 0.0

    for _ in range(num_lines):
        product = random.choice(orderable_products)
        quantity = random.randint(1, 3)
        # the scenario says a menu price can change later, so a line keeps
        # the price charged that day; this script does not model price
        # history, so that price is simply today's catalog price
        unit_price = product["price"]

        order_line_counter += 1
        order_line_id = f"OL{order_line_counter:06d}"

        order_lines.append({
            "order_line_id": order_line_id,
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price,
        })
        order_total += quantity * unit_price

        # a line may carry 0, 1 or 2 options, each at most once per line,
        # charged once per unit on the line
        num_options = random.choice([0, 0, 1, 1, 2])
        chosen_options = random.sample(options, num_options) if num_options > 0 else []
        for opt in chosen_options:
            if opt["option_id"] == option_never_used:
                continue  # keep this one unused, on purpose
            line_options.append({
                "order_line_id": order_line_id,
                "option_id": opt["option_id"],
                "unit_price": opt["price"],
            })
            order_total += quantity * opt["price"]

    order_total = round(order_total, 2)

    # split the total across 1 or 2 payments, so payments add up to the
    # order's total, as the scenario requires
    if random.random() < 0.25:
        split = round(order_total * random.uniform(0.3, 0.7), 2)
        amounts = [split, round(order_total - split, 2)]
    else:
        amounts = [order_total]

    for amount in amounts:
        if amount <= 0:
            continue  # a payment is always more than zero
        payment_counter += 1
        payment_id = f"PM{payment_counter:06d}"
        method = random.choice(payment_methods)
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "method": method,
            "amount": amount,
        })

# BROKEN RULE 2, on purpose: "a payment's method is one of cash, card, app, points"
# exactly two rows (0-based row numbers in payments.csv, header excluded)
broken_payment_rows = [10, 500]
for row_index in broken_payment_rows:
    payments[row_index]["method"] = "voucher"

print("BROKEN RULE: method not one of the four allowed values, rows", broken_payment_rows, "of payments.csv")
for row_index in broken_payment_rows:
    print("  ", payments[row_index])

write_csv("orders.csv", ["order_id", "order_datetime", "member_id", "channel"], orders)
write_csv(
    "order_lines.csv",
    ["order_line_id", "order_id", "product_id", "quantity", "unit_price"],
    order_lines,
)
write_csv("line_options.csv", ["order_line_id", "option_id", "unit_price"], line_options)
write_csv("payments.csv", ["payment_id", "order_id", "method", "amount"], payments)

print()
print("Members who joined but never ordered:", sorted(members_never_order))
print("Products never ordered:", sorted(products_never_ordered))
print("Option never used on any line:", option_never_used)
