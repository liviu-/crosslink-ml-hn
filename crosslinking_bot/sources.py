"""Sources to check for common links

This module constains different discussion sources that the bot uses
to find potential relevant links to crosslink.
"""
import collections
from abc import ABCMeta, abstractmethod

import requests

from . import utils

MIN_ACTIVITY = 3


class Source(object):
    """Abstract clas for discussion sources to subclass
    
    There is some common functionality between different
    sources, so this serves as a starting point for them.
    """
    __metaclass__ = ABCMeta

    def __init__(self, reddit_submissions, min_activity=MIN_ACTIVITY):
        """Constructor to store shared variables for different sources

        Args:
            self.reddit_submissions (iter): Iterable containing `praw` submission objects.
            self.min_comments (int, optional) Minimum number of comments to consider a 
                submission.
        """
        self.reddit_subs = reddit_submissions
        self.min_activity = min_activity

    @abstractmethod
    def get_common_submissions(self):
        pass


class HN(Source):
    """Hacker News source

    Args:
        _hn_algolia (str): Links to the API used for retrieving
            HN common submissions
    """
    _hn_algolia = ('http://hn.algolia.com/api/v1/search?'
                   'query={}&restrictSearchableAttributes=url')

    def get_common_submissions(self):
        """Filter common HN and /r/machinelearning submissions.

        The method queries the Algolia API for each URL
        in the submissions provided and fetches the HN IDs for submissions 
        that have more than `min_comments` comments.


        Returns:
            dict: A dict mapping `praw` submission objects to HN hit objects
        """
        common_subs = collections.defaultdict(list)

        for reddit_sub in self.reddit_subs:
            for hit in requests.get(self._hn_algolia.format(reddit_sub.url)).json().get('hits', []):
                try:
                    if (hit['num_comments'] > self.min_activity and 
                        utils.same_url(hit['url'], reddit_sub.url)):
                        common_subs[reddit_sub].append(hit)
                # `hit['num_comments'] may return `None`
                except TypeError:
                    continue
        return common_subs

class RedditStats(Source):
    """/r/statistics source """

    def get_common_submissions(self):
        pass
