import re

import urltools
from urllib import parse


def same_url(raw_url1, raw_url2):
    """Check if 2 URLs refer to the same primary resource

    `urltools.compare()` fails if the 2 URLs have different fragments.
    See issue #8 for details. The function treats a special case where
    the path is simply '/blog' to accommodate some blogs that refer to
    their posts via the fragment.

    Args:
        url1 (str): First URL to be compared
        url2 (str): Second URL

    Returns:
        bool: Whether the URLs are the same
    """
    arxiv_exception = 'arxiv.org'
    query_field_exception = 'id'

    url1 = parse_url(raw_url1)
    url2 = parse_url(raw_url2)

    if url1['netloc'] == url2['netloc'] and url1['path'] == url2['path']:
        # If one of the query field is `id`, parse the value
        if query_field_exception in url1['query'] and query_field_exception in url2['query']:
            return (parse.unquote(url1['query'][query_field_exception][0]) == 
                    parse.unquote(url2['query'][query_field_exception][0]))
        else:
            return urltools.compare(url1['netloc'] + url1['path'], url2['netloc'] + url2['path'])
    # If it's on arxiv, do some acrobatics
    elif url1['netloc'] == url2['netloc'] == arxiv_exception:
        regex = '([^/a-z]+\.[^/a-z.]+)'
        return re.findall(regex, url1['path']) == re.findall(regex, url2['path'])
    else:
        return urltools.compare(url1['netloc'] + url1['path'], url2['netloc'] + url2['path'])

def parse_url(url):
    """Parse URL into a dictionary"""
    url_dict = {}

    parsed_result = parse.urlparse(url)
    for key, value in zip(parsed_result._fields, parsed_result):
        url_dict[key] = value if key != 'query' else parse.parse_qs(value)

    return url_dict
