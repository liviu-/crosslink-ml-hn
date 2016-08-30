import urltools
from urllib.parse import urlparse

def same_url(url1, url2):
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
    exception_path = '/blog'

    _, netloc1, path1, params1, query1, fragment1 = urlparse(url1)
    _, netloc2, path2, params2, query2, fragment2 = urlparse(url2)
    if netloc1 == netloc2 and path1 == path2 == exception_path:
        return fragment1 == fragment2
    return urltools.compare(netloc1 + path1, netloc2 + path2)
