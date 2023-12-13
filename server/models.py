from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationship
    hotel_customers = db.relationship('HotelCustomer', back_populates='hotel')
    # add serialization rules
    serialize_rules = ('-hotel_customers.hotel',)
    def __repr__(self):
        return f'<Hotel {self.name}>'


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # add relationship
    hotel_customers = db.relationship('HotelCustomer', back_populates='customer')
    # add serialization rules
    serialize_rules = ('-hotel_customers.customer',)
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'


class HotelCustomer(db.Model, SerializerMixin):
    __tablename__ = 'hotel_customers'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # add relationships
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    hotel = db.relationship('Hotel', back_populates='hotel_customers')

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='hotel_customers')

    # add serialization rules
    serialize_rules = ('-hotel.hotel_customers', '-customer.hotel_customers')
    # add validation
    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError('rating must be between 1 and 5')
        return value
    def __repr__(self):
        return f'<HotelCustomer ★{self.rating}>'
