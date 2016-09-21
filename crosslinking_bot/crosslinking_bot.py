#!/usr/bin/env python3
"""Reddit bot that links to HN submissions

The bot checks the top submissions on /r/machinelearning
and compares the links against all HN submissions using the
Algolia API. The bot posts a new top-level reply if there is 
a relatively active match and links to the HN thread.
"""

import re
import time
import collections
import logging
from datetime import datetime

import praw
import requests

from .sources import HN
from .utils import get_config
from . import parse_args

CONFIG = get_config()
DEBUG = False

REDDIT_LIMIT = 50

HN_ALGOLIA = 'http://hn.algolia.com/api/v1/search?query={}&restrictSearchableAttributes=url' 
HN_STORY = 'https://news.ycombinator.com/item?id={}'

SLEEP_TIME = 60
# Minimum number of comments of an HN story to be considered
COMM_NUM_THRESHOLD = 3

logging.basicConfig(filename='.log',level=logging.DEBUG)

def get_reddit_submissions():
    """Download top `REDDIT_LIMIT` submissions from the /r/machinelearning subreddit.

    Uses Reddit API to get the hottest submissions. Expects `CONFIG`
    in the function scope.

    Returns:
	list: List of relevant praw.objects.Submission.
    """
    r = praw.Reddit(user_agent=CONFIG['agent'])
    r.login(CONFIG['user'], CONFIG['pass'], disable_warning=True)
    submissions = r.get_subreddit('machinelearning').get_hot(limit=REDDIT_LIMIT)
    return [sub for sub in submissions if 'reddit.com' not in sub.url]


def get_common_submissions(reddit_submissions, min_activity=COMM_NUM_THRESHOLD):
    """Get common submissions from various sources

    The function finds submissions to crosslink that are relevant to
    the submissoins provided. At the moment, only Hacker News is 
    considered.

    Args:
        reddit_submissions (iter): Iterable containing `praw` submission objects.
        min_activity (int, optional) Minimum number of comments to consider a
            submission. Default value is taken from the module-level constant
            `COMM_NUM_THRESHOLD`.
    Returns:
        dict: A dict mapping `praw` submission objects to HN hit objects
    """
    hn = HN(reddit_submissions, min_activity)
    return hn.get_common_submissions()

def parse_date(date):
    """Parse date to human readable format

    Args:
        date: `datetime.date` object
    Returns:
        str: human readable relative time
    """
    today = datetime.today().date()
    if date == today:
        return 'today'
    else:
        days_ago = (today - date).days
        plural_suffix = 's' if days_ago > 1 else ''
        return '{} day{} ago'.format(days_ago, plural_suffix)


def prepare_comment(hn_hits):
    """Format the comment from the HN hits

    Comments may get more complex when there are multiple 
    hits, so this function tries to format it neatly.

    Args:
        hn_hits: List of dictionaries containing data
            about the HN hits.

    Returns:
        str: Formatted comment.
    """
    header = 'HN discussion: '
    if len(hn_hits) == 1:
        return header + HN_STORY.format(hn_hits[0]['objectID'])
    else:
        # Change the header to use plural form
        header = re.sub(':', 's:', header)
        header += '\n\n'

        hit_strings = []
        for hit in hn_hits:
            hit_date = datetime.fromtimestamp(hit['created_at_i']).date()
            hit_date_human = parse_date(hit_date)
            url = HN_STORY.format(hit['objectID']) 
            hit_strings.append('{} ({})'.format(url, hit_date_human))

    return header + '\n\n'.join(hit_strings)


def post_comments(common_subs):
    """Post comments on Reddit.

    Posts `len(common_subs)` comments every `SLEEP_TIME` seconds. 

    Args:
        common_subs (dict): Maps `praw` submission objects to HN hit objects.
    """
    for reddit_obj, hn_hits in common_subs.items():
	# If I didn't post here before
        if not any(comm for comm in reddit_obj.comments if CONFIG['user'] in str(comm.author)):
            comment = prepare_comment(hn_hits)
            reddit_obj.add_comment(comment)
            logging.info(comment)
            time.sleep(SLEEP_TIME)

def run_bot():
    parse_args()
    reddit_subs = get_reddit_submissions()
    common_subs = get_common_submissions(reddit_subs)
    post_comments(common_subs)
