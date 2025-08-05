import os
from dotenv import load_dotenv
import requests


def scrape_user_tweets(twitter_url, count=10, mock=True):
    tweet_list = []
    if mock:
        res = requests.get(
            "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        )
        tweet_list = res.json()
    return tweet_list
    
    
if __name__ == "__main__":
    load_dotenv()
    username = "sid"
    tweets = scrape_user_tweets(username, mock=True)
    for tweet in tweets:
        print(tweet)