from urllib import request
import json
import gzip
from email.utils import formatdate


class Article:

    def __init__(self, aid, comment_count, title, last_floor=0):
        # article id
        self.aid = aid
        self.comment_count = comment_count
        self.title = title
        self.last_floor = last_floor

    def __str__(self):
        return 'https://www.acfun.cn/a/ac' + str(self.aid) + '\n' + 'comment_count: ' + str(self.comment_count) + \
               'last_floor: ' + str(self.last_floor) + '\n' + self.title + '\n '


class ArticleHelper:
    article_list = list()

    def __init__(self):
        return

    def get_article_list_by_json(self, js):
        self.article_list.clear()
        data = None
        if js['message'] == 'OK' and js['code'] == 200:
            data = js['data']
        if data != None:
            total_page = data['totalPage']
            dic_article_list = data['articleList']
            page_No = data['pageNo']
            for a in dic_article_list:
                # str深浅拷贝问题
                self.article_list.append(Article(a['id'], a['comment_count'], a['title']))
        return self.article_list
