import os
import psycopg2

from faker import Faker
from dotenv import load_dotenv

load_dotenv()

fake = Faker(seed=0)

# Database connection parameters
dbname = os.getenv("DBNAME")
user = os.getenv("DBUSER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")


# Connect to the PostgreSQL database
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()
vehicles = []

def populate_users(num_records):
    for _ in range(num_records):
        name_user = f'{fake.first_name()} {fake.last_name()}'
        email = fake.email()
        pw = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)        
        telefono = fake.random_int(min=100000000, max=999999999)
        address = fake.address()
        city = fake.city()                

        query = f"""
                    INSERT INTO uber.users (name_user, email, password, phone, address, city, created_at) 
                    VALUES ('{name_user}', '{email}', '{pw}', '{telefono}', '{address}', '{city}', now())
                """
        cursor.execute(query)

def populate_vehicles(num_records):
    for _ in range(num_records):
        license = fake.random_int(min=100000000, max=999999999)
        brand = fake.random_element(elements=('Toyota', 'Chevrolet', 'Ford', 'Nissan', 'Hyundai'))
        line = fake.random_element(elements=('Sedan', 'Hatchback', 'SUV', 'Pickup', 'Coupe'))
        model = fake.random_int(min=2014, max=2024)
        plate = fake.license_plate()
        
        query = f"""
                    INSERT INTO uber.vehicles (vehicle_license, brand, line, model, plate, created_at) 
                    VALUES ('{license}', '{brand}', '{line}', '{model}', '{plate}', now())
                """
        cursor.execute(query)

def populate_drivers(num_records):
    for _ in range(num_records):
        name_driver = f'{fake.first_name()} {fake.last_name()}'
        email = fake.email()
        pw = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        telefono = fake.random_int(min=100000000, max=999999999)
        address = fake.address()
        city = fake.city()
        driver_license = fake.random_int(min=100000000, max=999999999)


        query = f"""
                    INSERT INTO uber.drivers (name_driver, email, password, phone, address, city, driver_license, created_at, vehicle_id) 
                    VALUES ('{name_driver}', '{email}', '{pw}', {telefono}, '{address}', '{city}', {driver_license}, now(), {fake.random_int(min=1, max=num_drivers)})
                """
        
        cursor.execute(query)

def populate_travels(num_records, num_drivers, num_users):
    for _ in range(num_records):
        
        origin = fake.address()
        destination = fake.address()
        start_date_time = fake.date_time_this_year()
        final_date_time = fake.date_time_this_year()
        status = fake.random_element(elements=('Completado', 'Cancelado'))
        
        query = f"""
                    INSERT INTO uber.travels (origin, destination, start_date_time, final_date_time, status, created_at, driver_id, user_id) 
                    VALUES ('{origin}', '{destination}', '{start_date_time}', '{final_date_time}', '{status}', now(), {fake.random_int(min=1, max=num_drivers)}, {fake.random_int(min=1, max=num_users)})
                """
        cursor.execute(query)

def populate_payments(num_records):
    for _ in range(num_records):
        
        method = fake.random_element(elements=('Efectivo', 'Tarjeta'))
        amount = fake.random_element(elements=(10000, 20000, 30000, 40000, 50000, 5000, 7000, 15000))
        status = fake.random_element(elements=('Aprobado', 'Rechazado'))
        
        query = f"""
                    INSERT INTO uber.payments (method_payment, amount, status, created_at, user_id, travel_id, driver_id) 
                    VALUES ('{method}', {amount}, '{status}', now(), {fake.random_int(min=1, max=num_users)}, {fake.random_int(min=1, max=num_travels)}, {fake.random_int(min=1, max=num_drivers)})
                """
        cursor.execute(query)


# Define the number of records to generate
num_users = 1000000
num_vehicles = 200
num_drivers = 200
num_travels = 12000
num_payments = 10200

# Populate CLIENTES, PRODUCTOS, and ORDENES tables
populate_users(num_users)
populate_vehicles(num_vehicles)
populate_drivers(num_drivers)
populate_travels(num_travels, num_drivers, num_users)
populate_payments(num_payments)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
