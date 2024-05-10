#open ai make prompt

import random
from datetime import datetime, timedelta

from re import X
from nicegui import app, ui
import asyncio
import requests
import openai
import matplotlib.pyplot as plt
import sqlite3
import nicegui as ng
from nicegui import ui
import tkinter as tk
from flask import Flask, jsonify, request
from functools import wraps
import openai
from PIL import Image, ImageDraw, ImageFont
import secrets
import string
import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt
from flask_mail import Mail, Message
import stripe

# connect to create SQLite database and tables

   

#get from db
openai.api_key = 'sk-proj-rtQZICsVi0rtr1N2m2VST3BlbkFJqP0VjBDVtLqS623ihDhK'

class HashPassword:
    def __init__(self, password):
        self._password = password
        self._hashed_password = self._hash_password()

    def _hash_password(self):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self._password.encode('utf-8'), salt)

    def set_password(self, password):
        self._password = password
        self._hashed_password = self._hash_password()

    def get_hashed_password(self):
        return self._hashed_password

class aiTasks:
    
    def generate_image_from_prompt(prompt, output_path='output_image.png', max_tokens=50):
        # Generate text completion using OpenAI's API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens
        )

        # Extract the text completion from the response
        completion_text = response.choices[0].text.strip()

        # Create an image with the completion text
        image = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20)  # Change font and size as needed
        draw.text((10, 10), completion_text, fill='black', font=font)

        # Save the image to the specified output path
        image.save(output_path)
        print(f"Image generated and saved to {output_path}")

    def generate_text_from_prompt(prompt, max_tokens=50):
        # Generate text completion using OpenAI's API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens
        )
    
        # Example tokens usage:
        prompt_text = "A beautiful sunset over the mountains"
        generate_image_from_prompt(prompt_text, output_path='sunset_image.png', max_tokens=50)
        # Extract the text completion from the response
        completion_text = response.choices[0].text.strip()
        return completion_text



#redo gen text open ai / and images


