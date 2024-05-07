#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, after="", counts={}):
    """
    Queries the Reddit API, parses the titles of all hot articles,
    and counts the occurrences of given keywords.
    """
    # Set a custom User-Agent to avoid issues with Reddit's API
    headers = {
        "User-Agent": "custom-reddit-script/1.0"
    }

    # Define the endpoint for hot articles, including 'after' to support recursion
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    if after:
        url += f"&after={after}"

    try:
        # Make a GET request to the Reddit API with the appropriate headers
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            return None  # Invalid subreddit, return nothing

        # Parse the JSON response to get the hot articles
        data = response.json()
        articles = data['data']['children']

        # Convert all keywords in word_list to lowercase and create a frequency map
        word_list_lower = [word.lower() for word in word_list]

        for article in articles:
            # Get the title of each article
            title = article['data']['title'].lower()  # Lowercase for case-insensitive comparison

            # Count occurrences of each word in the title
            for keyword in word_list_lower:
                keyword_count = title.split().count(keyword)  # Count exact matches
                if keyword_count > 0:
                    if keyword in counts:
                        counts[keyword] += keyword_count
                    else:
                        counts[keyword] = keyword_count

        # Check if there is an 'after' token for recursion
        after = data['data']['after']
        if after:
            # Recursive call to get more articles
            count_words(subreddit, word_list, after, counts)

        # At the end of recursion, sort and print the counts
        if after is None:
            # Sort by count (descending), then by keyword (ascending) if counts are equal
            sorted_counts = sorted(
                counts.items(),
                key=lambda item: (-item[1], item[0])
            )

            for keyword, count in sorted_counts:
                print(f"{keyword}: {count}")

    except requests.exceptions.RequestException:
        return None
