#!/usr/bin/python3
"""
Module to query the Reddit API for hot posts in a given subreddit.
"""
import requests

def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        None: Prints the titles or None if the subreddit is invalid or
              an error occurs.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "my_custom_user_agent/1.0"  # Custom User-Agent to identify your app
    }
    params = {
        "limit": 10  # Request only the first 10 hot posts
    }

    try:
        # Make the GET request, disallowing redirects
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=5)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Navigate through the JSON structure to get post titles
            if 'data' in data and 'children' in data['data']:
                posts = data['data']['children']
                if not posts:
                    # If there are no posts, it might still be a valid subreddit
                    # but with no content. For this problem, we print None.
                    print("None")
                    return

                for post in posts:
                    if 'data' in post and 'title' in post['data']:
                        print(post['data']['title'])
                    else:
                        print("None") # Should not happen with valid data structure
            else:
                # If the expected data structure is not found
                print("None")
        else:
            # If status code is not 200 (e.g., 404 for invalid subreddit, or redirect)
            print("None")

    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print("None")
        # For debugging: print(f"An error occurred: {e}")
    except ValueError:
        # Handle JSON decoding errors
        print("None")
        # For debugging: print("Failed to decode JSON response.")
