from urllib import request
from url_helper import HeaderHelper
import json
import gzip
import time
import math


class Comment:

    def __init__(self, cid, floor_num, user_name, content, aid, uid):
        # comment id
        self.cid = cid
        self.floor_num = floor_num
        self.user_name = user_name
        # user id
        self.uid = uid
        self.content = content
        # article id
        self.aid = aid

    def __str__(self):
        return 'aid: ' + str(self.aid) + ' floor: ' + str(self.floor_num) + ' cid: ' + str(self.cid) + ' uid: ' + str(
            self.uid) + ' user_name: ' + self.user_name + '\n' + 'content: ' + self.content + '\n'


def get_comments_json(url, header):
    data = None
    rq = request.Request(url, data=data, headers=header)
    res = request.urlopen(rq)
    respoen = res.read()
    # 解决乱码问题
    respoen = gzip.decompress(respoen)
    result = str(respoen, encoding="utf-8")
    return json.loads(result)


class CommentHelper:
    comments_list = list()
    url_template = 'https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId={_aid}&sourceType=3&' \
                   'page={_page}&pivotCommentId=0&newPivotCommentId=0&_ts={_ts}'

    def __init__(self):
        self.header_helper = HeaderHelper()
        return

    def get_comments(self, aid):
        self.comments_list.clear()
        ts = int(math.floor(time.time() * 1000))
        url = self.url_template.format(_aid=aid, _page=1, _ts=ts)
        header = self.header_helper.get_comments_header(aid)
        js = get_comments_json(url, header)
        # 采集方式在某些情况（如大量新评论出现）会导致评论漏采
        if js['totalCount'] > 0:
            dic_comments_map = js['commentsMap']
            total_page_num = js['totalPage']
            curr_page = js['curPage']
            while curr_page <= total_page_num:
                # 读取curr_page和total_page_num
                total_page_num = js['totalPage']
                curr_page = js['curPage']
                dic_comments_map = js['commentsMap']
                # js['commentsMap']里包含引用的楼层，js['commentIds']为该page每层楼最底层评论的cid
                for cid in js['commentIds']:
                    dic_comment = dic_comments_map['c' + str(cid)]
                    self.comments_list.append(Comment(dic_comment['cid'], dic_comment['floor'], dic_comment['userName'],
                                                      dic_comment['content'], aid, dic_comment['userId']))
                curr_page = curr_page + 1

                ts = int(math.floor(time.time() * 1000))
                url = self.url_template.format(_aid=aid, _page=curr_page, _ts=ts)
                js = get_comments_json(url, header)
        return self.comments_list
