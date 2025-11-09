# Car Rental Management System (DBMS Project)

This repository contains a minimal Car Rental Management System project suitable for a DBMS assignment.
It includes:
- Database schema (SQLite-compatible) and sample data.
- A simple Streamlit app (`streamlit_app.py`) that demonstrates basic booking/search flows using SQLite.
- `requirements.txt` to install dependencies.

## Contents
- `sql/schema.sql` - Database schema (tables and constraints)
- `sql/sample_data.sql` - Example seed data
- `app/streamlit_app.py` - Simple Streamlit interface demonstrating basic features
- `requirements.txt` - Python dependencies
- `.gitignore`

## How to run (locally)
1. Create a virtual environment and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Initialize the database (SQLite):
   ```
   sqlite3 car_rental.db < sql/schema.sql
   sqlite3 car_rental.db < sql/sample_data.sql
   ```
3. Run the Streamlit app:
   ```
   streamlit run app/streamlit_app.py --server.port 8501
   ```
4. Open the shown local URL (usually http://localhost:8501)

## Notes
- This is a minimal educational project to demonstrate DB design and basic operations.
- Adapt and extend it for more features (user roles, concurrency tests, more reports).

