import requests
import tweepy
import pandas as pd

#Scraper
api_key = '73ad2775501f6f792b4d899a239f6d0f'
consumer_key = 'tBDoWzkyNvWF1xF1fDveUuBo2'
consumer_secret = 'hTMtYZwsEWRG2belcdx3kzGvOcG3QkPuYAda4B158lOIvhVg0g'
access_token = '1659597294931689473-zbgYJCSbeSMYhkdJO430x7CETVqiyU'
access_token_secret = 'qrm0KbZ4UNpQZiVCCygk1sIYOAAqifEJeYtAdRLSGWv8L'

def scrape_tweets(api_key, query, num_tweets):
    payload = {
        'api_key': api_key,
        'query': query,
        'num': num_tweets
    }

    response = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            return data.get('organic_results', [])
        except json.decoder.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
    else:
        print(f"API Error: Status Code {response.status_code}")
    return []

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

#input
twitter_username = 'affairs_royal'

num_tweets_to_fetch = 100

try:
    user = api.get_user(screen_name=twitter_username)
    user_details = {
        "User Name": user.name,
        "Description": user.description,
        "Location": user.location,
        "Followers Count": user.followers_count
    }
    print("User Details:")
    for key, value in user_details.items():
        print(f"{key}: {value}")
except tweepy.TweepError as e:
    print(f"Error fetching user details: {str(e)}")

tweets = scrape_tweets(api_key, f'from:{twitter_username}', num_tweets_to_fetch)

if tweets:
    tweet_data = []
    for tweet in tweets:
        tweet_data.append([tweet['position'], tweet['title'], tweet['link'], tweet['snippet']])
    
    columns = ["Position", "Title", "Link", "Snippet"]
    df = pd.DataFrame(tweet_data, columns=columns)
    
    df.to_csv('tweet.csv', index=False)

    print("\nTweets:")
    print(df)
else:
    print("No tweets retrieved.")