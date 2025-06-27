#!/usr/bin/python3
"""
Module containing top_ten function to query Reddit API
"""
import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print the titles of the first 10 hot posts
    for a given subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to query
        
    Returns:
        None: Prints the titles or "None" if invalid subreddit
    """
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return
    
    # Reddit API endpoint for hot posts
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Custom User-Agent header to comply with Reddit API requirements
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make request without following redirects
        # Invalid subreddits may redirect to search results
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
        
        # Debug: Uncomment next line to see status codes during testing
        # print(f"Debug: Status code: {response.status_code}")
        
        # Check if we got a redirect (invalid subreddit)
        if response.status_code == 302:
            print("None")
            return
        
        # Check for forbidden access (common in cloud environments)
        if response.status_code == 403:
            print("None")
            return
            
        # Check for successful response
        if response.status_code != 200:
            print("None")
            return
        
        # Parse JSON response
        try:
            data = response.json()
        except ValueError:
            print("None")
            return
        
        # Validate response structure
        if 'data' not in data or 'children' not in data['data']:
            print("None")
            return
        
        posts = data['data']['children']
        
        # Check if we have any posts
        if not posts:
            print("None")
            return
        
        # Print titles of first 10 posts (or all if less than 10)
        count = min(10, len(posts))
        for i in range(count):
            post_data = posts[i].get('data', {})
            title = post_data.get('title', '')
            if title:
                print(title)
        
        # If we have less than 10 posts but still have some, that's valid
        # If we have no posts with titles, print None
        if count == 0:
            print("None")
            
    except requests.exceptions.RequestException:
        # Handle network errors, timeouts, etc.
        print("None")
    except Exception:
        # Handle any other unexpected errors
        print("None")
