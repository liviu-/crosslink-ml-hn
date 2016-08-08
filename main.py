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
from datetime import datetime

import praw
import requests
import urltools

from config import REDDIT_USERNAME, REDDIT_PASS, USER_AGENT

REDDIT_LIMIT = 50

HN_ALGOLIA = 'http://hn.algolia.com/api/v1/search?query={}&restrictSearchableAttributes=url' 
HN_STORY = 'https://news.ycombinator.com/item?id={}'

SLEEP_TIME = 60
# Minimum number of comments of an HN story to be considered
COMM_NUM_THRESHOLD = 3


def get_reddit_submissions():
    """Download top `REDDIT_LIMIT` submissions from the /r/machinelearning subreddit.

    Uses Reddit API to get the hottest submissions. Expects `USER_AGENT`,
    `REDDIT_USERNAME`, and `REDDIT_PASS` in the function scope.

    Returns:
	list: List of relevant praw.objects.Submission.
    """
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)
    submissions = r.get_subreddit('machinelearning').get_hot(limit=REDDIT_LIMIT)
    return [sub for sub in submissions if 'reddit.com' not in sub.url]


def get_common_submissions(reddit_submissions, min_comments=COMM_NUM_THRESHOLD):
    """Filter common HN and /r/machinelearning submissions.

    The function queries the Algolia API for each URL
    in the submissions provided and fetches the HN IDs for submissions 
    that have more than `min_comments` comments.

    Args:
        reddit_submissions (iter): Iterable containing `praw` submission objects.
        min_comments (int, optional) Minimum number of comments to consider a HN
            submission. The default value is taken from the module constant 
            `COMM_NUM_THRESHOLD`.

    Returns:
        dict: A dict mapping `praw` submission objects to HN hit objects
    """
    common_subs = collections.defaultdict(list)

    for reddit_sub in reddit_submissions:
        for hit in requests.get(HN_ALGOLIA.format(reddit_sub.url)).json().get('hits'):
            try:
                if hit['num_comments'] > COMM_NUM_THRESHOLD and urltools.compare(hit['url'], reddit_sub.url):
                    common_subs[reddit_sub].append(hit)
            # `hit['num_comments'] may return `None`
            except TypeError:
                continue
    return common_subs


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
            today = datetime.today().date()
            # Use human readable format for date
            if hit_date == today:
                hit_date_human = 'today'
            else:
                days_ago = (today - hit_date).days
                plural_suffix = 's' if days_ago > 1 else ''
                hit_date_human = '{} day{} ago'.format(days_ago, plural_suffix)

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
        if not any(comm for comm in reddit_obj.comments if REDDIT_USERNAME in str(comm.author)):
            comment = prepare_comment(hn_hits)
            reddit_obj.add_comment(comment)
            time.sleep(SLEEP_TIME)

def main():
    reddit_subs = get_reddit_submissions()
    common_subs = get_common_submissions(reddit_subs)
    post_comments(common_subs)

if __name__ == '__main__':
    main()
