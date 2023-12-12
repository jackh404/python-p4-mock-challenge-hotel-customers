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

    # add serialization rules

    def __repr__(self):
        return f'<Hotel {self.name}>'


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # add relationship

    # add serialization rules

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'


class HotelCustomer(db.Model, SerializerMixin):
    __tablename__ = 'hotel_customers'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # add relationships

    # add serialization rules

    # add validation

    def __repr__(self):
        return f'<HotelCustomer ★{self.rating}>'
