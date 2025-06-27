#!/usr/bin/python3
"""
Reddit API Client Module

This module provides functionality to query Reddit's public API and retrieve
the top 10 hot posts from any specified subreddit. The module handles API
restrictions, invalid subreddits, and various error conditions gracefully.

Functions:
    top_ten(subreddit): Queries Reddit API and prints titles of top 10 hot posts

Author: Reddit API Client
Version: 1.0.0
Dependencies: requests

Example:
    Basic usage:
        >>> from 1-top_ten import top_ten
        >>> top_ten("programming")
        Firebase founder's response to last week's "Firebase Costs increased by 7000%!"
        How a 64k intro is made
        ...
        
    Invalid subreddit:
        >>> top_ten("this_is_fake")
        None
"""
import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print the titles of the first 10 hot posts
    for a given subreddit.
    
    This function makes an HTTP GET request to Reddit's public JSON API endpoint
    for the specified subreddit. It handles various error conditions including
    invalid subreddits, API restrictions, network errors, and malformed responses.
    
    Invalid subreddits are detected through HTTP 302 redirects, which Reddit
    uses to redirect invalid subreddit requests to search results. The function
    explicitly disables redirect following to catch this behavior.
    
    Args:
        subreddit (str): The name of the subreddit to query (e.g., "programming", 
                        "python", "askreddit"). Should not include the "r/" prefix.
        
    Returns:
        None: This function doesn't return a value. It prints either:
              - The titles of up to 10 hot posts, one per line
              - "None" if the subreddit is invalid or an error occurs
              
    Raises:
        No exceptions are raised. All errors are handled internally and result
        in printing "None" to maintain the expected interface behavior.
        
    Examples:
        >>> top_ten("programming")
        Firebase founder's response to last week's "Firebase Costs increased by 7000%!"
        How a 64k intro is made
        HTTPS on Stack Overflow: The End of a Long Road
        ...
        
        >>> top_ten("nonexistent_subreddit_12345")
        None
        
        >>> top_ten("")
        None
        
    Note:
        Reddit may block requests from certain environments (like cloud hosting
        providers) with HTTP 403 Forbidden responses. In such cases, the function
        will print "None" even for valid subreddits.
    """
    # Input validation: Check if subreddit parameter is valid
    if not subreddit or not isinstance(subreddit, str):
        print("None")
        return
    
    # Construct Reddit API endpoint URL for hot posts in JSON format
    # Reddit's public API structure: /r/{subreddit}/hot.json
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    
    # Set User-Agent header to comply with Reddit API requirements
    # Reddit blocks requests without proper User-Agent headers
    # Using browser-like User-Agent for better compatibility
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make HTTP GET request to Reddit API
        # allow_redirects=False: Prevents following redirects to detect invalid subreddits
        # timeout=10: Prevents hanging requests, fails after 10 seconds
        response = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
        
        # Debug: Uncomment next line to see status codes during testing
        # print(f"Debug: Status code: {response.status_code}")
        
        # HTTP 302 (Found/Redirect): Invalid subreddit redirects to search results
        # By disabling redirects, we can detect this condition
        if response.status_code == 302:
            print("None")
            return
        
        # HTTP 403 (Forbidden): Reddit blocks requests from certain environments
        # Common in cloud hosting providers and some network configurations
        if response.status_code == 403:
            print("None")
            return
            
        # HTTP 200 (OK): Only successful responses should be processed
        # Any other status codes indicate an error condition
        if response.status_code != 200:
            print("None")
            return
        
        # Parse JSON response from Reddit API
        # Reddit returns data in JSON format, handle parsing errors gracefully
        try:
            data = response.json()
        except ValueError:
            # Invalid JSON response indicates an error condition
            print("None")
            return
        
        # Validate Reddit API response structure
        # Expected structure: {"data": {"children": [{"data": {"title": "..."}}]}}
        if 'data' not in data or 'children' not in data['data']:
            print("None")
            return
        
        # Extract posts array from Reddit API response
        posts = data['data']['children']
        
        # Verify that the subreddit contains posts
        if not posts:
            print("None")
            return
        
        # Process and print titles of first 10 posts (or all available if less than 10)
        count = min(10, len(posts))
        for i in range(count):
            # Extract post data safely using .get() to handle missing keys
            post_data = posts[i].get('data', {})
            title = post_data.get('title', '')
            
            # Only print non-empty titles
            if title:
                print(title)
        
        # Edge case: If no posts had valid titles, print None
        # This maintains consistent behavior even if posts exist but lack titles
        if count == 0:
            print("None")
            
    except requests.exceptions.RequestException:
        # Handle all requests-related errors:
        # - Network connectivity issues
        # - DNS resolution failures  
        # - Timeout errors
        # - Connection errors
        print("None")
    except Exception:
        # Catch-all for any other unexpected errors
        # Ensures the function never raises exceptions to calling code
        print("None")
