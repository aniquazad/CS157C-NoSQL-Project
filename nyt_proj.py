from PopulateDB import addArticlesDB
from pynytimes import NYTAPI
from datetime import datetime, date, timezone
from pymongo import MongoClient, errors, ASCENDING, DESCENDING
from bson import regex
import sys
import json
import requests
import random
import string

nyt = NYTAPI("qsPCmSV09wV4AbCCaJmXFPxo3nCwGtbU")
LIMIT = 10 # output is limited to 10 documents

def start():
    global myclient
    global db
    global article
    try:
        #myclient = MongoClient("mongodb://localhost:27018/")
        myclient = MongoClient("mongodb://localhost:27018/", w=1,readPreference="primaryPreferred")
        print(myclient)
        print("Connection successful!")
    except errors.ConnectionFailure as e:
        print("Connection failed!")
        print(e)

    db = myclient["nyt"] #connect to database
    article = db["article"] #coonect to collections
    db_size_bytes = db.command("dbstats")['storageSize']
    #if DB doesn't have at least 1GB of data, it deletes anything in the collection and populates the DB
    if db_size_bytes < 1000000000: #1000000000 500000000
        article.delete_many({})
        article.create_index([("web_url", ASCENDING), ("section_name", ASCENDING)])
        addArticlesDB(myclient, db, article, nyt)
    print("This application displays articles from 2008-2020(inclusive)")
    main_menu()
"""
    This function displays the main menu and allows users to choose from options
"""
def main_menu():
    options = """
    **************************************************************************
    1. Add article
    2. Get articles given a keyword value
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
    16. Get the top N keywords for articles in 2020
    **************************************************************************"""
    print(options)
    selected = str(input("Select an operation:\t"))
    if selected == '1':
        addArticle()
    elif selected == '2':
        findArticlesWKeyValue()
    elif selected == '3':
        findArticlesNWordCount()
    elif selected == '4':
        getTotalWordCountSubsectionName()
    elif selected == '5':
        readAbstractBasedOnExpr()
    elif selected == '6':
        findArticlesFromDate()
    elif selected == '7':
        findOtherArticlesByPerson()
    elif selected == '8':
        getTypeOfMaterialAndMultimedia()
    elif selected == '9':
        getArticle()
    elif selected == '10':
        web_url = input('URL of the article you read:\t')
        updateReadCountForArticle(web_url)
    elif selected == '11':
        web_url = input('URL of the existing article you would like to add comments to:\t')
        addCommentsToArticle(web_url)
    elif selected == '12':
        deleteManyArticlesWithSectionKeywordVal()
    elif selected == '13':
        deleteArticleWordReadCount()
    elif selected == '14':
        web_url = input('URL of the existing article you would like to add keywords to:\t')
        addKeywordArticle(web_url)
    elif selected == '15':
        getArticlesInSections()
    elif selected == '16':
        getNMostPopularKeywords()
    else:
        print("Good-bye!")
        myclient.close() #close connection
        exit()
    main_menu()

def print_results(results):
    for r in results:
        print('{')
        for k,v in r.items():
            print("\t",k,":\t",v)
        print('}')
        print()
######################USE CASES######################

    # Helper function for addArticle()
    # Randomly generates and returns a unique id for each article
def create_article_id():
    id_1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    id_2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_3 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_4 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_5 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 12))
    return "nyt://article/"+id_1+"-"+id_2+"-"+id_3+"-"+id_4+"-"+id_5

    # Helper function for addArticle()
    # Takes the keywords provided by the client and turns them into a dictionary and adds them to a list
def create_keywords(kw_list):
    keywords = []
    for i in range(len(kw_list)-1):
        temp_dict = {}
        temp_list = kw_list[i].split(',')
        temp_dict["name"] = temp_list[0]
        temp_dict["value"] = temp_list[1]
        temp_dict["rank"] = int(temp_list[2])
        temp_dict["major"] = "N"
        keywords.append(temp_dict)
    return keywords

    # Helper function for addArticle()
    # Creates the byline of the article (which is the name of the writer)
def create_byline(first, middle, last,rank):
    full_name = ""
    if middle == "":
        full_name = "By "+first+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':None,'lastname':last,'rank':rank}]}
    else:
        full_name = "By "+first+" "+middle+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':middle,'lastname':last,'rank':rank}]}
    return byline

    # Allows users to add an article to the database
    # Users add information pertaining to the article which is then transformed into a dict
