from datetime import datetime, date
from pymongo import MongoClient, errors
import requests
def addArticlesDB(myclient, mydb, mycol, nyt):  
    article_err = 0
    for y in range(2014,2021):
        for m in range(1,13):
            try:
                print(m)
                data = nyt.archive_metadata(date = datetime(y, m, 1))
                mycol.insert_many(data, ordered=False, bypass_document_validation=True)
            except errors.BulkWriteError:
                #print (e.details['writeErrors'])
                article_err += 1
        print(y)
    print(f"Done inserting documents. {article_err} month(s) of articles unable to be inserted.")