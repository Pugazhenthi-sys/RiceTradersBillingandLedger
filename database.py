import sqlite3

# ==========================================
# DATABASE CONNECTION
# ==========================================

conn = sqlite3.connect(
    "billing_system.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# CUSTOMERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT UNIQUE
)
""")

# ==========================================
# TRANSACTIONS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    type TEXT,

    amount REAL,

    description TEXT,

    date TEXT,

    FOREIGN KEY(customer_id)
    REFERENCES customers(id)
)
""")

# ==========================================
# INCOME TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS income
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    bill_no INTEGER,

    profit REAL,

    date TEXT
)
""")

# ==========================================
# SALES REGISTER TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_register
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,
    bill_no INTEGER,

    particular TEXT,

    bags INTEGER,
    bag_size REAL,
    weight REAL,

    purchase_rate REAL,
    selling_rate REAL,

    lorry_rent REAL,

    actual_cost REAL,
    selling_amount REAL,

    profit REAL,

    date TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL
)
""")
# ==========================================
# GLOBAL BILL COUNTER
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_counter
(
    id INTEGER PRIMARY KEY,
    current_bill_no INTEGER
)
""")

cursor.execute("""
INSERT OR IGNORE INTO bill_counter
(id, current_bill_no)
VALUES
(1, 0)
""")
# ==========================================
# BILL STATUS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_status
(
    bill_no INTEGER PRIMARY KEY,

    customer_name TEXT,
    particular TEXT,

    bill_amount REAL,
    paid_amount REAL DEFAULT 0,

    profit REAL,

    status TEXT DEFAULT 'Pending'
)
""")
conn.commit()