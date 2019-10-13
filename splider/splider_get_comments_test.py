from urllib import request
import json
import gzip
import time
import math


class Comment:
    # comment id
    cid = ""
    # comment floor
    floor = ""
    # user id
    uid = ""
    user_name = ""
    content = ""
    # article id
    aid = ""

    def __init__(self, cid, floor, user_name, content, aid, uid):
        self.cid = cid
        self.floor = floor
        self.user_name = user_name
        self.content = content
        self.aid = aid
        self.uid = uid

    def __str__(self):
        return 'aid: ' + str(self.aid) + ' floor: ' + str(self.floor) + ' cid: ' + str(self.cid) + ' uid: ' + str(self.uid) + ' user_name: ' + self.user_name + '\n' + 'content: ' + self.content + '\n'

def get_result_page(url, user_agent, referer):
    header = {'Host': 'www.acfun.cn',
              'User-Agent': user_agent,
              'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Connection': 'keep-alive',
              'DNT': '1',
              'Referer': referer,
              'TE': 'Trailers'
    }
    data = None
    rq = request.Request(url, data=data, headers=header)
    res = request.urlopen(rq)
    respoen = res.read()
    # 解决乱码问题
    respoen = gzip.decompress(respoen)
    result = str(respoen, encoding="utf-8")
    return result


def main():

    start_time = time.time();

    url_template = 'https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId={_aid}&sourceType=3&page={_page}&pivotCommentId=0&newPivotCommentId=0&_ts={_ts}'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    aid = 11165378
    page = 1
    ts = int(math.floor(time.time() * 1000))
    url = url_template.format(_aid = aid, _page = page, _ts = str(ts))

    referer = 'https://www.acfun.cn/a/ac' + str(aid)
    result = get_result_page(url, user_agent, referer)
    # 解析评论json
    js = json.loads(result)
    comment_list = list()

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
                comment_list.append(Comment(dic_comment['cid'], dic_comment['floor'], dic_comment['userName'], dic_comment['content'], aid, dic_comment['userId']))
            curr_page = curr_page + 1

            ts = int(math.floor(time.time() * 1000))
            url = url_template.format(_aid = aid, _page = curr_page, _ts = ts)
            result = get_result_page(url, user_agent, referer)
            js = json.loads(result)
    print('采集时间: ' + str(time.time() - start_time) + 's')
    for c in comment_list:
        print(c)

    b = 2
    a = 1


if __name__ == '__main__':
    main()
