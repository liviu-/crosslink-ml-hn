#!/usr/bin/env python3

import time
import collections

import praw
import requests

# Import username and password
from config import *

HN_LIMIT = 100
REDDIT_LIMIT = 50

HN_URL = "http://hn.algolia.com/api/v1/search?query={}&restrictSearchableAttributes=url" 
HN_STORY = 'https://news.ycombinator.com/item?id={}'

SLEEP_TIME = 60
COMM_NUM_THRESHOLD = 3

def get_reddit_submissions():
    r = praw.Reddit(user_agent='crosslink_hackernews')
    r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)
    submissions = r.get_subreddit('machinelearning').get_hot(limit=REDDIT_LIMIT)

    return [sub for sub in submissions
	if 'reddit.com' not in sub.url]

def get_common_submissions(reddit_submissions):
    commons = collections.defaultdict(list)
    for sub in reddit_submissions:
        hn_hits = requests.get(HN_URL.format(sub.url)).json()['hits']
        for hit in hn_hits:
            if hit['num_comments'] > COMM_NUM_THRESHOLD:
                commons[sub].append(hit['objectID'])
    return commons

def post_comments(common_subs):
    for reddit_obj, hn_ids in common_subs.items():
	# If I didn't post here before
        if not any(comm for comm in reddit_obj.comments if REDDIT_USERNAME in str(comm.author)):
            hn_urls = [HN_STORY.format(hn_id) for hn_id in hn_ids]
            reddit_obj.add_comment('HN discussion: {}'.format('\n'.join(hn_urls)))
            time.sleep(SLEEP_TIME)

def main():
    reddit_subs = get_reddit_submissions()
    common_subs = get_common_submissions(reddit_subs)
    post_comments(common_subs)

if __name__ == '__main__':
    main()