def addArticle():
    article_id = create_article_id()
    pub_date = str(datetime.now().astimezone(timezone.utc).isoformat(timespec='seconds'))
    web_url = input("URL:\t")
    abstract = input("Abstract:\t")
    headline = input("Headline:\t")

    print("Person")
    first_name = input("\tFirst name:\t")
    middle_name = input("\tMiddle name:\t")
    last_name = input("\tLast name:\t")
    rank = input("\tRank:\t")
    byline = create_byline(first_name,middle_name,last_name,rank)

    print("\nPossible name choices: [subject, persons, organizations, glocations]")
    print("Keywords (name,value,rank) -- press d when done")
    kw_list=[]
    keyword = ""
    while keyword != "d":
        keyword = input("\t")
        kw_list.append(keyword)
    keywords = create_keywords(kw_list)

    word_count = int(input("Word count:\t"))
    
    print("\n[Op-Ed, News, Letter, Schedule, Brief, Editorial, Review, Correction, Obituary (Obit), Slideshow]")
    type_of_material = input("Type of material:\t")
   
    print("\n[New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Crosswords & Games, Education, Health, Theater, Food]")
    section_name = input("Section name:\t")
    
    print("\n[College Football, Media, World Business, Middle East, Pro Basketball, Music, Art & Design, Asia Pacific, Americas, Europe, Hockey, Bridge, Africa, Asia, Australia, Televsion]")
    subsection_name = input("Subsection name:\t")

    source = input("Source:\t")

    article_doc = {'abstract':abstract,'web_url':web_url,'source':source,
    'headline':{'main':headline,'kicker': None, 'content_kicker': None, 
    'print_headline': '', 'name': None, 'seo': None, 'sub': None},'keywords':keywords,
    'pub_date':pub_date,'document_type':'article',
    'section_name':section_name,'subsection_name': subsection_name, 'byline':byline,'type_of_material':type_of_material,
    '_id':article_id,'word_count':word_count,'uri':article_id, 'read_count':0}

    db.article.insert_one(article_doc)
    print(article_doc)


    # Find articles that has a specific keyword value
def findArticlesWKeyValue():
    value = input('Keyword value:\t')
    includeExclude = {'web_url':1, 'word_count': 1, 'abstract':1, 'keywords':1,'byline':1,'_id':0,'multimedia':0}
    results = db.article.find({'keywords': {'$elemMatch':{'value':value}}},includeExclude).limit(LIMIT)
    print_results(results)

    # Find articles where word count >= number
def findArticlesNWordCount():
    word_count = int(input('Find articles with a word count >=:\t'))
    # TODO: Check if this works
    if word_count <= 0:
        while word_count <= 0:
            print("Word count must be greater than 0")
            word_count = int(input('Find articles with a word count >=:\t'))
    includeExclude = {'web_url':1, 'word_count': 1, 'abstract':1, 'keywords':1,'byline':1,'_id':0,'multimedia':0}
    results = db.article.find({'word_count': {'$gte':word_count}},includeExclude).limit(LIMIT)
    print_results(results)

    # Gets the total word count of all the subsections in a given section

