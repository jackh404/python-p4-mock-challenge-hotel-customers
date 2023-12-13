#!/usr/bin/env python3

from models import db, Hotel, HotelCustomer, Customer
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
@app.route('/')
def index():
    return '<h1>Mock Code challenge</h1>'

class Hotels(Resource):
    def get(self):
        hotels = [hotel.to_dict(only=('id', 'name')) for hotel in Hotel.query.all()]
        return make_response(hotels, 200)
api.add_resource(Hotels, '/hotels')

class HotelById(Resource):
    def get(self, id):
        hotel = Hotel.query.filter_by(id=id).first()
        if not hotel:
            return make_response({'error': 'Hotel not found'}, 404)
        return make_response(hotel.to_dict(), 200)
    def delete(self,id):
        hotel = Hotel.query.filter_by(id=id).first()
        if not hotel:
            return make_response({'error': 'Hotel not found'}, 404)
        db.session.delete(hotel)
        db.session.commit()
        return make_response('', 204)
api.add_resource(HotelById, '/hotels/<int:id>')

class Customers(Resource):
    def get(self):
        customers = [customer.to_dict(only=('id', 'first_name', 'last_name')) for customer in Customer.query.all()]
        return make_response(customers, 200)
api.add_resource(Customers, '/customers')
class HotelCustomers(Resource):
    def post(self):
        data = request.get_json()
        try:
            hotel_customer = HotelCustomer(
                rating=data['rating'],
                customer_id=data['customer_id'],
                hotel_id=data['hotel_id'],
            )
            db.session.add(hotel_customer)
            db.session.commit()
            return make_response(hotel_customer.to_dict(), 201)
        except Exception as e:
            return make_response({'errors':['validation errors']}, 400)
api.add_resource(HotelCustomers, '/hotel_customers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
