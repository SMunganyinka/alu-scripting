#!/usr/bin/python3
""" top_ten.py """
import requests


def top_ten(subreddit):
    """ prints the titles of the first 10 hot posts listed in a subreddit """
    url = 'https://www.reddit.com/r/{}/hot.json?limit=10'.format(subreddit)
    headers = {'User-Agent': 'Chrome/1.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    # print(response)
    print(response.text[189097:])
    if response.status_code != 200:
        print(None)
    else:
        posts = response.json().get('data').get('children')
        for post in posts:
            print(post['data']['title'])
