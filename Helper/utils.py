from DB.Mongo import MongoAPI
import datetime

def checkForSamePerson(book_id, person_name):
    book_obj = {
        "book_id": book_id,
        "person": person_name
    }
    res = MongoAPI("transactions").findall(book_obj)
    if not res:
        return True

    if res[0]["isIssued"] == False:
        return "update"
    
    return False

def getDateObject(date_str):
    format_str = '%d/%m/%Y'
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    return datetime_obj