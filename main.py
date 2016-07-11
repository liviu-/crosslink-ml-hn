#!/usr/bin/env python3

import time

import praw
import requests

# Import username and password
from config import *

HN_LIMIT = 100
REDDIT_LIMIT = 50

HN_TOP_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
HN_ITEM = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
HN_STORY = 'https://news.ycombinator.com/item?id={}'

SLEEP_TIME = 60

def get_reddit_submissions():
    r = praw.Reddit(user_agent='crosslink_hackernews')
    r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)
    submissions = r.get_subreddit('machinelearning').get_hot(limit=REDDIT_LIMIT)

    return [sub for sub in submissions
	if 'reddit.com' not in sub.url]

def get_hn_submissions():
    # Makes a request for each story, but couldn't find
    # a better way through their API
    hn_items = [requests.get(HN_ITEM.format(id)).json()
                for id in requests.get(HN_TOP_URL).json()[:HN_LIMIT]]

    return [(hn_story.get('url'), hn_story['id']) for hn_story in hn_items]

# Couldn't find a satisfying way to normalize urls,
def get_common_submissions(reddit_subs, hn_subs):
    return [
        (reddit_sub, hn_sub[1])
        for reddit_sub in reddit_subs for hn_sub in hn_subs
        if hn_sub[0] == reddit_sub.url
    ]

def post_comment(common_subs):
    for common_sub in common_subs:
        if not any(comm for comm in common_sub[0].comments if REDDIT_USERNAME in str(comm.author)):
            common_sub[0].add_comment('HN discussion: {}'.format(HN_STORY.format(common_sub[1])))
            time.sleep(SLEEP_TIME)

def main():
    reddit_subs = get_reddit_submissions()
    hn_subs = get_hn_submissions()
    common_subs = get_common_submissions(reddit_subs, hn_subs)
    post_comment(common_subs)

if __name__ == '__main__':
    main()
