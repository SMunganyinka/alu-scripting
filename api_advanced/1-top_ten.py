#!/usr/bin/python3
"""Script that fetches the top 10 hot posts for a given subreddit."""
import requests


def top_ten(subreddit):
    """Prints the top 10 hot post titles of a subreddit, or does nothing if invalid."""
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return  # Don't print 'None'

    json_data = response.json()
    posts = json_data.get('data', {}).get('children', [])

    if not posts:
        return  # Don't print 'None'

    for post in posts:
        print(post.get('data', {}).get('title', ''))

