from database import engine, Base
from models import User, Product, Order

Base.metadata.create_all(bind=engine)
