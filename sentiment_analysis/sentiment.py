import json
import re
import pymongo
from pymongo import MongoClient
import nltk, nltk.classify.util
from nltk.classify import NaiveBayesClassifier
# search patterns for features
class TwittElection:
    def __init__(self):
        self.candidates = ['berniesanders', 'hillaryclinton', 'martinomalley', 'donaldtrump','bencarson', 'marcorubio', 'tedcruz', 'jebbush', 'chrischristie',
          'carlyfiorina', 'jimgilmore', 'randpaul', 'johnkasich' , 'mikehuckabee', \
          'lindseygraham', 'ricksantorum', 'georgepataki' \
         ]
        self.collection = dict()
        self.result = dict()

        self.testFeatures = \
            [('hasAddict',     (' addict',)), \
            ('hasAwesome',    ('awesome',)), \
             ('hasBroken',     ('broke',)), \
             ('hasBad',        (' bad',)), \
             ('hasBug',        (' bug',)), \
             ('hasCant',       ('cant','can\'t')), \
             ('hasCrash',      ('crash',)), \
             ('hasCool',       ('cool',)), \
             ('hasDifficult',  ('difficult',)), \
             ('hasDisaster',   ('disaster',)), \
             ('hasDown',       (' down',)), \
             ('hasDont',       ('dont','don\'t','do not','does not','doesn\'t')), \
             ('hasEasy',       (' easy',)), \
             ('hasExclaim',    ('!',)), \
             ('hasExcite',     (' excite',)), \
             ('hasExpense',    ('expense','expensive')), \
             ('hasFail',       (' fail',)), \
             ('hasFast',       (' fast',)), \
             ('hasFix',        (' fix',)), \
             ('hasFree',       (' free',)), \
             ('hasFrowny',     (':(', '):')), \
             ('hasFuck',       ('fuck',)), \
             ('hasGood',       ('good','great')), \
             ('hasHappy',      (' happy',' happi')), \
             ('hasHate',       ('hate',)), \
             ('hasHeart',      ('heart', '<3')), \
             ('hasIssue',      (' issue',)), \
             ('hasIncredible', ('incredible',)), \
             ('hasInterest',   ('interest',)), \
             ('hasLike',       (' like',)), \
             ('hasLol',        (' lol',)), \
             ('hasLove',       ('love','loving')), \
             ('hasLose',       (' lose',)), \
             ('hasNeat',       ('neat',)), \
             ('hasNever',      (' never',)), \
             ('hasNice',       (' nice',)), \
             ('hasPoor',       ('poor',)), \
             ('hasPerfect',    ('perfect',)), \
             ('hasPlease',     ('please',)), \
             ('hasSerious',    ('serious',)), \
             ('hasShit',       ('shit',)), \
             ('hasSlow',       (' slow',)), \
             ('hasSmiley',     (':)', ':d', '(:')), \
             ('hasSuck',       ('suck',)), \
             ('hasTerrible',   ('terrible',)), \
             ('hasThanks',     ('thank',)), \
             ('hasTrouble',    ('trouble',)), \
             ('hasUnhappy',    ('unhapp',)), \
             ('hasWin',        (' win ','winner','winning')), \
             ('hasWinky',      (';)',)), \
             ('hasWow',        ('wow','omg')) ]
        self.stopwords = list()
        with open("stopwords.txt") as f:
            for line in f:
                word = line.strip()
                self.stopwords.append(word)

    # Connect to annotated collection
    def connect_to_annotated_tweets(self):
        client = MongoClient('localhost', 27017)
        db = client['tweet_database']
        annotated_tweet_collection = db['annotated']
        return annotated_tweet_collection

    def connect_to_collections(self):
        client = MongoClient('localhost', 27017)
        db = client['tweet_database']
        for candidate in self.candidates:
            self.collection[candidate] = db[candidate].find()

    def connect_to_results(self):
        client = MongoClient('localhost', 27017)
        db = client['tweet_database']
        results = db['results']
        results.drop()
        return results

    def featureExtract(self,words):
        featureList = {}
        for test in self.testFeatures:
            key = test[0]
            featureList[key] = False
            for value in test[1]:
                if (value in words):
                    featureList[key] = True
                    words.remove(value)
        for word in words:
            if len(word)>2 and not word in self.stopwords:
                featureList[word] = True
        return featureList

    def evaluate(self):
        annotated = self.connect_to_annotated_tweets()
        self.connect_to_collections()
        trainData = []
        testData = []
        for tweet in annotated.find():
            trainData.append((tweet['text'].encode('ascii', 'ignore'),tweet['sentiment']))
        tweets = []
        for (tweet, sentiment) in trainData:
            lower = tweet.lower()
            text = re.sub( '\s+', ' ', lower ).strip()
            words = text.split()
            features = [self.featureExtract(words), sentiment]
            tweets.append(features)
        classifier = NaiveBayesClassifier.train(tweets)


        results_collection = self.connect_to_results()
        # testing
        #referenceSets = dict()
        #testSets = dict()
        i=0
        for candidate in self.candidates:
            tweets = []
            for cluster in self.collection[candidate]:
		tweet = cluster['text'].encode('ascii', 'ignore')
                lower = tweet.lower()
                text = re.sub( '\s+', ' ', lower ).strip()
                words = text.split()
                features = [self.featureExtract(words),1]
                tweets.append(features)
            positive = 0
            negative = 0
            neutral = 0
            for j, (features,i) in enumerate(tweets):
                predicted = classifier.classify(features)
                if predicted == 1:
                    positive += 1
                elif predicted == -1:
                    negative += 1
                elif predicted == 0:
                    neutral += 1
            self.result[candidate] = [positive,negative,neutral]
            json_data = {}
            json_data['candidate'] = str(candidate)
            json_data['pos'] = str(positive)
            json_data['neg'] = str(negative)
            json_data['neutral'] = str(neutral)
            results_collection.insert(json_data)
	print self.result

c = TwittElection()
c.evaluate()

