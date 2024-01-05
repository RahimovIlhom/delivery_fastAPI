from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    fullname = Column(String(30))
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')  # one to many

    def __repr__(self):
        return f"user: {self.username}"


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    price = Column(Integer)
    orders = relationship('Order', back_populates='product')  # one to many

    def __repr__(self):
        return f"product: {self.name} - {self.price}"


class Order(Base):
    STATUS_CHOISE = (
        ('CREATED', 'created'),
        ('PANDING', 'panding'),
        ('ON_WAY', 'on_way'),
        ('DELIVERED', 'delivered'),
    )
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))  # many to one
    user = relationship('User', back_populates='orders')
    product_id = Column(Integer, ForeignKey('product.id'))  # many to one
    product = relationship('Product', back_populates='orders')
    quantity = Column(Integer, default=1)
    status = Column(String(20), ChoiceType(choices=STATUS_CHOISE), default='CREATED')

    def __repr__(self):
        return f"order: {self.user.__repr__()}"
