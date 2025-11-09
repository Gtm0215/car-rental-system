import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

DB = 'car_rental.db'

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

st.set_page_config(page_title='Car Rental Demo', layout='wide')
st.title('Car Rental System - Demo')

menu = ['Search Available Cars', 'Make Reservation', 'View Reservations', 'Customers', 'Admin']
choice = st.sidebar.selectbox('Menu', menu)

conn = get_conn()
c = conn.cursor()

if choice == 'Search Available Cars':
    st.header('Search available cars by date range')
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input('Start date', value=datetime.today())
    with col2:
        end = st.date_input('End date', value=datetime.today())
    if st.button('Search'):
        start_dt = datetime.combine(start, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
        end_dt = datetime.combine(end, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
        query = """SELECT car_id, registration_no, make, model, year, status
        FROM car
        WHERE status = 'available'
        AND car_id NOT IN (
          SELECT car_id FROM reservation
          WHERE status IN ('booked','active')
          AND NOT (end_dt <= ? OR start_dt >= ?)
        )"""
        df = pd.read_sql_query(query, conn, params=(start_dt, end_dt))
        st.write(f'Available cars from {start_dt} to {end_dt}:')
        st.dataframe(df)

elif choice == 'Make Reservation':
    st.header('Make a Reservation')
    customers = pd.read_sql_query('SELECT customer_id, full_name FROM customer', conn)
    cars = pd.read_sql_query('SELECT car_id, registration_no, make, model FROM car WHERE status = "available"', conn)
    if customers.empty:
        st.info('No customers found. Add a customer first in "Customers" tab.')
    else:
        cust = st.selectbox('Select Customer', customers['full_name'])
        cust_id = customers[customers['full_name']==cust]['customer_id'].iloc[0]
        car_choice = st.selectbox('Select Car', cars['registration_no'] + ' - ' + cars['make'] + ' ' + cars['model'])
        car_id = int(cars.iloc[cars.index[cars['registration_no'] == car_choice.split(' - ')[0]][0]]['car_id'])
        start = st.date_input('Start date', value=datetime.today(), key='res_start')
        end = st.date_input('End date', value=datetime.today(), key='res_end')
        if st.button('Reserve'):
            start_dt = datetime.combine(start, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.combine(end, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
            # simple overlap check
            overlap = c.execute("""SELECT COUNT(*) FROM reservation
                WHERE car_id = ? AND status IN ('booked','active')
                AND NOT (end_dt <= ? OR start_dt >= ?)""", (car_id, start_dt, end_dt)).fetchone()[0]
            if overlap > 0:
                st.error('Selected car is not available for given range.')
            else:
                c.execute("INSERT INTO reservation (customer_id, car_id, branch_id, start_dt, end_dt, status, total_amount) VALUES (?,?,?,?,?,?,?)",
                          (cust_id, car_id, 1, start_dt, end_dt, 'booked', 0.0))
                c.execute("UPDATE car SET status = 'reserved' WHERE car_id = ?", (car_id,))
                conn.commit()
                st.success('Reservation created successfully.')

elif choice == 'View Reservations':
    st.header('Reservations')
    df = pd.read_sql_query('SELECT r.res_id, c.full_name, ca.registration_no, r.start_dt, r.end_dt, r.status FROM reservation r LEFT JOIN customer c ON r.customer_id=c.customer_id LEFT JOIN car ca ON r.car_id=ca.car_id', conn)
    st.dataframe(df)

elif choice == 'Customers':
    st.header('Customers')
    if st.checkbox('Show customers'):
        df = pd.read_sql_query('SELECT * FROM customer', conn)
        st.dataframe(df)
    st.subheader('Add new customer')
    name = st.text_input('Full name')
    phone = st.text_input('Phone')
    email = st.text_input('Email')
    license_no = st.text_input('License No')
    address = st.text_area('Address')
    if st.button('Add Customer'):
        if not name:
            st.error('Name required')
        else:
            c.execute('INSERT INTO customer (full_name, phone, email, license_no, address) VALUES (?,?,?,?,?)', (name, phone, email, license_no, address))
            conn.commit()
            st.success('Customer added.')

else:
    st.header('Admin (Basic)')
    st.subheader('Cars')
    cars = pd.read_sql_query('SELECT * FROM car', conn)
    st.dataframe(cars)
    st.subheader('Car Classes')
    st.dataframe(pd.read_sql_query('SELECT * FROM car_class', conn))
    st.subheader('Branches')
    st.dataframe(pd.read_sql_query('SELECT * FROM branch', conn))

# close connection on exit
conn.close()
