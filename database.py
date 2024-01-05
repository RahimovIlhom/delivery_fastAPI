from sqlalchemy import engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = engine.create_engine('postgresql://postgres:ilhomjon@localhost/delivery_db',
                              echo=True)

Base = declarative_base()
session = sessionmaker()
