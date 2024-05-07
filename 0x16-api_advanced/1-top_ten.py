#!/usr/bin/python3
# This is the shebang to ensure the script is executed with Python 3

import requests

def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a given subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    headers = {
        "User-Agent": "custom-reddit-script/1.0"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            for post in posts[:10]:
                print(post['data']['title'])
        else:
            print("None")

    except requests.exceptions.RequestException:
        print("None")
