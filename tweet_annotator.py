#!/usr/bin/python

import json
import sys
import pymongo
from pymongo import MongoClient

DELIMITER = "\n------------------------------\n"
POSITIVE = 1
NEGATIVE = -1
NEUTRAL = 0

# Connect to filtered collection
def connect_to_filtered_tweets():
    client = MongoClient('localhost', 27017)
    db = client['tweet_database']
    filtered_tweet_collection = db['filtered']
    return filtered_tweet_collection

# Connect to annotated collection
def connect_to_annotated_tweets():
    client = MongoClient('localhost', 27017)
    db = client['tweet_database']
    annotated_tweet_collection = db['annotated']
    return annotated_tweet_collection

def main():
    # Connect to mongo database
    filtered = connect_to_filtered_tweets()

    print "Number of tweets to annotate: " + str(filtered.find().count())
    lower = int(raw_input("Lower Range: "))
    upper = int(raw_input("Upper Range: "))

    if lower >= upper:
        print "lower must be < upper"
        sys.exit(0)

    annotated = connect_to_annotated_tweets()

    # Iterate through all tweets
    for tweet in filtered.find():
	data = {}
	try:
	    # Build collection entry
	    data["id"] = str(tweet['id'])
	    data["text"] = tweet['text'].encode('ascii', 'ignore') 
	    data["entities"] = str(tweet['entities'])
	    data["user"] = str(tweet['user'])
	    print DELIMITER + tweet['text'].encode('ascii', 'ignore') + DELIMITER
	    arg = raw_input("Input:\n'a': positive\n's': negative\n'd': neutral/irrelevant\n> ")
	    if arg is 'a':
		# Positive
		data["sentiment"] = POSITIVE
	    elif arg is 's':
		# Negative
		data["sentiment"] = NEGATIVE
	    elif arg is 'd':
		# Neutral/irrelevant
		data["sentiment"] = NEUTRAL

	    annotated.insert(data) 
	except KeyError:
	    print "Tweet does not have an id. Ignore"


if __name__ == "__main__":
    main()
