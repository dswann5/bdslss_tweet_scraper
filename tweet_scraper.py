#!/usr/bin/python

import tweepy
import json
import csv
import sys
import pymongo

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_data(self, data):
        json_data = json.loads(data)
        #file.write(str(json_data))
	# Add to database instead of file
	tweet_collection.insert(json_data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
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

print "Search keywords: " + str(parse_csv('corpus.csv'))

auth = tweepy.OAuthHandler("TuRZl0vHr0c7LHUIYRM42TNF4", "ThcNNtcyqydd3Ejf7XoWoDXJrRoPt5KuIrusfyvDxBfy98ZpVi")
auth.set_access_token("758446584-bIL3A7LPaQywQ6g0O0IhCXk0G0w09GNceOMzoFVS", "Jm6lRMxcvAFIbdBlafEgkBnk1ZipxmrnXKvXhanLfclZV")

api = tweepy.API(auth)

# Test tweet retrieval
#print json.loads(api.get_user("@snowden"))['followers']

# Attach to Mongo and create database if it doesn't exist already
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['tweet_database']
tweet_collection = db['tweets']

#file = open('tweets.json', 'a')

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=parse_csv('corpus.csv'))

# In case we want to add location constraints
#sapi.filter(locations=[103.60998,1.25752,104.03295,1.44973], track=parse_csv('corpus.csv'))
