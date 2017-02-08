#Import the necessary methods from tweepy library
#! /usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json

#Variables that contains the user credentials to access Twitter API 
access_token = "827268804359053313-8j4xGXrMnsunJGNt5jAiFaLjzEK0zwN"
access_token_secret = "fyhey4tyQu5dWj2XsHpkvvyijBkZnmI1OIIynOda6bhs6"
consumer_key = "ZdLJZz2T4fLTFaEgc0piD1rvF"
consumer_secret = "qGEqPv4dn537sAEgPmdir2a30tkG4s66PghiYKclA1CpA0lFZM"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    rawData = []
    jDatas = []

    def extract_link(text):
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        match = re.search(regex, text)
        if match:
            return match.group()
        return ''

    def parseData(self, data):
        jdata = json.loads(data)
        if 'possibly_sensitive' in jdata.keys():
            self.jDatas.append(jdata)

    def on_data(self, data):
        print str(len(self.rawData)) + " " + str(len(self.jDatas))
        self.rawData.append(data)
        self.parseData(data)        
        return len(self.jDatas) < 15000

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])


def runThis():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby', 'trump', 'cnn', 'time', 'articles'])

    f = open('tweet_dump', 'w')
    for i in l.jDatas:
        f.write(str(i) + '\n')

    return l.jDatas


    
