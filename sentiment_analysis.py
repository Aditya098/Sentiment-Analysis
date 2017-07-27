import plotly as py
py.tools.set_credentials_file(username='adityac564', api_key='r0oOvo7yWphavCbFEoMG') # plotly username and API key
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as plotly_tools
from plotly.graph_objs import *
py.sign_in("adityac564", "r0oOvo7yWphavCbFEoMG")

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'Dl6Xl0Xh3ydmcV9bw3Pvr94B4'                              # Twitter API key and access token
        consumer_secret = 'flrjl36HbaLj3s2zFo8Mzkxv9Lzbmx7KcQLwDlYbDcsegZj91G'
        access_token = '809633084370886657-He6d90EMjqSEfU87A7a0EmFcl1T9Yo9'
        access_token_secret = 'Cv37nNYgIDBvdn0KBiVS0CAhTftQ1bzrflSwyz4Q8jjFU'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets                          here the query is OnePlus change it to your requirement  
    tweets = api.get_tweets(query = 'OnePlus', count = 200)  # you can increase the count for more acurate result 
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    nutweets = len(tweets) - len(ntweets) - len(ptweets)
    
    print("Neutral tweets percentage: {} %".format(100*nutweets/len(tweets)))
  
    ptweetper = 100*len(ptweets)/len(tweets)
    ntweetper = 100*len(ntweets)/len(tweets)
    nutweetper = 100*nutweets/len(tweets)
    
    labels = ['Positive_tweets','Negative_tweets','Neutral_Tweets']
    values = [ptweetper,ntweetper,nutweetper]       #you can see a demo pie chart at 
    trace = go.Pie(labels=labels, values=values)    #https://plot.ly/~adityac564/40/#plot
    py.iplot([trace], filename='sentiment_analysis_OnePlus')
   
 
if __name__ == "__main__":
    # calling main function
    main()


