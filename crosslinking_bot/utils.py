import urltools
from urllib.parse import urlparse

def same_url(url1, url2):
    """Check if 2 URLs refer to the same primary resource

    `urltools.compare()` fails if the 2 URLs have different fragments.
    See issue #8 for details.

    Args:
        url1 (str): First URL to be compared
        url2 (str): Second URL

    Returns:
        bool: Whether the URLs are the same
    """
    _, netloc1, path1, *rest = urlparse(url1)
    _, netloc2, path2, *rest = urlparse(url2)
    return urltools.compare(netloc1 + path1, netloc2 + path2)
