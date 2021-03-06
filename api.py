from flask import Flask
from flask import  jsonify, request
from recommender.recommender import Recommender
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Customer, Item, Purchcase
import numpy as np

app = Flask(__name__)
engine = create_engine('sqlite:///customers.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
buffer = 2
events = 0

# -------------------------- HELPERS ---------------------
def getPurchasedItems(customer_name):
	customer = session.query(Customer).filter(Customer.name == customer_name)[:1]
	if customer:
		items_list = []
		purchases = session.query(Purchcase).filter(Purchcase.customer_id == customer[0].id)
		[items_list.append(item.item_id) for item in purchases]
		return items_list
	else:
		return None

def countItems():
	return session.query(Item).count()

# TODO: handle users without items
def buildPurchcaseVector(customer_name):
	total_items = countItems() +1 # questo ancora mi e' molto oscuro, ma funziona
	v = np.zeros(total_items)
	purchases = getPurchasedItems(customer_name)
	if purchases:
		v[purchases] = 1
		return v[1:]
	else:
		return None

def buildGlobalMatrix():
	vectors = []
	customers = session.query(Customer).all()
	for customer in customers:
		v = buildPurchcaseVector(customer.name)
		vectors.append(v)
	return np.array(vectors)

def insertEvent():
	global events
	events = events +1
	if events >= buffer:
		global matrix
		matrix = buildGlobalMatrix()
		global r 
		r = Recommender(matrix)
		print "Updating matrix"

# ------------------------------------------------------
matrix = buildGlobalMatrix() # build the initial matrix
r = Recommender(matrix) # pass the matrix to the model


@app.route('/api/new/customer/<string:name>')
def addCustomer(name):
	customer = Customer(name = name)
	session.add(customer)
	session.commit()
	insertEvent()
	response = {
		"status" : "insert ok"
	}
	return jsonify(response)

@app.route('/api/new/item/<string:name>')
def addItem(name):
	item = Item(name = name)
	session.add(item)
	session.commit()
	insertEvent()
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
		insertEvent()
		response = {
		"status" : "insert ok"
		}
		return jsonify(response)	
	else:
		return jsonify({"error" : "invalid combination of customer/item"})


@app.route('/api/get/items/<string:customer_name>')
def getItemsFromUser(customer_name):
	items = getPurchasedItems(customer_name)
	if items:
		return jsonify({"response": items})
	else:
		return jsonify({"error": "no customer found"})


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

@app.route('/api/get/matrix')
def getOldMatrix():
	return jsonify({"response": str(matrix)})

@app.route('/api/update_matrix')
def updateMatrix():
	global matrix
	matrix = buildGlobalMatrix()
	global r
	r = Recommender(matrix)
	return jsonify({"response": "Matrix updated"})

@app.route('/api/predict/<string:customer_name>')
def predict(customer_name):
	vector = buildPurchcaseVector(customer_name)

	if len(vector)>0:
		prediction = r.vector_model(vector)
		indices = zip(*([(i+1,x) for (i,x) in enumerate(prediction) if x != 0]))[0]
		products = session.query(Item).filter(Item.id.in_(indices)).all()
		return jsonify({"response": str([p.name for p in products])})
	else:
		return jsonify({"error": "No customer found"})	


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)