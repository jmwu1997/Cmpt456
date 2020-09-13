from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re

access_token = "3248149716-Ihz5xqN4gqwNqJpiOIvTU2WEu7drDH1yZb33e1r"
access_token_secret = "C4a8Z6o92CYwAXM1WMEwl5CjWIYL18Jjrfnn7QbFjKlmt"
consumer_key = "xcSm8CZNipD6tXMRHsZUWiz1X"
consumer_secret = "3s2ANOu17hkSXaslDUD3moDiRZRZUBXybIZGiWG8LobOJfljHu"

tracklist = ['#COVID-19']

tweet_count=0

n_tweets = 1000

f=open("D3.txt","w")
f.close

class StdOutListener(StreamListener):
    def on_data(self,data):
        global tweet_count
        global n_tweets
        global stream

        if tweet_count < n_tweets:
            try:

                print(tweet_count,data,"\n")
                tweet_data=json.loads(data)
                if (not tweet_data['retweeted']) and ('RT @' not in tweet_data['text']):
                    pattern1=re.compile(r'\n')
                    tweet_txt=pattern1.sub(r'',tweet_data['text'])
                    pattern2=re.compile(r'RT')
                    tweet=pattern2.sub(r'',tweet_txt)
                    f=open("D3.txt","a+")
                    f.write(str(tweet_data['id'])+"\t"+tweet+"\n")
                    tweet_count+=1
            except BaseException:
                print("Error:",tweet_count,data)
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)

l=StdOutListener()
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
stream=Stream(auth,l)


stream.filter(track=tracklist)