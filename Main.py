from PopulateDB import addArticlesDB, addBooksDB
import UseCases
from pynytimes import NYTAPI
from datetime import datetime, date
from pymongo import MongoClient, errors
import sys
import json
import requests
nyt = NYTAPI("qsPCmSV09wV4AbCCaJmXFPxo3nCwGtbU")
myclient = MongoClient("mongodb://localhost:27017/")
db = myclient["nyt"]
article = db["article"]
book = db["book"]
LIMIT = int(input('Limit output to __ documents:\t'))

def main_menu():
    options = """
    **************************************************************************
    1. Add article
    2. Get articles given a keyword value and rank >= number
    3. Find articles with a word count >= number
    4. Get the total word count of all articles by section name
    5. Read the abstracts based on a given keyword value
    6. Find abstracts that contain an expression
    7. Find other articles written by a person
    8. Find articles that have multimedia and are a certain type of material
    9. Get metadata of an article given an URL
    10. Update the document type for 1 article
    11. Update the keyword value for all articles
    12. Update the read status for an article
    13. Delete 1 article given the section name
    14. Delete all articles with a certain keyword value
    15. Delete 1 article where the word count < number
    **************************************************************************"""
    print(options)
    selected = str(input("Select an operation:\t"))
    if selected == '1':
        article_doc = UseCases.addArticle()
        db.article.insert_one(article_doc)
        print(article_doc)
    elif selected == '2':
        query = UseCases.findArticlesWKeyValueRank()
        results = db.article.find({'keywords': {'$elemMatch':query}}).limit(LIMIT)
        for r in results:
            print(r)
    else:
        print("Good-bye!")
        myclient.close() #close connection
        exit()
        
    main_menu()
    
if __name__ == "__main__": 
    db_size_bytes = db.command("dbstats")['storageSize']
    if db_size_bytes < 1000000000:
        article.delete_many({})
        #book.delete_many({})
        addArticlesDB(myclient, db, article, nyt)
    #addBooksDB(myclient, db, book, nyt)
    print("This application displays articles from 2007-2020(inclusive)")
    main_menu()
