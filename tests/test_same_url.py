from crosslinking_bot import utils

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
