from urllib import request
from url_helper import HeaderHelper
import json
import gzip
import time
import math


class Comment:

    def __init__(self, cid: int, floor_num: int, content: str, aid: int, uid: int) -> None:
        # comment id
        self.cid = cid
        self.floor_num = floor_num
        # user id
        self.uid = uid
        self.content = content
        # article id
        self.aid = aid

    def __str__(self):
        return 'aid: ' + str(self.aid) + ' floor: ' + str(self.floor_num) + ' cid: ' + str(self.cid) + ' uid: ' + str(
            self.uid) + '\n' + 'content: ' + self.content + '\n'


class CommentHelper:
    comments_list = list()
    url_template = 'https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId={_aid}&sourceType=3&' \
                   'page={_page}&pivotCommentId=0&newPivotCommentId=0&_ts={_ts}'

    __comments_js_list = list()
    __is_updated = False

    def __init__(self):
        self.header_helper = HeaderHelper()
        return

    def __get_comments_json(self, aid: int, curr_page: int, ts: int = None) -> dict:
        """
获取指定页评论json
        :param aid: 文章ID
        :param curr_page: 当前页面号
        :param ts: 时间戳，默认为当前时间
        :return: 解析好的json
        """
        if ts is None:
            ts = int(math.floor(time.time() * 1000))
        header = self.header_helper.get_comments_header(aid)
        url = self.url_template.format(_aid=aid, _page=curr_page, _ts=ts)
        data = None
        rq = request.Request(url, data=data, headers=header)
        res = request.urlopen(rq)
        respond = res.read()
        # 解决乱码问题
        respond = gzip.decompress(respond)
        result = str(respond, encoding="utf-8")
        return json.loads(result)

    def __get_comment_floor_in_curr_page_js(self, js: dict, index: int) -> int:
        """
获取该评论也第index个评论的楼层
        :param js: 评论json
        :param index: 评论index
        :return: 楼层
        """
        return js['commentsMap']['c' + str(js['commentIds'][index])]['floor']

    def __get_comments_js_list(self, aid: int, last_floor: int = 0) -> list:
        """
获取指定评论页所有json
        :param aid: 文章ID
        :return: 解析好的json list
        """
        self.__comments_js_list.clear()
        # 首次请求确认评论总页数
        js = self.__get_comments_json(aid, 1)
        if js['totalCount'] > 0:
            total_page_num = js['totalPage']
            curr_page = js['curPage']
            # 暂存所有评论js
            while curr_page <= total_page_num:
                js = self.__get_comments_json(aid, curr_page)
                self.__comments_js_list.append(js)
                # 检查last_floor是在当前评论页内
                first_floor_in_curr_page = self.__get_comment_floor_in_curr_page_js(js, 0)
                last_floor_in_curr_page = self.__get_comment_floor_in_curr_page_js(js, -1)
                if first_floor_in_curr_page < last_floor or \
                   first_floor_in_curr_page >= last_floor >= last_floor_in_curr_page:
                    break
                # 每次检查总页数是否变化
                total_page_num = js['totalPage']
                curr_page = curr_page + 1
        return self.__comments_js_list

    def __get_comments_from_js(self, js: dict, aid: int, last_floor: int = 0) -> list:
        """
从解析好的json中获取评论
        :param js: 解析好的json
        :param aid: 文章ID
        :param last_floor: 最后一个评论的楼层，解析终止条件
        :return: 评论list
        """
        dic_comments_map = js['commentsMap']
        # js['commentsMap']里包含引用的楼层，js['commentIds']为该page每层楼最底层评论的cid
        for cid in js['commentIds']:
            dic_comment = dic_comments_map['c' + str(cid)]
            # 检查是否爬取到上次楼层（该楼层可能被删）
            if dic_comment['floor'] <= last_floor:
                return self.comments_list
            # 添加评论到list
            self.comments_list.append(
                Comment(dic_comment['cid'], dic_comment['floor'], dic_comment['content'], aid, dic_comment['userId']))
        return self.comments_list

    def get_all_comments_by_aid(self, aid: int) -> list:
        """
根据文章ID获取评论
        :param aid: 文章ID
        :return: 评论list
        """
        self.comments_list.clear()
        self.__get_comments_js_list(aid)
        for cjl in self.__comments_js_list:
            self.comments_list = self.__get_comments_from_js(cjl, aid)
        return self.comments_list

    def get_new_comments_by_aid(self, aid: int, last_floor: int) -> list:
        """
根据上次更新的楼层增量式抓取新增楼层评论list
        :param aid: 文章ID
        :param last_floor: 上次抓取到的最后楼层
        :return: 新增评论list
        """
        self.comments_list.clear()
        self.__get_comments_js_list(aid, last_floor)
        for cjl in self.__comments_js_list:
            self.comments_list = self.__get_comments_from_js(cjl, aid, last_floor)
        return self.comments_list
