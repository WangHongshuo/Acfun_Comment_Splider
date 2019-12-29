import gzip
import json
from urllib import request

from url_helper import HeaderHelper, ArticlesUrlHelper


class Article:

    def __init__(self, aid: int, comment_count: int, title: str, latest_comment_time: int, latest_floor: int = 0) -> None:
        # article id
        self.aid = aid
        self.comment_count = comment_count
        self.title = title
        self.latest_floor = latest_floor
        self.latest_comment_time = latest_comment_time

    def __str__(self):
        return 'https://www.acfun.cn/a/ac' + str(self.aid) + '\n' + 'comment_count: ' + str(self.comment_count) + \
               ' latest_floor: ' + str(self.latest_floor) + ' latest_comment_time: ' + str(self.latest_comment_time) + \
               '\n' + self.title + '\n '


class ArticleHelper:
    article_list = list()

    __article_url_helper = ArticlesUrlHelper()
    __header_helper = HeaderHelper()
    __js = dict()

    def __init__(self):
        return

    def get_article_list(self, list_id: int, realm_ids: int, user_agent: str = None) -> list:
        """
获取文章列表
        :param list_id: 文章list_id，详见url_config.py
        :param realm_ids: 领域realm_id，详见url_config.py
        :param user_agent: user_agent
        :return: 文章列表list
        """
        header = self.__header_helper.get_article_header(list_id, user_agent)
        article_url = self.__article_url_helper.get_url(realm_ids)
        data = None
        rq = request.Request(article_url, data=data, headers=header)
        res = request.urlopen(rq)
        respond = res.read()
        # 解决乱码问题
        respond = gzip.decompress(respond)
        result = str(respond, encoding="utf-8")
        self.__js = json.loads(result)
        return self.__get_article_list_by_json()

    def __get_article_list_by_json(self) -> list:
        """
通过json获取文章列表
        :return: 文章列表list
        """
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
                self.article_list.append(Article(a['id'], a['comment_count'], a['title'], a['latest_comment_time']))
        return self.article_list
