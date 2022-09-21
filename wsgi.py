from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from apis.books import HelloWorld, SearchBooks, Transactions,ListOfPeople,TotalRentGen, PersonCollection, BetweenDateRange
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app)

CORS(app)


# apis
api.add_resource(HelloWorld, '/')
api.add_resource(SearchBooks, '/search-book')

api.add_resource(Transactions, "/book-status")

api.add_resource(ListOfPeople, "/people-list")
api.add_resource(TotalRentGen, "/total-rent")
api.add_resource(PersonCollection, "/person-collection")
api.add_resource(BetweenDateRange, "/between-dates")


if __name__ == '__main__':
    app.run(debug=True)