from flask_restful import Resource, Api
from flask import  jsonify, request
from DB.Mongo import MongoAPI
import json
from Helper.utils import checkForSamePerson, getDateObject
from dateutil import parser

class HelloWorld(Resource):
    def get(self):
        return jsonify("good.....")

class SearchBooks(Resource):
    def get(self):
        book_q = request.args.get('book_q', None)
        min_rent_q = request.args.get('min_rent_q', 0)
        max_rent_q = request.args.get('max_rent_q', None)
        category_q = request.args.get('category_q', None)

        query = {
            }
        
        if book_q != None:

            query["name"] = { "$regex": book_q }

        if max_rent_q != None:          
  
            query["rent"] ={ "$gt": int(min_rent_q), "$lt": int(max_rent_q)}
        
        if category_q != None:
            query["category"] = { "$regex": category_q}
          

        data = MongoAPI('bookdetails').findall(query)

        return data,200

class Transactions(Resource):

    def post(self):
        try:
            book_name = request.args['book_name']
            person_name = request.args['person_name']
            issued_date = request.args['issued_date']
        except:
            return {"msg" : "missing key-pair"}, 401
        
        book_q = {
            "name" : book_name
        }
        book_obj = MongoAPI('bookdetails').findall(book_q)
        
        if not book_obj:
            return {"msg" : "book not found"}, 404
        
        book_id = book_obj[0]['_id']

        is_same_person = checkForSamePerson(book_id, person_name)
        if is_same_person == True:
            trns = {"book_id":book_id, "person": person_name, "book_name": book_name, "isIssued": True, "issuedDate": getDateObject(issued_date), "returned_date" : ""}
            MongoAPI('transactions').insertTransaction(trns)
            return {"msg": f"{book_name} Issued to {person_name}"}, 201

        elif is_same_person == "update":
            trns_query = {
                "book_id" : book_id,
                "person": person_name
                    }

            to_set = {
                    '$set': {
                        "isIssued":True,
                        "issuedDate": getDateObject(issued_date)
                    }
                }
           
            MongoAPI('transactions').updateTransaction(trns_query, to_set)
            return {"msg": f"{book_name} Issued to {person_name}"}, 202

        return {"msg": f"{book_name} already Issued to {person_name}"}, 401

    def put(self):
        
        try:
            book_name = request.args['book_name']
            person_name = request.args['person_name']
            returned_date = request.args['returned_date']
        except:
            return {"msg" : "missing key-pair"}, 401
        
        book_q = {
            "name" : book_name
        }
        book_obj = MongoAPI('bookdetails').findall(book_q)
      
        if not book_obj:
            return {"msg" : "book not found"}, 404
        
        book_id = book_obj[0]['_id']

        trns_query = {
            "book_id" : book_id,
            "person": person_name
        }

        to_set = {
                '$set': {
                    "isIssued":False,
                    "returned_date": getDateObject(returned_date)
                }
            }

        res = MongoAPI('transactions').updateTransaction(trns_query ,to_set)

        if res:
            dates = MongoAPI('transactions').findall(trns_query)[0]
            rent = (dates['returned_date'] - dates['issuedDate']).days * book_obj[0]['rent']
            return {"msg": f"{book_name} returned by {person_name}", "Payable Rent" : f"Rs.{rent}"}, 201
        
        return {"msg": f"No record found for {person_name}"}, 404


class ListOfPeople(Resource):

    def get(self):
        try:
            book_name = request.args['book_name']
        except:
            return {"msg" : "missing key-pair"}, 401
        
        book_q = {
            "name" : book_name
        }
        book_obj = MongoAPI('bookdetails').findall(book_q)
      
        if not book_obj:
            return {"msg" : "book not found"}, 404

        book_id = book_obj[0]['_id']
        trns_q = {
            "book_id" : book_id
        }

        all_trns = MongoAPI('transactions').findall(trns_q)
        list_of_people = []
        for i in all_trns:
            if i['isIssued']:
                list_of_people.append(i['person'])
        
        return {"total count" : len(list_of_people),"data" : list_of_people}, 200

class TotalRentGen(Resource):

    def get(self):
        try:
            book_name = request.args['book_name']
           
        except:
            return {"msg" : "missing key-pair"}, 401

        book_q = {
            "name" : book_name
        }
        book_obj = MongoAPI('bookdetails').findall(book_q)
      
        if not book_obj:
            return {"msg" : "book not found"}, 404

        book_id = book_obj[0]['_id']
        trns_q = {
            "book_id" : book_id
        }

        all_trns = MongoAPI('transactions').findall(trns_q)
        total_rent = 0
        for i in all_trns:
            if i['isIssued'] == False:
                rent = (i['returned_date'] - i['issuedDate']).days * book_obj[0]['rent']
                total_rent += rent
        
        return {"name" : book_name, "total rent" : f'Rs.{total_rent}'}, 200

class PersonCollection(Resource):

    def get(self):
        try:
            person_name = request.args['person_name']
           
        except:
            return {"msg" : "missing key-pair"}, 401
        
        person_q = {
            "person" : person_name
        }

        all_books = MongoAPI('transactions').findall(person_q)
        list_of_books = []
        for i in all_books:
            list_of_books.append(i['book_name'])

        return {"name" : person_name, "data" : list_of_books}, 200

class BetweenDateRange(Resource):

    def get(self):
        try:
            start = request.args['fromDate']
            end = request.args['toDate']
        except:
            return {"msg" : "missing key-pair"}, 401

        date_q = {
            "issuedDate": { 
                        '$gt': getDateObject(start),
                        '$lt': getDateObject(end)
                    }
        }

        issue_in_range = MongoAPI('transactions').findall(date_q)

        books_list = []
        for i in issue_in_range:
            details = {
                "book" : i['book_name'],
                "issued on" :  str(i['issuedDate'].date()),
                "status" : "issued" if i['isIssued'] is True else "returned"
            }
            books_list.append(details)
        
        return {"data" : books_list}, 200
