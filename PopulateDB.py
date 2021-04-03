from datetime import datetime, date
from pymongo import MongoClient, errors
import requests
def addArticlesDB(myclient, mydb, mycol, nyt):
    mycol.delete_many({})
    article_err = 0
    for y in range(2007,2021):
        for m in range(1,13):
            try:
                data = nyt.archive_metadata(date = datetime(y, m, 1))
                map(lambda x: x.pop('multimedia'), data)
                mycol.insert_many(data, ordered=False, bypass_document_validation=True)
            except errors.BulkWriteError as e:
                #print (e.details['writeErrors'])
                article_err += 1
        print(y)
    print(f"Done inserting documents. {article_err} article(s) unable to be inserted.")
def addBooksDB(myclient, mydb, mycol, nyt):
    mycol.delete_many({})
    book_err = 0
    reviews = requests.get("https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=qsPCmSV09wV4AbCCaJmXFPxo3nCwGtbU")
    lst = reviews.json()['results']
    list_names = [d['list_name_encoded'] for d in lst]
    for i in range(len(list_names)):
        books = nyt.best_sellers_list(name = list_names[i])
        try:
            mycol.insert_many(list(books), ordered=False, bypass_document_validation=True)
        except errors.BulkWriteError as e:
            #print (e.details['writeErrors'])
            book_err += 1
    print(f"Done inserting book documents. {book_err} book(s) unable to be inserted.")