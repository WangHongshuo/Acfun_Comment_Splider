from urllib import request
import json
import gzip
from email.utils import formatdate


class Article:

    def __init__(self, aid, comment_count, last_floor):
        # article id
        self.aid = aid
        self.comment_count = comment_count
        self.last_floor = last_floor

    def __str__(self):
        return 'https://www.acfun.cn/a/ac' + str(self.aid) + '\n' + 'comment_count: ' + str(
            self.comment_count) + '\n' + 'last_floor: ' + str(self.last_floor) + '\n'


class ArticleHelper:
    article_list = list()

    def __init__(self, url):
        # article id
        self.url = url

    def set_url(self, url):
        self.url = url

    def execute(self):
        self.article_list.clear()
