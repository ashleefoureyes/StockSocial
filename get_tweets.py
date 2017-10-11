import tweepy
from textblob import TextBlob

# Gain Twitter access
api_key = 'PDEIa5zExerTYtpgc7hnrJmaF'
api_key_secret = 'gTv1kP5msxoX3WC2ZrBwlbLXdxthLqFqoa1W5ZYPCcAVhlObJO'
access_token = '917857438505865216-BusHvSeDVEZOXoUZSIgBt1UNZAWBxKy'
access_token_secret = 'VvEr5GI3XqeHVGK7vdNPMW5jlbSgl9UctexCwAl1ZE8qt'

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

user = tweepy.API(auth)

def stock_sentiment(quote, num_tweets):
    # Checks if the sentiment for our quote is positive
    tweet_list = user.search(quote, count=num_tweets)
    positive, null = 0, 0

    for tweet in tweet_list:
        blob = TextBlob(tweet.text).sentiment
        if blob.subjectivity == 0:
            null += 1
            next
        if blob.polarity > 0:
            positive += 1
        print(tweet_list)

    if positive > ((num_tweets - null) / 2):
        return True

