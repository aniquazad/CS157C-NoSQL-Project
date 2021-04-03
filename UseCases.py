from datetime import datetime, timezone
import random
import string
def create_article_id():
    id_1 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    id_2 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_3 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_4 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 4))
    id_5 = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 12))
    return "nyt://article/"+id_1+"-"+id_2+"-"+id_3+"-"+id_4+"-"+id_5

def create_keywords(kw_list):
    keywords = []
    for i in range(len(kw_list)-1):
        temp_dict = {}
        temp_list = kw_list[i].split(',')
        temp_dict["name"] = temp_list[0]
        temp_dict["value"] = temp_list[1]
        temp_dict["rank"] = temp_list[2]
        temp_dict["major"] = "N"
        keywords.append(temp_dict)
    return keywords

def create_byline(first, middle, last,rank):
    full_name = ""
    if middle == "":
        full_name = "By "+first+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':None,'lastname':last,'rank':rank}]}
    else:
        full_name = "By "+first+" "+middle+" "+last
        byline = {'original':full_name,'person':[{'firstname':first,'middlename':middle,'lastname':last,'rank':rank}]}
    return byline

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

    word_count = input("Word count:\t")
    
    print("\n[Op-Ed, News, Letter, Schedule, Brief, Editorial, Review, Correction, Obituary (Obit), Slideshow]")
    type_of_material = input("Type of material:\t")
   
    print("\n[New York, Sports, Opinion, Business Day, Technology, Science, World, U.S., Arts, Opinion, World, Books, Crosswords & Games, Education, Health, Theater, Food]")
    section_name = input("Section name:\t")
    
    print("\n[College Football, Media, World Business, Middle East, Pro Basketball, Music, Art & Design, Asia Pacific, Americas, Europe, Hockey, Bridge, Africa, Asia, Australia, Televsion]")
    subsection_name = input("Subsection name:\t")
    
    print("\n[Metro, Sports, Letters, Business, National, Foreign, Editorial, Culture, ContinuousNews, OpEd, Summary, Science, New York, Finance, Magazin, Real Estate, Education, Dining]")
    news_desk = input('News desk:\t')

    source = input("Source:\t")
    article_doc = {'abstract':abstract,'web_url':web_url,'source':source,
    'headline':{'main':headline,'kicker': None, 'content_kicker': None, 
    'print_headline': '', 'name': None, 'seo': None, 'sub': None},'keywords':keywords,
    'pub_date':pub_date,'document_type':'article','news_desk':news_desk,
    'section_name':section_name,'subsection_name': subsection_name, 'byline':byline,'type_of_material':type_of_material,
    '_id':article_id,'word_count':word_count,'uri':article_id}
    return article_doc
def findArticlesWKeyValueRank():
    value = input('Keyword value:\t')
    rank = input('Rank:\t')
    return {'value':value, 'rank':{'$gte':int(rank)}}
if __name__ == "__main__": 
    addArticle()