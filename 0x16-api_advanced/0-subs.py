#!/usr/bin/python3
import requests

def number_of_subscribers(subreddit):
    """
    Returns the number of subscribers for a given subreddit.
    If the subreddit is invalid, return 0.
    """
    # Define the endpoint to get subreddit information
    url = f"https://www.reddit.com/r/{subreddit}/about.json"

    # Set a custom User-Agent to avoid issues with Reddit's API
    headers = {
        "User-Agent": "custom-reddit-script/1.0"
    }

    try:
        # Make a GET request to the Reddit API with the appropriate headers
        response = requests.get(url, headers=headers, allow_redirects=False)

        # If the response status code is 200, it's a valid subreddit
        if response.status_code == 200:
            # Extract the number of subscribers from the JSON response
            data = response.json()
            return data['data']['subscribers']
        else:
            # If the response status code is not 200, it's likely an invalid subreddit
            return 0

    except requests.exceptions.RequestException:
        # Handle exceptions, return 0 in case of an error
        return 0
