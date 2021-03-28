from nyt2 import addArticles, addBooks
from pynytimes import NYTAPI
from datetime import datetime, date
from pymongo import MongoClient, errors
import sys
import json
import requests

def main_menu():
    #while input doesn't equal q or Q:
        #display query options
        #take input
        #call corresponding function
    print("Good-bye!")
    myclient.close() #close connection
if __name__ == "__main__": 
    nyt = NYTAPI("qsPCmSV09wV4AbCCaJmXFPxo3nCwGtbU")
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["nyt"]
    article = db["article"]
    book = db["book"]
    db_size_bytes = db.command("dbstats")['storageSize']
    if db_size_bytes < 1000000000:
        article.delete_many({})
        book.delete_many({})
        addArticles(myclient, db, article, nyt)
    addBooks(myclient, db, book, nyt)
    main_menu()
