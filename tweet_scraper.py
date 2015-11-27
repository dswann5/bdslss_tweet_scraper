#!/usr/bin/python

import tweepy
import json
import csv
import sys
import pymongo
import datetime
import time
import logging
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ProtocolError

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_data(self, data):
        json_data = json.loads(data)
        #file.write(str(json_data))
	# Add to database instead of file
	tweet_collection.insert(json_data)

    def on_error(self, status_code):
        logging.error(sys.stderr, 'Encountered error with status code: ', str(status_code))
        return True # Don't kill the stream

    def on_timeout(self):
        logging.error('Timeout...')
        return True # Don't kill the stream

# Retrieve list of keywords from the given corpus file, assumed to be CSV
def parse_csv(corpus_path):
    keywords = []
    with open(corpus_path, 'rb') as corpus:
        reader = csv.reader(corpus, delimiter=',')
        for row in reader:
            for word in row:
                if word is not '':
                    keywords.append(word)
    return keywords

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='scraper.log', level=logging.INFO)

logging.info("Filtering using keywords: " + str(parse_csv('corpus.csv')))

# Attach to Mongo and create database if it doesn't exist already
def connect_to_db():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client['tweet_database']
    tweet_collection = db['tweets']
    logging.info("Connected to Mongo database " + str(tweet_collection))
    return tweet_collection

auth = tweepy.OAuthHandler("TuRZl0vHr0c7LHUIYRM42TNF4", "ThcNNtcyqydd3Ejf7XoWoDXJrRoPt5KuIrusfyvDxBfy98ZpVi")
auth.set_access_token("758446584-bIL3A7LPaQywQ6g0O0IhCXk0G0w09GNceOMzoFVS", "Jm6lRMxcvAFIbdBlafEgkBnk1ZipxmrnXKvXhanLfclZV")

# Test tweet retrieval
#api = tweepy.API(auth)
#print json.loads(api.get_user("@snowden"))['followers']

#file = open('tweets.json', 'a')

while (1):	
    try:
	tweet_collection = connect_to_db()
        sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
        sapi.timeout = 901 # Just above the 15 minute rate limit
        sapi.filter(track=parse_csv('corpus.csv'))
    except ( Timeout, ReadTimeoutError, ConnectionError, ProtocolError, tweepy.error.TweepError) as err:
	logging.error("Reloading stream connection, error " + str(err))
	continue
# In case we want to add location constraints
#sapi.filter(locations=[103.60998,1.25752,104.03295,1.44973], track=parse_csv('corpus.csv'))
