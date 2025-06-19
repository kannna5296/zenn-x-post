import requests
from requests_oauthlib import OAuth1
import json
import os
import sys

def post_tweet(message, api_key, api_secret, access_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    
    # OAuth 1.0a認証を設定
    auth = OAuth1(
        api_key,
        api_secret,
        access_token,
        access_token_secret
    )
    
    data = {
        "text": message
    }
    
    try:
        response = requests.post(url, auth=auth, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("Tweet posted successfully!")
            return True
        else:
            print(f"Failed to post tweet: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    message = os.environ.get("MESSAGE")
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_SECRET")
    
    if not all([message, api_key, api_secret, access_token, access_token_secret]):
        print("Error: Required Twitter credentials not set")
        sys.exit(1)
    
    # デバッグ情報を表示
    print("=== Debug Information ===")
    print(f"Message: {message}")
    print("========================")
    
    # 改行を正しく処理
    if message:
        message = message.replace('\\n', '\n')
    
    success = post_tweet(message, api_key, api_secret, access_token, access_token_secret)
    sys.exit(0 if success else 1) 