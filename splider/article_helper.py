import gzip
import json
from urllib import request

from url_helper import HeaderHelper, ArticlesUrlHelper

class Article:

    def __init__(self, aid, comment_count, title, last_floor=0):
        # article id
        self.aid = aid
        self.comment_count = comment_count
        self.title = title
        self.last_floor = last_floor

    def __str__(self):
        return 'https://www.acfun.cn/a/ac' + str(self.aid) + '\n' + 'comment_count: ' + str(self.comment_count) + \
               ' last_floor: ' + str(self.last_floor) + '\n' + self.title + '\n '


class ArticleHelper:
    article_list = list()

    __article_url_helper = ArticlesUrlHelper()
    __header_helper = HeaderHelper()
    __js = dict()

    def __init__(self):
        return

    def get_article_list(self, list_id, realm_ids, user_agent=None):
        header = self.__header_helper.get_article_header(list_id, user_agent)
        article_url = self.__article_url_helper.get_url(realm_ids)
        data = None
        rq = request.Request(article_url, data=data, headers=header)
        res = request.urlopen(rq)
        respoen = res.read()
        # 解决乱码问题
        respoen = gzip.decompress(respoen)
        result = str(respoen, encoding="utf-8")
        self.__js = json.loads(result)
        return self.__get_article_list_by_json()

    def __get_article_list_by_json(self):
        self.article_list.clear()
        data = None
        if self.__js['message'] == 'OK' and self.__js['code'] == 200:
            data = self.__js['data']
        if data != None:
            total_page = data['totalPage']
            dic_article_list = data['articleList']
            page_No = data['pageNo']
            for a in dic_article_list:
                # str深浅拷贝问题
                self.article_list.append(Article(a['id'], a['comment_count'], a['title']))
        return self.article_list
