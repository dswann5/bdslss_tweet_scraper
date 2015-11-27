#!/usr/bin/python

import json
import sys
import pymongo

DELIMITER = "\n------------------------------\n"

# Attach to Mongo and create database if it doesn't exist already
def connect_to_db():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client['tweet_database']
    tweet_collection = db['tweets']
    return tweet_collection

# Connect to mongo database
tweets = connect_to_db()

f = open('filtered_tweets.txt', 'w')

# Iterate through all tweets
for tweet in tweets.find():
    try:
        #print tweet['text'].encode('ascii', 'ignore')
        f.write(str(tweet['id']) + ", " + 
            tweet['text'].encode('ascii', 'ignore') + DELIMITER);
    except KeyError:
        print "Tweet does not have an id. Ignore"
