import json
import pandas
import os
import pymongo
from stackapi import StackAPI
    
from django.template.context_processors import csrf
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.conf  import settings

from spoken_auth.models import TutorialDetails, TutorialResources, TutorialCommonContent
from .tfidf import *


def get_questions_from_stack(category, tutorial, terms, db_tags):
    rel_tags = []

    if len(db_tags) != 0:
        rel_tags.extend(db_tags)
    if len(terms) != 0:
        rel_tags.extend(terms)

    print("rel_tags")
    print(rel_tags)
    mongo_ip = os.getenv("URL_MONGO_IP")
    mongo_port = os.getenv("URL_MONGO_PORT")
    mongo_url = "mongodb://" + mongo_ip + ":" + mongo_port
    client = pymongo.MongoClient(mongo_url)
    db = client.stackapi
    collec_ques = db.questions
    collec_ques.create_index('question_id')

    ''' fetch questions '''
    entries = []
    print("Fetching data from stackoverflow.. ")
    SITE = StackAPI('stackoverflow')
    
    ''' Fetching questions with only category name(e.g. latex) as tag '''
    questions = SITE.fetch('questions', fromdate=1456232494, min=20, tagged=category, sort='votes', order='desc')
    entries.extend(questions['items'])
    
    ''' Fetching questions with addition of rel_tags(obtained from quert/srt files) '''
    for t in db_tags:
        questions = SITE.fetch('questions', fromdate=1456232494, min=20, tagged=category+';'+t.lower(), sort='votes', order='desc')
        entries.extend(questions['items'])
        
    for t in rel_tags:
        questions = SITE.fetch('questions', fromdate=1456232494, min=20, tagged=category+';'+t.lower(), sort='votes', order='desc')
        entries.extend(questions['items'])
    
    ''' inserting fetched data into mongodb '''
    if len(entries) > 0:
        for entry in entries:
            collec_ques.update({'question_id': entry['question_id']}, entry, upsert=True)
    print(str(len(entries)) + " questions fetched and inserted into mongodb")

def get_categories_tutorials():
    ''' get all categories '''
    categories = []
    trs = TutorialResources.objects.filter(Q(status=1) | Q(status=2),tutorial_detail__foss__show_on_homepage__lt=2, language__name='English')
    trs = trs.values('tutorial_detail__foss__foss').order_by('tutorial_detail__foss__foss')
        
    for tr in trs.values_list('tutorial_detail__foss__foss').distinct():
        categories.append(tr[0])
    
    print("categories:")
    print(categories)
    ''' for each category fetch all tutorials '''
    for category in categories:
        tutorials = TutorialDetails.objects.using('spoken').filter(foss__foss=category).order_by('level', 'order')
        cat = tutorials[0].foss
        path = settings.MEDIA_ROOT + 'videos/' + str(cat.pk)
        create_vocab_tfidf(path)
        print("for categoery - " + str(cat))

        ''' for each tutorial in the category, find terms from db as well as srt files '''
        for tut in tutorials:
            tutorial = tut.tutorial
            print("tutorial - " + str(tutorial))
            td_rec = TutorialDetails.objects.using('spoken').filter(tutorial=tutorial, foss__foss=category).order_by('level', 'order')
            cat = td_rec[0].foss
            td = td_rec[0]

            ''' fetching terms from db '''
            db_tags = TutorialCommonContent.objects.using('spoken').filter(tutorial_detail=td.pk)
            db_tags = db_tags[0].keyword.replace(".", "").split(", ")
            print("list of db_tags >>>>>>>>>>>>")
            print(db_tags)
            
            ''' fetching terms from srt files using NLP method '''
            filename = settings.MEDIA_ROOT + 'videos/' + str(cat.pk) + '/' + str(td.pk) + '/' + tutorial.replace(' ', '-') + '-English.srt'
            topic_keys = extract_keywords(filename)
            print("topic_keys >>>>>>>>>>>>>")
            print(topic_keys)

            ''' Scraping stackoverflow to get questions and store in mongodb '''
            get_questions_from_stack(category.lower(), tutorial.lower(), topic_keys, db_tags)
            
    print("Successfully fetched data from stackoverflow")

get_categories_tutorials()