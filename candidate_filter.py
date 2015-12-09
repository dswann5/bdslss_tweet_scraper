#!/usr/bin/python

import json
import sys
import csv
import pymongo
from pymongo import MongoClient

candidates = {'berniesanders': [], 'hillaryclinton': [], 'martinomalley': [], 'donaldtrump':[],
	      'bencarson': [], 'marcorubio': [], 'tedcruz': [], 'jebbush':[], 'chrischristie':[], 
	      'carlyfiorina':[], 'jimgilmore':[], 'randpaul': [], 'johnkasich':[] , 'mikehuckabee': [], 
	      'lindseygraham': [], 'ricksantorum': [], 'georgepataki': [] 
	     }

client = MongoClient('localhost', 27017)

# Connect to a specified collection
def connect_to_collection(collection_name):
    db = client['tweet_database']
    filtered_tweet_collection = db[collection_name]
    return filtered_tweet_collection

# Retrieve list of keywords from the given corpus file, assumed to be CSV
def get_candidate_keywords(corpus_path):
    with open(corpus_path, 'rb') as corpus:
        reader = csv.reader(corpus, delimiter=',')
	current_candidate = ''
	for row in reader:
	    if (row[0] in candidates.keys()):
		current_candidate = row[0]
		candidates[current_candidate].append(row[0]) 
		continue	
	    for word in row:
		if word is not '':
		    candidates[current_candidate].append(word) 
    return candidates

def main():

    get_candidate_keywords('corpus_no_commas.csv') 

    # Connect to filtered source mongo collection
    filtered = connect_to_collection('filtered')
     
    # Iterate through all tweets
    for tweet in filtered.find():
	try:
	    text = tweet['text'].encode('ascii', 'ignore').lower() 

	    # Insert tweet into relevant candidate collection if any keyword matches
	    for candidate, values in candidates.iteritems():
		for keyword in values:
		    if keyword in text:
			#print "inserting into " + candidate
			collection = connect_to_collection(candidate)
			collection.insert(tweet)
	except(KeyError, pymongo.errors.DuplicateKeyError):
	    pass 
if __name__ == "__main__":
    main()
