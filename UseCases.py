from datetime import datetime, timezone
import random
import string
from bson import regex
############################CREATE: addArticle()#############################
"""
    Helper function for addArticle()
    Randomly generates and returns a unique id for each article
"""
def create_article_id():
    id_1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    id_2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_3 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_4 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_5 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 12))
    return "nyt://article/"+id_1+"-"+id_2+"-"+id_3+"-"+id_4+"-"+id_5

"""
    Helper function for addArticle()
    Takes the keywords provided by the client and turns them into a dictionary and adds them to
    a list
"""
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
"""
    Helper function for addArticle()
    Creates the byline of the article (which is the name of the writer)
"""
def create_byline(first, middle, last,rank):
    full_name = ""
    if middle == "":
        full_name = "By "+first+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':None,'lastname':last,'rank':rank}]}
    else:
        full_name = "By "+first+" "+middle+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':middle,'lastname':last,'rank':rank}]}
    return byline

"""
    Allows users to add an article to the database
    Users add information pertaining to the article which is then transformed into a dict
"""
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
    
    print("\n[Metro, Sports, Letters, Business, National, Foreign, Editorial, Culture, ContinuousNews, OpEd, Summary, Science, New York, Finance, Magazine, Real Estate, Education, Dining]")
    news_desk = input('News desk:\t')

    source = input("Source:\t")

    article_doc = {'abstract':abstract,'web_url':web_url,'source':source,
    'headline':{'main':headline,'kicker': None, 'content_kicker': None, 
    'print_headline': '', 'name': None, 'seo': None, 'sub': None},'keywords':keywords,
    'pub_date':pub_date,'document_type':'article','news_desk':news_desk,
    'section_name':section_name,'subsection_name': subsection_name, 'byline':byline,'type_of_material':type_of_material,
    '_id':article_id,'word_count':word_count,'uri':article_id, 'read_count':0}
    return article_doc
######################RETRIEVE: findArticlesWKeyValueRank()######################
"""
    Find articles where the keyword value has a certain rank
"""
def findArticlesWKeyValueRank():
    value = input('Keyword value:\t')
    rank = int(input('Rank (less than or equal to):\t'))
    if rank < 1:
        print("Rank must be a number >= 1. Default is set to 1")
        rank = 1
    return {'value':value, 'rank':{'$lte':rank}}
######################RETRIEVE: findArticlesNWordCount()######################
"""
    Find articles where word count >= number
        Return: word count value
"""
def findArticlesNWordCount():
    word_count = int(input('Find articles with a word count >=:\t'))
    # TODO: Check if this works
    if word_count <= 0:
        while word_count <= 0:
            print("Word count must be greater than 0")
            word_count = int(input('Find articles with a word count >=:\t'))

    return word_count
