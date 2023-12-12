import pytest
from app import app
from models import db, Hotel, Customer, HotelCustomer
from faker import Faker


class TestHotelCustomer:
    '''Class HotelCustomer in models.py'''

    def test_rating_between_1_and_5(self):
        '''requires rating between 1 and 5.'''

        with app.app_context():

            customer = Customer(first_name="Joelle", last_name="Sams")
            hotel = Hotel(name="The Plaza")
            db.session.add(customer)
            db.session.add(hotel)
            db.session.commit()

            hotel_customer_1 = HotelCustomer(hotel_id=hotel.id, customer_id=customer.id, rating=1)
            hotel_customer_2 = HotelCustomer(hotel_id=hotel.id, customer_id=customer.id, rating=5)
            db.session.add(hotel_customer_1)
            db.session.add(hotel_customer_2)
            db.session.commit()

    def test_rating_too_low(self):
        '''requires rating between 1 and 5 and fails when rating is 0.'''

        with app.app_context():

            with pytest.raises(ValueError):
                customer = Customer(first_name="Hammond", last_name="Devi")
                hotel = Hotel(name="Algonquin Hotel")
                db.session.add(customer)
                db.session.add(hotel)
                db.session.commit()

                hotel_customer = HotelCustomer(
                    hotel_id=hotel.id, customer_id=customer.id, rating=0)
                db.session.add(hotel_customer)
                db.session.commit()

    def test_rating_too_high(self):
        '''requires rating between 1 and 5 and fails when rating is 6.'''

        with app.app_context():

            with pytest.raises(ValueError):
                customer = Customer(
                    first_name="Emma", last_name="Montana")
                hotel = Hotel(name="Hotel Edison Times Square")
                db.session.add(customer)
                db.session.add(hotel)
                db.session.commit()

                hotel_customer = HotelCustomer(
                    hotel_id=hotel.id, customer_id=customer.id, rating=6)
                db.session.add(hotel_customer)
                db.session.commit()
