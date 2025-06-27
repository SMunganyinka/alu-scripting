#!/usr/bin/python3
"""
This module contains a function `top_ten(subreddit)` that queries
the Reddit API and prints the titles of the first 10 hot posts
listed for the given subreddit.
"""

import requests

def top_ten(subreddit):
    """Prints the top 10 hot post titles of a subreddit, or does nothing if invalid."""
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return

    json_data = response.json()
    posts = json_data.get('data', {}).get('children', [])

    if not posts:
        return

    for post in posts:
        print(post.get('data', {}).get('title', ''))
