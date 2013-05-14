#!/bin/false

import oauth2 as oauth
import os
import simplejson
import time
import re
import datetime

class RequestError(Exception):
    """Exception raised for errors in request."""


class twitter_stat():

    BASELINE_WORD = 'tessellate'
    CREDENTIALS_FILE = './credentials.priv'

    def __init__(self):
        self.search_url = 'https://api.twitter.com/1.1/search/tweets.json?&result_type=recent&include_entities=false&lang=en'
        self.exceptions = { 
            200 : 'Success!',
            400 : 'Bad Request: The request was invalid',
            401 : 'Unauthorized: Authentication credentials were missing or incorrect',
            403 : 'Forbidden: The request is understood, but it has been refused or access is not allowed',
            404 : 'Not Found: The URI requested is invalid or the resource requested does not exists',
            406 : 'Not Acceptable: Invalid format is specified in the request',
            410 : 'Gone: This resource is gone',
            420 : 'Enhance Your Calm:  You are being rate limited',
            422 : 'Unprocessable Entity: Image unable to be processed',
            429 : 'Too Many Requests: Request cannot be served due to the application\'s rate limit having been exhausted for the resource',
            500 : 'Internal Server Error: Something is broken',
            502 : 'Bad Gateway: Twitter is down or being upgraded',
            503 : 'Service Unavailable: The Twitter servers are up, but overloaded with requests',
            504 : 'Gateway timeout: The request couldn\'t be serviced due to some failure wi'
        }
        credentials = {}
        if os.path.exists(twitter_stat.CREDENTIALS_FILE):
            with open(twitter_stat.CREDENTIALS_FILE, 'r') as f:
                for line in f:
                    line = line.replace('\n', '').split(':')
                    credentials[line[0]] = line[1]
        print credentials
        consumer = oauth.Consumer(key = credentials['consumer_key'], secret = credentials['consumer_secret'])
        token = oauth.Token(key = credentials['access_token'], secret = credentials['access_token_secret'])
        self.client = oauth.Client(consumer, token)

    def get_recent_statuses(self, search_term, number):
        suffix = '&q=%s&count=%d' % (search_term.lower(), number)
        response, content = self.client.request(self.search_url + suffix , 'GET')
        if response['status'] != '200':
            print self.search_url + suffix
            raise RequestError(self.exceptions[int(response['status'])])
        content = simplejson.loads(content)
        return content

    def get_ambient_temperature(self):
        content = self.get_recent_statuses(twitter_stat.BASELINE_WORD, 100)
        min_time = min([ status['created_at'] for status in content['statuses'] ])
        min_time = min_time.replace(' +0000', '')
        min_time = time.mktime(datetime.datetime.strptime(min_time, "%a %b %d %H:%M:%S %Y").timetuple())
        return min_time

    def get_temperature(self, search_term):
        content = self.get_recent_statuses(search_term, 100)
        min_time = min([ status['created_at'] for status in content['statuses'] ])
        min_time = min_time.replace(' +0000', '')
        min_time = time.mktime(datetime.datetime.strptime(min_time, "%a %b %d %H:%M:%S %Y").timetuple())
        print search_term, ':', min_time
        return min_time - self.get_ambient_temperature()