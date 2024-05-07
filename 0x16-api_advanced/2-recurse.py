#!/usr/bin/python3
import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively fetches the titles of all hot articles for a given subreddit.
    Returns a list of titles, or None if the subreddit is invalid.
    """
    # Set a custom User-Agent to avoid rate-limiting issues with Reddit's API
    headers = {
        "User-Agent": "custom-reddit-script/1.0"
    }

    # Define the endpoint for fetching hot articles, with 'after' for pagination
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    if after:
        url += f"&after={after}"

    try:
        # Make a GET request to the Reddit API with the appropriate headers
        response = requests.get(url, headers=headers, allow_redirects=False)

        # If the status code is 200, it's a valid subreddit
        if response.status_code == 200:
            data = response.json()
            articles = data['data']['children']

            # Append the titles to the hot_list
            for article in articles:
                hot_list.append(article['data']['title'])

            # Check if there's an 'after' token for further recursion
            after = data['data']['after']
            if after:
                # Recursively call the function with the new 'after' token
                return recurse(subreddit, hot_list, after)
            else:
                # If there's no 'after', recursion ends, return the list of titles
                return hot_list
        else:
            return None  # Invalid subreddit, return None

    except requests.exceptions.RequestException:
        return None  # Handle exceptions and return None if there's an error
