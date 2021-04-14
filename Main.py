from PopulateDB import addArticlesDB
import UseCases
from pynytimes import NYTAPI
from datetime import datetime, date
from pymongo import MongoClient, errors, ASCENDING, DESCENDING
import sys
import json
import requests

nyt = NYTAPI("qsPCmSV09wV4AbCCaJmXFPxo3nCwGtbU")
myclient = MongoClient("mongodb://localhost:27018/", w=1,readPreference="primaryPreferred")
#myclient = MongoClient("mongodb://localhost:27018/")
print(myclient)
db = myclient["nyt"]
article = db["article"]
LIMIT = int(input('Limit output to __ documents:\t'))

"""
    This function displays the main menu and allows users to choose from options
"""
def main_menu():
    options = """
    **************************************************************************
    1. Add article
    2. Get articles given a keyword value and rank >= number
    3. Find articles with a word count >= number
    4. Get the total word count of all articles by subsection name given a section
    5. Read the abstracts that contain an expression
    6. Find articles from a certain date
    7. Find other articles written by a person
    8. Find articles that have multimedia and are a certain type of material
    9. Get article given URL
    10. Update the read count for an article
    11. Add comment(s) to an article
    12. Delete many articles in a section with a certain keyword value
    13. Delete article(s) where the word count < X and read count < Y
    14. Add keyword to an article
    15. Find articles only in certain sections
    16. Get the top N keywords for articles
    **************************************************************************"""
    print(options)
    selected = str(input("Select an operation:\t"))
    #LIMIT = int(input('Limit output to __ documents:\t'))
    if selected == '1':
        article_doc = UseCases.addArticle()
        db.article.insert_one(article_doc)
        print(article_doc)
    elif selected == '2':
        query = UseCases.findArticlesWKeyValueRank()
        results = db.article.find({'keywords': {'$elemMatch':query}}).limit(LIMIT)
        print_results(results)
    elif selected == '3':
        wc = UseCases.findArticlesNWordCount()
        results = db.article.find({'word_count': {'$gte':wc}}, 
            {'web_url':1, 'word_count': 1, 'abstract':1}).limit(LIMIT)
        print_results(results)
    elif selected == '4':
        query = UseCases.getTotalWordCountSubsectionName()
        query.append({'$limit':LIMIT})
        results = db.article.aggregate(query)
        print_results(results)
    elif selected == '5':
        query = UseCases.readAbstractBasedOnExpr()
        results = db.article.find(query, {'abstract':1,'web_url':1,'keywords':1}).limit(LIMIT)
        print_results(results)
    elif selected == '6':
        user_input = UseCases.findArticlesFromDate()
        results = article.find(user_input).limit(LIMIT)
        print_results(results)
    elif selected == '7':
        query = UseCases.findOtherArticlesByPerson()
        results = db.article.find(query,{'abstract': 1,'web_url':1,}).limit(LIMIT)
        print_results(results)
    elif selected == '8':
        query = UseCases.getTypeOfMaterialAndMultimedia()
        results = db.article.find(query).limit(LIMIT)
        print_results(results)
    elif selected == '9':
        query = UseCases.getArticle()
        results = db.article.find(query)
        print_results(results)
    elif selected == '10':
        web_url = input('URL of the article you read:\t')
        query = UseCases.updateReadCountForArticle()
        message = db.article.update_one({'web_url':web_url},query)
        print("Successfully modified: " + str(message.acknowledged))
        results = db.article.find({'web_url':web_url})
        print_results(results)
    elif selected == '11':
        web_url = input('URL of the existing article you would like to add comments to:\t')
        query = UseCases.addCommentsToArticle()
        message = db.article.update_one({'web_url':web_url},query)
        print("Successfully modified: " + str(message.acknowledged))
        results = db.article.find({'web_url':web_url})
        print_results(results)
    elif selected == '12':
        query = UseCases.deleteManyArticlesWithSectionKeywordVal()
        message = db.article.delete_many(query)
        print("Deleted: " + str(message.deleted_count) + " articles")
    elif selected == '13':
        query = UseCases.deleteArticleWordReadCount()
        message = db.article.delete_many(query)
        print("Deleted: " + str(message.deleted_count) + " articles")
    elif selected == '14':
        web_url = input('URL of the existing article you would like to add keywords to:\t')
        new_kw = UseCases.addKeywordArticle()
        message = db.article.update_one({'web_url':web_url},new_kw)
        print("Successfully modified: " + str(message.acknowledged))
        results = db.article.find({'web_url':web_url})
        print_results(results)
    elif selected == '15':
        section_choices = UseCases.getArticlesInSections()
        results = db.article.find({'section_name':{'$in':section_choices}}).limit(LIMIT)
        print_results(results)
    elif selected == '16':
        query = UseCases.getNMostPopularKeywords()
        results = db.article.find({},query).limit(LIMIT)
        print_results(results)
    else:
        print("Good-bye!")
        myclient.close() #close connection
        exit()
    main_menu()
def print_results(results):
    for r in results:
        print(r)
    
if __name__ == "__main__": 
    db_size_bytes = db.command("dbstats")['storageSize']
    #if DB doesn't have at least 1GB of data, it deletes anything in the collection and populates the DB
    if db_size_bytes < 1000000000: #1000000000 500000000
        x = article.delete_many({})
        #print(x)
        article.create_index([("web_url", ASCENDING), ("section_name", ASCENDING)])
        addArticlesDB(myclient, db, article, nyt)
    print("This application displays articles from 2008-2020(inclusive)")
    main_menu()
