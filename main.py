#!/usr/bin/env python3
"""Reddit bot that links to HN submissions

The bot checks the top submissions on /r/machinelearning
and compares the links against all HN submissions using the
Algolia API. The bot posts a new top-level reply if there is 
a relatively active match and links to the HN thread.
"""

import time
import collections

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
	list: List of relevant praw.orjects.Submission.
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
        dict: A dict mapping `praw` submission objects to HN story IDs.
    """
    # TODO Expand to loops for readability 
    return {reddit_sub:hit['objectID'] for reddit_sub in reddit_submissions
            for hit in requests.get(HN_ALGOLIA.format(reddit_sub.url)).json().get('hits', [])
            if hit['num_comments'] > COMM_NUM_THRESHOLD
            and urltools.compare(hit['url'], reddit_sub.url)}


def post_comments(common_subs):
    """Post comments on Reddit.

    Posts `len(common_subs)` comments every `SLEEP_TIME` seconds. 

    Args:
        common_subs (dict): Maps `praw` submission objects to HN story IDs.
    """
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