def getTotalWordCountSubsectionName():
    print('Choose a section: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    print("\t\tNOTE: Some sections may not have subsections. In that case, nothing will be displayed\n")
    section_name = input('Section name:\t')
    query=[
        {'$match': {'section_name': section_name}},
	    {'$group': {'_id': '$subsection_name', 'total': {'$sum':'$word_count'}}},
	    {'$sort': {'total':-1}},
        {'$limit':LIMIT}
    ]
    results = db.article.aggregate(query)
    print_results(results)

    # Finds abstracts that contain an expression
def readAbstractBasedOnExpr():
    expr = input('Enter a keyword value expression (case sensitive):\t')
    query = {'abstract':{'$regex':f"{expr}"}}
    includeExclude = {'web_url':1, '_id':0, 'multimedia':0,'keywords':1, 'abstract':1,'byline':1}
    results = db.article.find(query, includeExclude).limit(LIMIT)
    print_results(results)

    # Find articles from a specified date
def findArticlesFromDate():
    date_formats = """
        -year -- /YYYY/
		-year/month -- YYYY/MM
		-year/month/day -- YYYY/MM/DD
    """
    print(date_formats)
    print('Enter the date in one of the formats above.')
    date = input('Date:\t')
    query = {'web_url':{'$regex':f"{date}"}}
    includeExclude = {'web_url':1, '_id':0, 'multimedia':0,'keywords':1, 'abstract':1,'byline':1}
    results = article.find(query, includeExclude).limit(LIMIT)
    print_results(results)

 # Find other articles written by a person given their first and last name
def findOtherArticlesByPerson():
    firstname = input('First name:\t')
    lastname = input('Last name:\t')
    query = {'byline.person':{'$elemMatch': {'firstname':firstname,'lastname': lastname}}}
    includeExclude = {'web_url':1, '_id':0, 'multimedia':0,'keywords':1, 'abstract':1,'byline':1} 
    results = db.article.find(query,includeExclude).limit(LIMIT)
    print_results(results)

    # Find articles of a certain type of the material that also has multimedia
def getTypeOfMaterialAndMultimedia():
    print("\n[Op-Ed, News, Letter, Schedule, Brief, Editorial, Review, Correction, Obituary (Obit), Slideshow]")
    input1 = input('Type of Material:\t')
    query = {'type_of_material': input1, 'multimedia': {'$exists': True}}
    includeExclude = {'web_url':1, '_id':0, 'multimedia':1,'type_of_material':1, 'abstract':1,'byline':1}
    results = db.article.find(query,includeExclude).limit(LIMIT)
    print_results(results)

    # Retrieves the article metadata of the provided URL
def getArticle():
    url = input('URL:\t')
    query = {'web_url': url}
    results = db.article.find(query)
    print_results(results)

    # Updates the read count for an article given the URL
def updateReadCountForArticle(web_url):
    inc_read = {'$inc':{'read_count':1}}
    message = db.article.update_one({'web_url':web_url},inc_read)
    print("Successfully modified: " + str(message.acknowledged))

    results = db.article.find({'web_url':web_url})
    print_results(results)
    
    # Add comments to an article
def addCommentsToArticle(web_url):
    num_comments = int(input('How many comments will you add:\t'))
    comments_list = []
    for i in range(num_comments):
        comment_info = {}
        comment_info['userDisplayName'] = input('\tUser Display Name:\t')
        comment_info['commentBody'] = input('\tComment Body:\t')
        comment_info['recommendations'] = int(input('\tNumber of recommendations(integer):\t'))
        comments_list.append(comment_info)

    query = {'$set':{'comments': comments_list}}
    message = db.article.update_one({'web_url':web_url},query)
    print("Successfully modified: " + str(message.acknowledged))

    results = db.article.find({'web_url':web_url})
    print_results(results)

    # Deletes articles with a specific keyword value in a specific section
def deleteManyArticlesWithSectionKeywordVal():
    print('Sections: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    section_name = input("Delete articles with section name:\t")
    kw_value = input("with keyword value:\t")
    query = {'section_name':section_name,'keywords': {'$elemMatch':{'value':kw_value}}}

    message = db.article.delete_many(query)
    print("Deleted: " + str(message.deleted_count) + " articles")

    # Deletes articles where the word count < X and read count < Y (X and Y are int)
def deleteArticleWordReadCount():
    wc = int(input('\tDelete article where word count is less than (integer):\t'))
    rc = int(input('\tDelete article where read count is less than (integer):\t'))
    query = {'word_count': {'$lt': wc}, 'read_count': {'$lt': rc}}

    message = db.article.delete_many(query)
    print("Deleted: " + str(message.deleted_count) + " articles")

    # Adds a keyword to the current list of keywords to an article
def addKeywordArticle(web_url):
    new_kw = {}
    new_kw['name'] = input('Name of keyword [persons, subject, organizations]:\t')
    new_kw['value'] = input('Keyword value:\t')
    new_kw['rank'] = int(input('Rank of keyword(integer):\t'))
    query = {'$push': {'keywords': new_kw}}

    message = db.article.update_one({'web_url':web_url},query)
    print("Successfully modified: " + str(message.acknowledged))
    results = db.article.find({'web_url':web_url})
    print_results(results)

    # Returns the top N keywords for all articles in 2020
def getNMostPopularKeywords():
    top_n_kw = int(input('Get top __ keywords for articles:\t'))
    query = {'keywords': {'$slice':top_n_kw}, '_id':0,'abstract':0, 'headline':0,'byline':0,'snippet':0,'lead_paragraph':0,'multimedia':0}
    
    results = db.article.find({'web_url':{'$regex':"/2020/"}},query).limit(LIMIT)
    print_results(results)

    # Retrieves articles ONLY in certain sections
def getArticlesInSections():
    print('Sections: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    section_choices = []
    choice = ""
    print("Enter the sections as they appear. Press \'d\' when done.")
    while choice != "d":
        choice = input("\tSection:\t")
        section_choices.append(choice)
    #section_choices = section_choices[:-1]
    includeExclude = {'web_url':1, '_id':0, 'multimedia':0,'keywords':1, 'abstract':1,'byline':1}
    results = db.article.find({'section_name':{'$in':section_choices[:-1]}},includeExclude).limit(LIMIT)
    print_results(results)
    
if __name__ == "__main__": 
    start()
