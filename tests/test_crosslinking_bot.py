from datetime import datetime
from datetime import date, timedelta

import pytest

from crosslinking_bot import crosslinking_bot as cb
from crosslinking_bot import utils


# Test `cb.parse_date()`

def test_return_today():
    today = datetime.today().date()
    assert 'today' == cb.parse_date(today)

def test_return_1_day_ago():
    yesterday = date.today() - timedelta(1)
    assert '1 day ago' == cb.parse_date(yesterday)

def test_return_2_days_ago():
    two_days_ago = date.today() - timedelta(2)
    assert '2 days ago' == cb.parse_date(two_days_ago)


# Test `cv.prepare_comment()`

@pytest.fixture
def hn_hits():
    return [{
        'objectID': 12135399,
        'created_at_i': 1469823139,
        },
        {
        'objectID': 12135398,
        'created_at_i': 1469821139,
        },
    ]

def test_one_hit_contains_right_url(hn_hits):
    hn_hits = [hn_hits[0]]
    hn_url = cb.HN_STORY.format(hn_hits[0]['objectID'])
    assert hn_url in cb.prepare_comment(hn_hits)

def test_two_hits_contain_second_url(hn_hits):
    hn_url = cb.HN_STORY.format(hn_hits[1]['objectID'])
    assert hn_url in cb.prepare_comment(hn_hits)

def test_two_hits_contain_plural_form(hn_hits):
    hn_url = cb.HN_STORY.format(hn_hits[1]['objectID'])
    assert 'discussions' in cb.prepare_comment(hn_hits)

def test_same_url_even_if_fragment_differs():
    url1 = 'https://example.com/somtehing#nothing'
    url2 = 'https://example.com/somtehing'
    assert utils.same_url(url1, url2) is True

def test_different_urls():
    url1 = 'https://example1.com/somtehing#nothing'
    url2 = 'https://example2.com/somtehing'
    assert utils.same_url(url1, url2) is False

def test_different_urls_different_fragment_path_is_blog():
    url1 = 'https://example.com/blog#one-example'
    url2 = 'https://example.com/blog#two-example'
    assert utils.same_url(url1, url2) is False

def test_same_urls_same_fragment_path_is_blog():
    url1 = 'https://example.com/blog#one-example'
    url2 = 'https://example.com/blog#one-example'
    assert utils.same_url(url1, url2) is True

def test_same_urls_same_fragment_longer_path():
    url1 = 'https://example.com/blog/something#one-example'
    url2 = 'https://example.com/blog/something#two-example'
    assert utils.same_url(url1, url2) is True

def test_different_urls_different_fragment_longer_path():
    url1 = 'https://example.com/blog/something#one-example'
    url2 = 'https://example.com/blog/something#one-example'
    assert utils.same_url(url1, url2) is True
