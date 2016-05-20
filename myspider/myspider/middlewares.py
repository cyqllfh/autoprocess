import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from myspider import settings

class RotateUserAgentMiddleware(object):

    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)

        if ua:
            print "*******Current UserAgent:%s************" %ua
            request.headers.setdefault('User-Agent', ua)


class MyProxyMiddleware(object):

    def __init__(self):
        self.proxy_list = settings.PROXY_LIST
        with open(self.proxy_list) as f:
            self.proxies = [ip.strip() for ip in f]
            print self.proxies

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))
        print "@@@@@@@@@@@@@@@" + request.meta['proxy'] +"@@@@@@@@@@@@@@@"