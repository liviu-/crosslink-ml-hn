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

def test_arxiv_same_resource_abs_pdf():
    url1 = 'https://arxiv.org/abs/1608.03282'
    url2 = 'https://arxiv.org/pdf/1608.03282.pdf'
    assert utils.same_url(url1, url2) is True

def test_arxiv_same_resource_ftp_abs():
    url1 = 'https://arxiv.org/ftp/arxiv/papers/1608/1608.03282.pdf'
    url2 = 'https://arxiv.org/abs/1608.03282'
    assert utils.same_url(url1, url2) is True

def test_arxiv_same_resource_abs_pdf_different_versions():
    # It's questionable whether those 2 refer to the same resource
    url1 = 'https://arxiv.org/abs/1608.03282'
    url2 = 'https://arxiv.org/pdf/1608.03282v2.pdf'
    assert utils.same_url(url1, url2) is True

def test_arxiv_same_resource_pdf_different_versions():
    # It's questionable whether those 2 refer to the same resource
    url1 = 'https://arxiv.org/pdf/1608.03282.pdf'
    url2 = 'https://arxiv.org/pdf/1608.03282v2.pdf'
    assert utils.same_url(url1, url2) is True

def test_plos_different_resource_same_base_query():
    url1 = 'http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004485'
    url2 = 'http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004961'
    assert utils.same_url(url1, url2) is False

def test_plos_same_resource():
    url1 = 'http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004485'
    url2 = 'http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004485'
    assert utils.same_url(url1, url2) is True

def test_plos_same_resource_different_encoding():
    url1 = 'http://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0141854'
    url2 = 'http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0141854'
    assert utils.same_url(url1, url2) is True

def test_different_resource_same_base_uses_id_query():
    url1 = 'http://journals.plos.org/article?id=1000'
    url2 = 'http://journals.plos.org/plosone/article?id=1000'
    assert utils.same_url(url1, url2) is False
