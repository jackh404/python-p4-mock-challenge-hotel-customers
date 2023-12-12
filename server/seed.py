#!/usr/bin/env python3

from app import app
from models import db, Hotel, Customer, HotelCustomer

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Customer.query.delete()
    Hotel.query.delete()
    HotelCustomer.query.delete()

    print("Creating hotels...")
    hotel_1 = Hotel(name="Wyndham Resort")
    hotel_2 = Hotel(name="Disney World Resort")
    hotel_3 = Hotel(name="The Chanler at Cliff Walk")
    hotels = [hotel_1, hotel_2, hotel_3]

    print("Creating customers...")

    customer_1 = Customer(first_name="Alice", last_name="Baker")
    customer_2 = Customer(first_name="Bob", last_name="Cooper")
    customer_3 = Customer(first_name="Collin", last_name="Davidson")
    customers = [customer_1, customer_2, customer_3]

    print("Creating hotel_customers...")

    hotel_customer_1 = HotelCustomer(hotel=hotel_1, customer=customer_1, rating=5)
    hotel_customer_2 = HotelCustomer(hotel=hotel_2, customer=customer_2, rating=4)
    hotel_customer_3 = HotelCustomer(hotel=hotel_3, customer=customer_3, rating=1)
    hotel_customers = [hotel_customer_1, hotel_customer_2, hotel_customer_3]
    db.session.add_all(hotels)
    db.session.add_all(customers)
    db.session.add_all(hotel_customers)
    db.session.commit()

    print("Seeding done!")
