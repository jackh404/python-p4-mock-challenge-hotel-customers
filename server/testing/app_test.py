from models import Hotel, HotelCustomer, Customer
from app import app, db
from faker import Faker


class TestApp:
    '''Flask application in app.py'''

    def test_hotels(self):
        """retrieves hotels with GET request to /hotels"""
        with app.app_context():
            hotel1 = Hotel(name="The Plaza")
            hotel2 = Hotel(name="Algonquin Hotel")
            db.session.add_all([hotel1, hotel2])
            db.session.commit()

            hotels = Hotel.query.all()

            response = app.test_client().get('/hotels')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert [hotel['id'] for hotel in response] == [
                hotel.id for hotel in hotels]
            assert [hotel['name'] for hotel in response] == [
                hotel.name for hotel in hotels]
            for hotel in response:
                assert 'hotel_customers' not in hotel

    def test_hotels_id(self):
        '''retrieves one hotel using its ID with GET request to /hotels/<int:id>.'''

        with app.app_context():
            hotel = Hotel(name="Hotel Edison Times Square")
            db.session.add(hotel)
            db.session.commit()

            response = app.test_client().get(
                f'/hotels/{hotel.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json
            assert response['id'] == hotel.id
            assert response['name'] == hotel.name
            assert 'hotel_customers' in response

    def test_returns_404_if_no_hotel_to_get(self):
        '''returns an error message and 404 status code with GET request to /hotels/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/hotels/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error')
            assert response.status_code == 404

    def test_deletes_hotel_by_id(self):
        '''deletes hotel with DELETE request to /hotels/<int:id>.'''

        with app.app_context():
            hotel = Hotel(name="Hotel Elysee")
            db.session.add(hotel)
            db.session.commit()

            response = app.test_client().delete(
                f'/hotels/{hotel.id}')

            assert response.status_code == 204

            result = Hotel.query.filter(
                Hotel.id == hotel.id).one_or_none()
            assert result is None

    def test_returns_404_if_no_hotel_to_delete(self):
        '''returns an error message and 404 status code with DELETE request to /hotels/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/hotels/0')
            assert response.status_code == 404
            assert response.json.get('error') == "Hotel not found"

    def test_customers(self):
        """retrieves customers with GET request to /customers"""
        with app.app_context():
            customer1 = Customer(first_name="Steven", last_name="Connor")
            customer2 = Customer(first_name="Abdul", last_name="Fox")

            db.session.add_all([customer1, customer2])
            db.session.commit()

            response = app.test_client().get('/customers')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            customers = Customer.query.all()

            assert [customer['id'] for customer in response] == [
                customer.id for customer in customers]
            assert [customer['first_name'] for customer in response] == [
                customer.first_name for customer in customers]
            assert [customer['last_name'] for customer in response] == [
                customer.last_name for customer in customers]
            for customer in response:
                assert 'hotel_customers' not in customer

    def test_creates_hotel_customers(self):
        '''creates one hotel_customer using a customer_id, hotel_id, and rating with a POST request to /hotel_customers.'''

        with app.app_context():
            customer = Customer(first_name="Roderick", last_name="Spencer")
            hotel = Hotel(name="Waldorf Astoria")
            db.session.add(customer)
            db.session.add(hotel)
            db.session.commit()

            # delete if existing in case rating differs
            hotel_customer = HotelCustomer.query.filter_by(
                customer_id=customer.id, hotel_id=hotel.id).one_or_none()
            if hotel_customer:
                db.session.delete(hotel_customer)
                db.session.commit()

            response = app.test_client().post(
                '/hotel_customers',
                json={
                    "rating": 3,
                    "customer_id": customer.id,
                    "hotel_id": hotel.id,
                }
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            response = response.json
            assert response['rating'] == 3
            assert response['customer_id'] == customer.id
            assert response['hotel_id'] == hotel.id
            assert response['id']
            assert response['customer']
            assert response['hotel']

            query_result = HotelCustomer.query.filter(
                HotelCustomer.hotel_id == hotel.id, HotelCustomer.customer_id == customer.id).first()
            assert query_result.rating == 3

    def test_400_for_validation_error(self):
        '''returns a 400 status code and error message if a POST request to /hotel_customers fails.'''

        with app.app_context():
            customer = Customer(first_name="Harley", last_name="Stark")
            hotel = Hotel(name="The Ritz Carlton")
            db.session.add(customer)
            db.session.add(hotel)
            db.session.commit()

            # price not in 1..5
            response = app.test_client().post(
                '/hotel_customers',
                json={
                    "rating": 0,
                    "customer_id": customer.id,
                    "hotel_id": hotel.id,
                }
            )

            assert response.status_code == 400
            assert response.json['errors'] == ["validation errors"]

            response = app.test_client().post(
                '/hotel_customers',
                json={
                    "rating": 6,
                    "customer_id": customer.id,
                    "hotel_id": hotel.id,
                }
            )

            assert response.status_code == 400
            assert response.json['errors'] == ["validation errors"]
