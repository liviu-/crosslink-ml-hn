import re
import os

import yaml
import urltools
from urllib import parse

# Environment variable pointing to the config file
config_environ = 'CROSSLINKING_CONFIG'
default_path = os.path.join(os.path.expanduser("~"), '.crosslinking_config.yaml')

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
    fragment_identifier = '#'

    url1 = _parse_url(raw_url1)
    url2 = _parse_url(raw_url2)

    # If it's on arxiv, do some acrobatics
    if url1['netloc'] == url2['netloc'] == arxiv_exception:
        regex = '([^/a-z]+\.[^/a-z.]+)'
        return re.findall(regex, url1['path']) == re.findall(regex, url2['path'])
    else:
        return urltools.compare(_normalize_url(raw_url1), _normalize_url(raw_url2))

def _parse_url(url):
    """Parse URL into a dictionary"""
    url_dict = {}

    parsed_result = parse.urlparse(url)
    for key, value in zip(parsed_result._fields, parsed_result):
        url_dict[key] = value if key != 'query' else parse.parse_qs(value)

    return url_dict

def _normalize_url(url):
    """Remove fragment from an URL"""
    return url.split('#', 1)[0]

def get_config():
    """Read config file and return Python dictionary"""
    config_file = os.environ.get(config_environ) or default_path
    with open(config_file) as f:
        config = yaml.load(f)
    return config 

