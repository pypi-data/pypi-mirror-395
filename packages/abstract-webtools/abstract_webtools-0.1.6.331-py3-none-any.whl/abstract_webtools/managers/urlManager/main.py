from .src import *
def get_url_mgr(url=None,url_mgr=None):
    return url_mgr or urlManager(url)
def get_url(url=None,url_mgr=None):
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    return url_mgr.url

