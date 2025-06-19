#!/usr/bin/env python3
# X（旧Twitter）投稿用スクリプト
import requests
from requests_oauthlib import OAuth1
import os
import sys

PREFIX = "[post-to-x.py]"

def log(msg):
    print(f"{PREFIX} {msg}")

def post_to_x(message, api_key, api_secret, access_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"  # X公式API
    auth = OAuth1(
        api_key,
        api_secret,
        access_token,
        access_token_secret
    )
    data = {"text": message}
    try:
        response = requests.post(url, auth=auth, json=data)
        log(f"Status Code: {response.status_code}")
        log(f"Response: {response.text}")
        if response.status_code == 201:
            log("Post to X successful!")
            return True
        else:
            log(f"Failed to post to X: {response.text}")
            return False
    except Exception as e:
        log(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        log("Usage: post-to-x.py <message>")
        sys.exit(1)
    message = sys.argv[1]
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_SECRET")

    if not all([message, api_key, api_secret, access_token, access_token_secret]):
        log("Error: Required X credentials not set")
        sys.exit(1)

    log("=== Debug Information ===")
    log(f"Message: {message}")
    log("========================")
    if message:
        message = message.replace('\\n', '\n')
    success = post_to_x(message, api_key, api_secret, access_token, access_token_secret)
    sys.exit(0 if success else 1) 