######################RETRIEVE: getTotalWordCountSubsectionName()######################
"""
    Gets the total word count of all the subsections in a section
        Return: query to get the word count of all subsections in a section
"""
def getTotalWordCountSubsectionName():
    print('Choose a section: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    print("\t\tNOTE: Some sections may not have subsections. In that case, nothing will be displayed")
    section_name = input('Section name:\t')
    query=[
        {'$match': {'section_name': section_name}},
	    {'$group': {'_id': '$subsection_name', 'total': {'$sum':'$word_count'}}},
	    {'$sort': {'total':-1}}
    ]
    return query
######################RETRIEVE: readAbstractBasedOnExpr()######################
"""
    Finds abstracts that contain an expression
"""
def readAbstractBasedOnExpr():
    expr = input('Enter a keyword value expression (case sensitive):\t')
    query = {'abstract':{'$regex':f"{expr}"}}
    return query
######################RETRIEVE: findArticlesFromDate()######################
"""
Find articles from a certain date
    Return the input which is date of article need to be find
"""
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
    return query
######################RETRIEVE: findOtherArticlesByPerson()######################
"""
Find articles by person by firstname + lastname 
    Return the query by $elemMatch which use input are fistname and lastname of the author.
"""
def findOtherArticlesByPerson():
    firstname = input('First name:\t')
    lastname = input('Last name:\t')
    query = {'byline.person':{'$elemMatch': {'firstname':firstname,'lastname': lastname}}} 
    return query
######################RETRIEVE: getTypeOfMaterialAndMultimedia()######################
"""
Find article by getting type of the material and multimedia
    Return query which use $exists to check for existing field, search by type of material
"""
def getTypeOfMaterialAndMultimedia():
    print("\n[Op-Ed, News, Letter, Schedule, Brief, Editorial, Review, Correction, Obituary (Obit), Slideshow]")
    input1 = input('Type of Material:\t')
    query = {'type_of_material': input1, 'multimedia': {'$exists': True}}
    return query
######################RETRIEVE: getArticle()######################
"""
    Retrieves the article metadata of the provided URL
"""
def getArticle():
    url = input('URL:\t')
    query = {'web_url': url}
    return query

######################UPDATE: updateReadCountForArticle()######################
"""
    Updates the read count for an article given the URL
"""
def updateReadCountForArticle():
    inc_read = {'$inc':{'read_count':1}}
    return inc_read
######################UPDATE: addCommentsToArticle()######################
"""
    Add comments to an article
"""
def addCommentsToArticle():
    num_comments = int(input('How many comments will you add:\t'))
    comments_list = []
    for i in range(num_comments):
        comment_info = {}
        comment_info['userDisplayName'] = input('\tUser Display Name:\t')
        comment_info['commentBody'] = input('\tComment Body:\t')
        comment_info['recommendations'] = int(input('\tNumber of recommendations(integer):\t'))
        comments_list.append(comment_info)
    query = {'$set':{'comments': comments_list}}
    return query
######################DELETE: deleteManyArticlesWithSectionKeywordVal()######################
"""
    Deletes articles with a specific keyword value in a specific section
"""
def deleteManyArticlesWithSectionKeywordVal():
    print('Sections: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    section_name = input("Delete articles with section name:\t")
    kw_value = input("with keyword value:\t")
    query = {'section_name':section_name,'keywords': {'$elemMatch':{'value':kw_value}}}
    return query
######################DELETE: deleteArticleWordReadCount()######################
"""
    Deletes articles where the word count < X and read count < Y (X and Y are int)
"""
def deleteArticleWordReadCount():
    wc = int(input('\tDelete article where word count is less than (integer):\t'))
    rc = int(input('\tDelete article where read count is less than (integer):\t'))
    query = {'word_count': {'$lt': wc}, 'read_count': {'$lt': rc}}
    return query
######################UPDATE: addKeywordArticle()######################
"""
    Adds a keyword to the current list of keywords to an article
"""
def addKeywordArticle():
    new_kw = {}
    new_kw['name'] = input('Name of keyword [persons, subject, organizations]:\t')
    new_kw['value'] = input('Keyword value:\t')
    new_kw['rank'] = int(input('Rank of keyword(integer):\t'))
    query = {'$push': {'keywords': new_kw}}
    return query
######################RETRIEVE: getNMostPopularKeywords()######################
"""
    Returns the top N keywords for all articles
"""
def getNMostPopularKeywords():
    top_n_kw = int(input('Get top __ keywords for articles:\t'))
    query = {'keywords': {'$slice':top_n_kw}, '_id':0}
    return query
######################RETRIEVE: getArticlesInSections()######################
"""
    Retrieves articles ONLY in certain sections
"""
def getArticlesInSections():
    print('Sections: [Fashion, Parenting, Video, Travel, New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Homepage, College, Movies, Education, Health, Theater, Food]')
    section_choices = []
    choice = ""
    print("Enter the sections as they appear. Press \'d\' when done.")
    while choice != "d":
        choice = input("\tSection:\t")
        section_choices.append(choice)
    return section_choices[:-1]
######################DELETE: deleteOneArticle()######################
"""
    Deletes an article from the database given an URL
"""

if __name__ == "__main__": 
    print(__name__)