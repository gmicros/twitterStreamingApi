#Import the necessary methods from tweepy library
#! /usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import urllib
import json
import re

#Variables that contains the user credentials to access Twitter API 
access_token = "827268804359053313-8j4xGXrMnsunJGNt5jAiFaLjzEK0zwN"
access_token_secret = "fyhey4tyQu5dWj2XsHpkvvyijBkZnmI1OIIynOda6bhs6"
consumer_key = "ZdLJZz2T4fLTFaEgc0piD1rvF"
consumer_secret = "qGEqPv4dn537sAEgPmdir2a30tkG4s66PghiYKclA1CpA0lFZM"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    rawData = []
    jDatas = []
    numTweets = 0

    def __init__(self, noTweets):
        self.numTweets = noTweets

    def on_data(self, data):
        print str(len(self.rawData)) + " " + str(len(self.jDatas))
        self.rawData.append(data)
        self.parseData(data)        
        return len(self.jDatas) < self.numTweets

    def on_error(self, status):
        print status
    
    def parseData(self, data):
        jdata = json.loads(data)
        if 'possibly_sensitive' in jdata.keys():
            self.jDatas.append(jdata)

def saveUris(uris, filename):
    f = open('filename', 'w')
    for uri in uris:
        f.write(uri+'\n')
    f.close()

def getAllTheFinalURI(links):
    uris = []
    for link in links:
        uri = getFinalURI(link)
        uris.append(uri)
    return uris

def getFinalURI(link):
    try:
        url = urllib.urlopen(link)
        return url
    except:
        return ""        

def extractLinksFromTweets(tweets):
    links = []
    for tweet in tweets:
        link = extractLinkFromTweet(tweet)
        links.append(link)
    return links

def extractLinkFromTweet(tweet):
    link = ""
    if 'retweeted_status' in tweet:
        link = extractLink(tweet['retweeted_status']['text'])
    else:
        link = extractLink(tweet['text'])
    return link

def extractLink(text):
        regex = r'https?://t.co/\S{10,10}'
        match = re.search(regex, text)
        if match:
            return match.group()
        return ''

def saveTweets(tweets, filename):
    f = open(filename, 'w')
    for tweet in tweets:
        json.dump(tweet, f)
        f.write('\n')
    f.close()

def loadTweets(filename):
    f = open(filename, 'r')
    jData = []
    for i in f:    
        jData.append(json.loads(i))
    f.close()
    return jData

def collectTheTweets(noTweets):
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener(noTweets)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby', 'trump', 'cnn', 'time', 'articles'])

    return l.jDatas


    
