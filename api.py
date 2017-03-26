from flask import Flask
from flask import  jsonify, request
from recommender.recommender import Recommender
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer, Item, Purchcase
import numpy as np

app = Flask(__name__)
engine = create_engine('sqlite:///customers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/api/new/customer/<string:name>')
def addCustomer(name):
	customer = Customer(name = name)
	session.add(customer)
	session.commit()
	response = {
		"status" : "insert ok"
	}
	return jsonify(response)

@app.route('/api/new/item/<string:name>')
def addItem(name):
	item = Item(name = name)
	session.add(item)
	session.commit()
	response = {
		"status" : "insert ok"
	}
	return jsonify(response)

@app.route('/api/new/purchcase/<string:customer_name>/<string:item_name>')
def addPurchase(customer_name, item_name):
	customer = session.query(Customer).filter(Customer.name == customer_name)[:1]
	item = session.query(Item).filter(Item.name == item_name)[:1]

	if customer and item:
		purchcase = Purchcase(customer_id = customer[0].id, item_id = item[0].id)
		session.add(purchcase)
		session.commit()
		response = {
		"status" : "insert ok"
		}
		return jsonify(response)	
	else:
		return jsonify({"error" : "invalid combination of customer/item"})

def getPurchasedItems(customer_name):
	customer = session.query(Customer).filter(Customer.name == customer_name)[:1]
	if customer:
		items_list = []
		purchases = session.query(Purchcase).filter(Purchcase.customer_id == customer[0].id)
		[items_list.append(item.item_id) for item in purchases]
		return items_list
	else:
		return None

@app.route('/api/get/items/<string:customer_name>')
def getItemsFromUser(customer_name):
	items = getPurchasedItems(customer_name)
	if items:
		return jsonify({"response": items})
	else:
		return jsonify({"error": "no customer found"})

def countItems():
	return session.query(Item).count()

def buildPurchcaseVector(customer_name):
	total_items = countItems()
	v = np.zeros(total_items)
	purchases = getPurchasedItems(customer_name)
	if purchases:
		v[purchases] = 1
		return v[1:]
	else:
		return None

@app.route('/api/get/vector/<string:customer_name>')
def getUserVector(customer_name):
	v = buildPurchcaseVector(customer_name)
	try:
		if len(v) > 0:
			return jsonify({"response" : str(v)})
		else:
			return jsonify({"error" : ""})
	except:
		return jsonify({"error" : ""})

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)