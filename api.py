from flask import Flask
from flask import  jsonify, request
from recommender import Recommender


app = Flask(__name__)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)