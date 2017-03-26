import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Customer(Base):
	__tablename__ = 'customer'
	id = Column(Integer, primary_key = True)
	name = Column(String(50))
	email = Column(String(50))
	
class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key = True)
	name = Column(String(50))

class Purchcase(Base):
	__tablename__ = 'purchcase'
	id = Column(Integer, primary_key = True)
	customer_id = Column(Integer, ForeignKey('customer.id'))
	item_id = Column(Integer, ForeignKey('item.id'))
	customer = relationship(Customer)
	item = relationship(Item)



engine = create_engine("sqlite:///customers.db")
Base.metadata.create_all(engine)