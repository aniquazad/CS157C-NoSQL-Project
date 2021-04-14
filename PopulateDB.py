from datetime import datetime, date
from pymongo import MongoClient, errors
import requests
"""
    This function gets all of the articles in a given range of years (2008-2020) and
    adds it to the specified collection
"""
def addArticlesDB(myclient, mydb, mycol, nyt):  
    article_err = 0 # keeps track of how many months were unable to get inserted
    #year range
    for y in range(2008,2021):
        #month range
        for m in range(1,13):
            try:
                #print(m)
                #gets all of the articles in YYYY/MM
                data = nyt.archive_metadata(date = datetime(y, m, 1))
                #adds it to collections
                mycol.insert_many(data, ordered=False, bypass_document_validation=True)
            except errors.BulkWriteError:
                #print (e.details['writeErrors'])
                article_err += 1
        print(y)
    print(f"Done inserting documents. {article_err} month(s) of articles unable to be inserted.")