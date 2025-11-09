-- SQLite-compatible schema for Car Rental System (educational)
PRAGMA foreign_keys = ON;

-- Car classes / categories
CREATE TABLE IF NOT EXISTS car_class (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    daily_rate REAL NOT NULL
);

-- Branches
CREATE TABLE IF NOT EXISTS branch (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT
);

-- Cars
CREATE TABLE IF NOT EXISTS car (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_no TEXT UNIQUE NOT NULL,
    vin TEXT UNIQUE,
    make TEXT,
    model TEXT,
    year INTEGER,
    class_id INTEGER,
    current_branch_id INTEGER,
    status TEXT NOT NULL DEFAULT 'available',
    FOREIGN KEY (class_id) REFERENCES car_class(class_id),
    FOREIGN KEY (current_branch_id) REFERENCES branch(branch_id)
);

-- Customers
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    license_no TEXT UNIQUE,
    address TEXT
);

-- Reservations
CREATE TABLE IF NOT EXISTS reservation (
    res_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    car_id INTEGER,
    branch_id INTEGER,
    start_dt TEXT NOT NULL, -- ISO timestamp as TEXT
    end_dt TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'booked',
    total_amount REAL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id),
    FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
);

-- Payments
CREATE TABLE IF NOT EXISTS payment (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    res_id INTEGER,
    amount REAL NOT NULL,
    method TEXT,
    paid_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (res_id) REFERENCES reservation(res_id)
);

-- Maintenance
CREATE TABLE IF NOT EXISTS maintenance (
    maint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER,
    maint_date TEXT,
    description TEXT,
    cost REAL,
    FOREIGN KEY (car_id) REFERENCES car(car_id)
);
