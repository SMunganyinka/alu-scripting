#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
for a given subreddit. Prints nothing if the subreddit is invalid.
"""

import requests


def top_ten(subreddit):
    """Print titles of the first 10 hot posts for a subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "python:alx:0.1 (by /u/yourusername)"}
    params = {"limit": 10}

    try:
        response = requests.get(url, headers=headers,
                                params=params,
                                allow_redirects=False,
                                timeout=10)
        if response.status_code != 200:
            return

        posts = response.json().get("data", {}).get("children", [])
        for post in posts:
            print(post.get("data", {}).get("title"))

    except Exception:
        pass