def get_pexels_images(search_query, api_key, per_page=10):
    # Pexels API endpoint for searching photos
    endpoint = "https://api.pexels.com/v1/search"
    temp_api = "iV4nfFBiLs0hPu72u0nlggWrFzuVHaWdnWGAlK6zCDyE8woYwKfFOKrV"
    
    # Parameters for the API request
    params = {
        'query': search_query,
        'per_page': per_page  # Limit the number of results
    }
    
    # Headers including the API key
    headers = {
        'Authorization': api_key
    }
    
    try:
        # Send GET request to Pexels API
        response = requests.get(endpoint, params=params, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Check if there are any photos matching the search query
            if data['total_results'] > 0:
                # Extract URLs of the photos
                image_urls = [photo['src']['original'] for photo in data['photos']]
                return image_urls
            else:
                print("No images found for the search query:", search_query)
                return []
        else:
            print("Error:", response.status_code)
            return []
    except Exception as e:
        print("An error occurred:", e)
        return []



def choose_URL(url):
    
    if random.random() < .84:
        pass
    else:
        array_of_values = ['t', 'u']
        randChoice = random.choice(array_of_values)
        if randChoice == 't':
            url = getLink().shorten_linkT(url)
        elif randChoice == 'u':
            url = getLink().shorten_linkU(url)
    


class getLink:
    
    def shorten_linkT(self, long_url):
        """
        Shortens a long URL using the Tiny API.

        Args:
            long_url (str): Long URL to be shortened.

        Returns:
            str: Shortened URL.
        """
        base_url = "https://tny.im/api/v1/shorten"
        payload = {"url": long_url}
        response = requests.post(base_url, data=payload)
        if response.status_code == 200:
            return response.json()["short"]
        else:
            return f"Error: {response.text}"

    def shorten_linkU(self, long_url):
        """
        Shortens a long URL using the URLday API.

        Args:
            long_url (str): Long URL to be shortened.

        Returns:
            str: Shortened URL.
        """
        # Replace 'YOUR_API_KEY' with your actual API key
        API_KEY = '7iohIWckUwH2rAwNO3lawO4lmCFwZKpFU4flunm1WBRQ2DKRr0rlyEyW0tR2'
        url_shorten_endpoint = 'https://api.url.day/shorten'
        response = requests.post(url_shorten_endpoint, json={'url': long_url}, headers={'Authorization': f'Bearer {API_KEY}'})
        if response.status_code == 200:
            return response.json()['short_url']
        else:
            return f"Error: {response.json()['message']}"

    
        


def create_linkedin_post(access_token, message):
    # Example of creating a post on LinkedIn
    post_url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    post_body = {
        "author": "urn:li:person:YOUR_LINKEDIN_USER_ID",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(post_url, headers=headers, json=post_body)
    if response.status_code == 201:
        print("Post created successfully!")
    else:
        print("Failed to create post:", response.text)

def create_twitter_post(auth, tweet_text):
    """
    Creates a post (tweet) on Twitter.

    Args:
        auth (OAuth1): OAuth1 object for making authenticated requests.
        tweet_text (str): Text content of the tweet.

    Returns:
        dict: Response JSON from the Twitter API.
    """
    post_url = 'https://api.twitter.com/1.1/statuses/update.json'
    params = {'status': tweet_text}
    response = requests.post(post_url, auth=auth, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to create tweet: {response.text}"}

  
def create_medium_post(access_token, post_content):
    """
    Creates a post on Medium.

    Args:
        access_token (str): Access token for making authenticated requests.
        post_content (str): Content of the post to be created.

    Returns:
        dict: Response JSON from the Medium API.
    """
    # Create post using the authenticated access token
    post_url = 'https://api.medium.com/v1/users/me/posts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'title': 'Sample Title',  # Change as needed
        'contentFormat': 'html',
        'content': post_content,
        'publishStatus': 'public'
    }
    response = requests.post(post_url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create post: {response.text}"}

#tblr

def create_tumblr_post(client, blog_name, post_content):
    """
    Creates a post on Tumblr.

    Args:
        client (pytumblr.TumblrRestClient): Tumblr API client object for making authenticated requests.
        blog_name (str): Name of the Tumblr blog where the post will be created.
        post_content (str): Content of the post to be created. 

    Returns:
        dict: Response JSON from the Tumblr API.
    """
    response = client.create_text(blog_name, state="published", body=post_content)
    return response



def create_blogger_post(access_token, blog_id, post_title, post_content):
    """
    Creates a post on Blogger.

    Args:
        access_token (str): Access token for making authenticated requests.
        blog_id (str): ID of the blog where the post will be created.
        post_title (str): Title of the post.
        post_content (str): Content of the post.

    Returns:
        dict: Response JSON from the Blogger API.
    """
    # Blogger API endpoint for creating a post
    post_url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts'

    # Request headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Request body with the post title and content
    post_body = {
        'title': post_title,
        'content': post_content
    }

    # Send POST request to create the post
    response = requests.post(post_url, headers=headers, json=post_body)

    # Return response JSON
    return response.json()


def create_imgur_post(access_token, image_path, title=''):
    """
    Uploads an image to Imgur and creates a post.

    Args:
        access_token (str): Access token for making authenticated requests.
        image_path (str): Path to the image file    to be uploaded.
        title (str): Title for the Imgur post (optional).

    Returns:
        dict: Response JSON from the Imgur API.
    """
    # Imgur API upload endpoint
    upload_url = 'https://api.imgur.com/3/upload'

    # Request headers with access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Request body with image data
    data = {
        'image': open(image_path, 'rb'),
        'title': title
    }

    # Send POST request to upload image
    response = requests.post(upload_url, headers=headers, data=data)

    # Return response JSON
    return response.json()



def create_flickr_post(access_token, photo_path, title='', description=''):
    """
    Uploads a photo to Flickr and creates a post.

    Args:
        access_token (str): Access token for making authenticated requests.
        photo_path (str): Path to the photo file to be uploaded.
        title (str): Title for the Flickr post (optional).
        description (str): Description for the Flickr post (optional).

    Returns:
        dict: Response JSON from the Flickr API.
    """
    # Flickr API upload endpoint
    upload_url = 'https://www.flickr.com/services/upload/'

    # Request body with access token, photo data, and optional title/description
    data = {
        'photo': open(photo_path, 'rb'),
        'title': title,
        'description': description,
        'oauth_token': access_token,
        'format': 'json',
        'nojsoncallback': 1
    }

    # Send POST request to upload photo
    response = requests.post(upload_url, files=data)

    # Return response JSON
    return response.json()


def create_facebook_post(access_token, message):
    """
    Creates a post on Facebook.

    Args:
        access_token (str): Access token for making authenticated requests.
        message (str): Message content of the post.

    Returns:
        dict: Response JSON from the Facebook Graph API.
    """
    # Facebook Graph API endpoint for creating a post
    post_url = f'https://graph.facebook.com/v12.0/me/feed'

    # Request body with the post message 
    data = {
        'message': message,
        'access_token': access_token
    }

    # Send POST request to create the post
    response = requests.post(post_url, data=data)

    # Return response JSON
    return response.json()



def create_facebook_post(page_access_token, message):
    """
    Creates a post on Facebook Page.

    Args:
        page_access_token (str): Page access token for making authenticated requests.
        message (str): Message content of the post.

    Returns:
        dict: Response JSON from the Facebook Pages API.
    """
    # Facebook API endpoint for creating a post
    post_url = f'https://graph.facebook.com/v12.0/me/feed'

    # Request body with the post message
    data = {
        'message': message,
        'access_token': page_access_token
    }

    # Send POST request to create the post
    response = requests.post(post_url, data=data)

    # Return response JSON
    return response.json()




def create_instagram_post(access_token, caption, image_url):
    """
    Creates a post on Instagram.

    Args:
        access_token (str): Access token for making authenticated requests.
        caption (str): Caption for the Instagram post.
        image_url (str): URL of the image to be posted.

    Returns:
        dict: Response JSON from the Instagram Graph API.
    """
    # Instagram Graph API endpoint for creating a post
    post_url = 'https://graph.instagram.com/me/media'
    
    # Request body with caption and image URL
    data = {
        'caption': caption,
        'image_url': image_url,
        'access_token': access_token
    }

    # Send POST request to create the post
    response = requests.post(post_url, data=data)

    # Return response JSON
    return response.json()



def create_disqus_post(access_token, forum, thread_id, message):
    """
    Creates a post on Disqus.

    Args:
        access_token (str): Access token for making authenticated requests.
        forum (str): Disqus forum name.
        thread_id (str): ID of the thread where the post will be created.
        message (str): Message content of the post.

    Returns:
        dict: Response JSON from the Disqus API.
    """
    # Disqus API endpoint for creating a post
    post_url = 'https://disqus.com/api/3.0/posts/create.json'

    # Request body with access token, forum name, thread ID, and post message
    data = {
        'access_token': access_token,
        'forum': forum,
        'thread': thread_id,
        'message': message
    }

    # Send POST request to create the post
    response = requests.post(post_url, data=data)

    # Return response JSON
    return response.json()





def create_sendie_post(access_token, platform, message):
    """
    Creates a post on Sendie.

    Args:
        access_token (str): Access token for making authenticated requests.
        platform (str): Social media platform where the post will be created (e.g., 'twitter', 'facebook', etc.).
        message (str): Message content of the post.

    Returns:
        dict: Response JSON from the Sendie API.
    """
    # Sendie API endpoint for creating a post
    post_url = 'https://api.sendie.io/post'

    # Request headers with access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Request body with platform and post message
    data = {
        'platform': platform,
        'message': message
    }

    # Send POST request to create the post
    response = requests.post(post_url, headers=headers, json=data)

    # Return response JSON
    return response.json()



def create_mastodon_post(instance_url, access_token, status):
    """
    Creates a post on Mastodon.

    Args:
        instance_url (str): URL of the Mastodon instance (e.g., 'https://mastodon.social').
        access_token (str): Access token for making authenticated requests.
        status (str): Status content of the post.

    Returns:
        dict: Response JSON from the Mastodon API.
    """
    # Mastodon API endpoint for creating a post
    post_url = f'{instance_url}/api/v1/statuses'

    # Request headers with access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Request body with status content
    data = {
        'status': status
    }

    # Send POST request to create the post
    response = requests.post(post_url, headers=headers, data=data)

    # Return response JSON
    return response.json()

#linked in
#POST https://api.linkedin.com/v2/assets?action=registerUpload
#needs to be posted before upload
def editProfilelinkedin():
    payload = {
    "patch": {
        "$set": {
            "FIELD": {
                "originalImage": "urn:li:digitalmediaAsset:C5604AQEMWf4Nl_mf2g",
                "displayImage": "urn:li:digitalmediaAsset:C5616AQEoeGkp7U5GEA",
                "birthDate": {
                "day": bDay,
                "month": bMonth,
                "year": bYear 
                },
                "phoneNumbers" : [{
                    "number": "123-444-5555",
                    "type": "WORK"
                }],
                "vanityName": nickName,
                "websites": [
                {
                    "category": "OTHER",
                    "label": {
                        "localized": {
                            "en_US": websiteURL
                        },
                        "preferredLocale": {
                            "country": "US",
                            "language": "en"
                        }
                    },
                    "url": {
                    "localized": {
                        "en_US": "http://www.linkedin-other.com"
                    },
                    "preferredLocale": {
                        "country": "US",
                        "language": "en"
                    }
                }
                }]



            }
        }
    }
}


def create_facebook_post(access_token, message):
    """
    Creates a post on Facebook.

    Args:
        access_token (str): Access token for making authenticated requests.
        message (str): Message content of the post.

    Returns:
        dict: Response JSON from the Facebook Graph API.
    """
    # Facebook Graph API endpoint for creating a post
    post_url = f'https://graph.facebook.com/v12.0/me/feed'

    # Request body with the post message
    data = {
        'message': message,
        'access_token': access_token
    }

    # Send POST request to create the post
    response = requests.post(post_url, data=data)

    # Return response JSON
    return response.json()


def create_sendie_post(access_token, platform, message):
    # Implement Sendie post creation logic
    pass


    
    

def create_linkedin_post(access_token, message):
    access_token = authenticate_linkedin()
    message = "Hello from the LinkedIn API!"
    create_linkedin_post(access_token, message)

# Medium

def create_medium_post(access_token, post_content):
    # Implement Medium post creation logic
    pass

# Imgur


def create_imgur_post(access_token, image_path, title):
    # Implement Imgur post creation logic
    pass



def create_flickr_post(access_token, photo_path, title, description):
    # Implement Flickr post creation logic
    pass

# Blogger
def blogger_post(api_key):
    
    # Blogger
    api_key = ''
    access_token = blogger_login(api_key)

    blog_id = ''
    post_title = "Hello from the Blogger API!"
    post_content = "This is a test post created using the Blogger API."

    response = create_blogger_post(access_token, blog_id, post_title, post_content)
    print("Response:", response)
   

        
def create_blogger_post(access_token, blog_id, post_title, post_content):
    # Implement Blogger post creation logic
    pass

# Tumblr
def tumblr_login(consumer_key, consumer_secret, access_token, access_token_secret):
    # Implement Tumblr login logic
    pass

def create_tumblr_post(client, blog_name, post_content):
    # Implement Tumblr post creation logic
    pass


   # Flickr
   

    # Instagram


    # Disqus
    
    
   
    
class socialParent:

    def blogger_login(api_key):
        """  
        Logs in to the Blogger API.

        Args:
            api_key (str): API key obtained from the Google Cloud Console.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Blogger API base URL
        base_url = 'https://www.googleapis.com/blogger/v3'

        # Use the API key as the access token
        return api_key

 
    def disqus_login(username, password, api_key, api_secret):
        """
        Logs in to Disqus and obtains an access token.

        Args:
            username (str): Disqus username.
            password (str): Disqus password.
            api_key (str): Disqus API key obtained from the Disqus Developer Dashboard.
            api_secret (str): Disqus API secret obtained from the Disqus Developer Dashboard.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Disqus API authentication endpoint
        auth_url = 'https://disqus.com/api/oauth/2.0/access_token/'

        # Request body with username, password, API key, and API secret
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'api_key': api_key,
            'api_secret': api_secret
        }

        # Send POST request to obtain access token
        response = requests.post(auth_url, data=data)

        # Return access token
        return response.json()['access_token']
    
    def facebook_login(app_id, app_secret, page_id, access_token):
        """
        Logs in to the Facebook Pages API.

        Args:
            app_id (str): App ID obtained from the Facebook Developer Portal.
            app_secret (str): App Secret obtained from the Facebook Developer Portal.
            page_id (str): ID of the Facebook Page where the post will be created.
            access_token (str): Access token with the required permissions.

        Returns:
            str: Page access token for making authenticated requests.
        """
        # Facebook API base URL
        base_url = 'https://graph.facebook.com/v12.0'

        # Generate page access token
        response = requests.get(
            f'{base_url}/{page_id}',
            params={
                'fields': 'access_token',
                'access_token': access_token
            }
        )
        page_access_token = response.json()['access_token']


        return page_access_token


    def flickr_login(api_key, api_secret):
        """
        Logs in to the Flickr API.

        Args:
            api_key (str): API key obtained from the Flickr Developer Portal.
            api_secret (str): API secret obtained from the Flickr Developer Portal.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Flickr API authentication endpoint
        auth_url = 'https://www.flickr.com/services/oauth/request_token'

        # Request body with API key and API secret
        data = {
            'api_key': api_key,
            'api_secret': api_secret,
            'format': 'json',
            'nojsoncallback': 1
        }

        # Send POST request to obtain access token
        response = requests.post(auth_url, data=data)

        # Return access token
        return response.json()['access_token']
    
    def instagram_login(app_id, app_secret, redirect_uri, code):
        """
        Logs in to Instagram and obtains an access token.

        Args:
            app_id (str): Instagram App ID obtained from the Instagram Developer Portal.
            app_secret (str): Instagram App Secret obtained from the Instagram Developer Portal.
            redirect_uri (str): Redirect URI registered with the Instagram App.
            code (str): Authorization code received after the user grants permission.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Instagram API token endpoint
        token_url = 'https://api.instagram.com/oauth/access_token'

        # Request body with app credentials and authorization code
        data = {
            'client_id': app_id,
            'client_secret': app_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code
        }

        # Send POST request to obtain access token
        response = requests.post(token_url, data=data)

        # Return access token
        return response.json()['access_token']

    def imgur_login(client_id, client_secret):
        """
        Logs in to the Imgur API.

        Args:
            client_id (str): Client ID obtained from the Imgur Developer Portal.
            client_secret (str): Client secret obtained from the Imgur Developer Portal.

        Returns:
            dict: Access and refresh tokens for making authenticated requests.
        """
        # Imgur API token endpoint
        token_url = 'https://api.imgur.com/oauth2/token'

        # Request body with client credentials for authentication
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        # Send POST request to obtain access token
        response = requests.post(token_url, data=data)

        # Return access and refresh tokens
        return response.json()
    
   

    def authenticate_linkedin():
        # LinkedIn OAuth 2.0 endpoints
        AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
        ACCESS_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

        # Replace these with your actual values
        CLIENT_ID = "YOUR_CLIENT_ID"
        CLIENT_SECRET = "YOUR_CLIENT_SECRET"
        REDIRECT_URI = "YOUR_REDIRECT_URI"

        # Generate the authorization URL
        authorization_params = {
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'state': 'random_string',
            'scope': 'r_liteprofile w_member_social'
        }
        authorization_url = AUTHORIZATION_URL + '?' + '&'.join([f"{key}={value}" for key, value in authorization_params.items()])

        print("Go to the following URL and authorize access:")
        print(authorization_url)

        # After authorization, you'll be redirected to your redirect URI with a 'code' parameter in the URL
        authorization_code = input("Enter the authorization code from the callback URL: ")

        # Exchange the authorization code for an access token
        access_token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
        }
        response = requests.post(ACCESS_TOKEN_URL, data=access_token_data)

        # Extract the access token from the response
        access_token = response.json()['access_token']

    
    
    def mastodon_login(instance_url, username, password):
        """
        Logs in to Mastodon and obtains an access token.

        Args:
            instance_url (str): URL of the Mastodon instance (e.g., 'https://mastodon.social').
            username (str): Mastodon username.
            password (str): Mastodon password.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Mastodon API token endpoint
        token_url = f'{instance_url}/oauth/token'

        # Request body with username, password, and grant type
        data = {
            'client_id': 'mastodon-python',
            'client_secret': 'mastodon-python',
            'grant_type': 'password',
            'username': username,
            'password': password
        }

        # Send POST request to obtain access token
        response = requests.post(token_url, data=data)

        # Return access token
        return response.json()['access_token']
    

    # medium
    def medium_login(client_id, client_secret, username, password):
        """
        Logs in to the Medium API using OAuth 2.0 authentication.

        Args:
            client_id (str): Medium API client ID.
            client_secret (str): Medium API client secret.
            username (str): Medium account username.
            password (str): Medium account password.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Obtain access token using OAuth 2.0 Password Grant flow
        token_url = 'https://api.medium.com/v1/tokens'
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return None
    
    def pexals_login():
           pass


    def sendie_login(username, password):
        """
        Logs in to Sendie and obtains an access token.

        Args:
            username (str): Sendie username.                                                                                                                                                                                               
            password (str): Sendie password.

        Returns:
            str: Access token for making authenticated requests.
        """
        # Sendie API authentication endpoint
        auth_url = 'https://api.sendie.io/login'

        # Request body with username and password
        data = {
            'username': username,
            'password': password
        }

        # Send POST request to obtain access token
        response = requests.post(auth_url, json=data)

        # Check if login was successful
        if response.status_code == 200:
            return response.json()['token']
        else:
            print("Login failed:", response.text)
            return None
    
    def tumblr_login(consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Logs in to the Tumblr API.

        Args:
            consumer_key (str): Consumer key obtained from the Tumblr Developer Platform.
            consumer_secret (str): Consumer secret obtained from the Tumblr Developer Platform.
            access_token (str): Access token obtained from the Tumblr Developer Platform.
            access_token_secret (str): Access token secret obtained from the Tumblr Developer Platform.

        Returns:
            pytumblr.TumblrRestClient: Tumblr API client object for making authenticated requests.
        """
        client = pytumblr.TumblrRestClient(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )
        return client
    
    
def generate_password(length=12):
    # Define characters to use for password generation
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password using secrets.choice() method
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return password

class UserDictionary:
    def __init__(self):
        self.dictionary = {}

    def add_entry(self, username, numbers_array, user_key):
        # Check if the username already exists in the dictionary
        if username in self.dictionary:
            print(f"Username '{username}' already exists in the dictionary.")
            return
        # Check if the value is an array of numbers
        if not isinstance(numbers_array, list) or not all(isinstance(num, int) for num in numbers_array):
            print("Value must be an array of numbers.")
            return
        # Add the entry to the dictionary
        self.dictionary[username] = {"numbers": numbers_array, "key": user_key}
        print(f"Entry '{username}' added to the dictionary.")

    def get_dictionary(self):
        return self.dictionary
    #-

    
app = Flask(__name__)   
# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://desktop_black.lan:{os.environ.get("api")}@192.168.1.236:port/omniiflask'
db = SQLAlchemy(app)

app.config['STRIPE_PUBLIC_KEY'] = os.environ.get("stripePubKey")
app.config['STRIPE_SECRET_KEY'] = os.environ.get("stripeSecretKey")


@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        email = payment_intent['receipt_email']
        handle_payment_success(payment_intent, email)
    elif event['type'] == 'payment_intent.failed':
        # Payment failed, handle accordingly
        handle_payment_failure(event['data']['object'])

    return jsonify({'status': 'success'})

def handle_payment_success(payment_intent):
    send_prepurchase_email()
    pass

def handle_payment_failure(payment_intent):
    # Handle failed payment
    pass

# Function to send purchase email
def send_prepurchase_email(customer_email, amount):
    msg = Message('Thank you for your purchase!', recipients=[customer_email])
    msg.body = f'Your purchase of ${amount/100:.2f} was successful. Thank you for shopping with us! You will recieved another email with the product on launch day or early release! Keep an eye out! '
    mail.send(msg)



API_KEY = os.environ.get('api')

# Decorator to require API key
def require_api_key(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401
        return view_func(*args, **kwargs)
    return decorated_function

user_dict = UserDictionary()
user_dict.add_entry('apincumbe@gmail.com', [0,1 ], 'esfd23gR#R')

@app.route('/api/userDict', methods=['GET'])
@require_api_key
def get_resource():
    # Retrieve resource from database or elsewhere
    dictionary = user_dict.get_dictionary()
    print(dictionary)
    return jsonify(dictionary)



# Define User and APICredential models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    api_credentials = db.relationship('APICredential', backref='user', uselist=False)

class APICredential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    api_key = db.Column(db.String(50), nullable=False)
    api_secret = db.Column(db.String(50), nullable=False)
    
   
    
# Instantiate HashPassword outside of route functions
# Secret key for encoding/decoding JWT tokens
SECRET_KEY = os.environ.get("secretkey")

def generate_jwt_token(user_id):
    # Set token expiration time (e.g., 1 hour from now)
    expiration_time = datetime.utcnow() + timedelta(hours=1)

    # Create payload for JWT token
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }

    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')  # Decode bytes to string   
   
hash_password_instance = HashPassword()

# Routes for user management
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username is available
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Hash password before storing
    password_hash = hash_password_instance.hash_password(password)

    # Create new user
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct
    if user:
        # Verify password
        if hash_password_instance.verify_password(password, user.password_hash):
            # Generate and return JWT token for authentication
            token = generate_jwt_token(user.id)
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
#db or cache?
#pyinstaller for package.exe
#Stored Procedures and Functions:
#Encapsulating Sensitive Logic and Data:     
 # AES_ENCRYPT() and AES_DECRYPT()

