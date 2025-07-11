#!/usr/bin/python3
"""
Module to query the Reddit API and print the titles of the first 10 hot posts.
"""
import requests

def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        None: Prints the titles or None if the subreddit is invalid.
    """
    # Reddit API endpoint for hot posts in a subreddit
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    # Set a custom User-Agent to avoid Too Many Requests errors.
    # Reddit API best practices recommend a unique and descriptive User-Agent.
    headers = {
        "User-Agent": "my-custom-user-agent/1.0"
    }

    try:
        # Make a GET request to the Reddit API.
        # allow_redirects=False is crucial to avoid following redirects for invalid subreddits.
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=5)

        # Check if the request was successful (status code 200)
        # and if it's not a redirect (status code not 3xx).
        if response.status_code == 200:
            data = response.json()

            # Check if 'data' and 'children' keys exist in the response
            if 'data' in data and 'children' in data['data']:
                posts = data['data']['children']

                # Print the titles of the first 10 posts
                for i, post in enumerate(posts):
                    if i < 10:  # Ensure we only print up to 10 titles
                        title = post['data']['title']
                        print(title)
                    else:
                        break # Stop after 10 titles
            else:
                # This case might occur if the subreddit exists but has no posts
                # or if the JSON structure is unexpected.
                print("None")
        elif response.status_code == 404 or (300 <= response.status_code < 400):
            # If status is 404 (Not Found) or a redirect (3xx), it's an invalid subreddit.
            print("None")
        else:
            # Handle other potential HTTP errors
            print(f"Error: Received status code {response.status_code}")
            print("None")

    except requests.exceptions.RequestException as e:
        # Catch any request-related exceptions (e.g., network issues, timeouts)
        print(f"An error occurred: {e}")
        print("None")
 except ValueError:
        # Catch JSON decoding errors if the response is not valid JSON
        print("Error: Could not decode JSON response.")
        print("None")

