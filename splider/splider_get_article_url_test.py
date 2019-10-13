from urllib import request
import json
import gzip
from email.utils import formatdate
import copy


class Article:
    aid = ""
    title = ""
    comment_count = ""

    def __init__(self, aid, title, comment_count):
        self.aid = aid
        self.title = title
        self.comment_count = comment_count

    def __str__(self):
        return 'https://www.acfun.cn/a/ac' + str(self.aid) + '\n' + self.title + '\n' + 'comment_count: ' + str(self.comment_count) + '\n'


def get_result_page(url, user_agent, referer):
    df = formatdate(None, usegmt=True)
    header = {'Host': 'webapi.acfun.cn',
              'User-Agent': user_agent,
              'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Origin': 'https://www.acfun.cn',
              'Connection': 'keep-alive',
              'If-Modified-Since': df,
              'Referer': referer,
              'Cache-Control': 'max-age=0'
              }
    data = None
    rq = request.Request(url, data=data, headers=header)
    res = request.urlopen(rq)
    respoen = res.read()
    # 解决乱码问题
    respoen = gzip.decompress(respoen)
    result = str(respoen, encoding="utf-8")
    return result

def get_realmIds_by_list_id(_list_id):
    # 110 - 综合 - 5,22,3,4
    if _list_id == 110:
        return '5%2C22%2C3%2C4'
    # 73 - 情感 - 25,34,7,6,17,1,2
    if _list_id == 73:
        return '25%2C34%2C7%2C6%2C17%2C1%2C2'
    # 64 - 游戏 - 8,11,43,44,45,46
    if _list_id == 64:
        return '8%2C11%2C43%2C44%2C45%2C46'

def main():
    pageNo = 1
    # 110 - 综合； 73 - 情感； 64 - 游戏
    list_id = 110
    realmIds = get_realmIds_by_list_id(list_id)
    # 1 - 最新动态； 2 - 最新发表； 3 - 最热文章
    orderType = 1
    # 仅在最热文章下（orderType == 3）排序有效，其他默认为-1：-1 - 时间不限； 0 - 24小时； 1 - 三天； 2 - 一周； 3 - 一个月
    periodType = -1
    url = 'https://webapi.acfun.cn/query/article/list?pageNo={_pageNo}&size=10&realmIds={' \
          '_realmIds}&originalOnly=false&orderType={_orderType}&periodType={_periodType}&filterTitleImage=true '
    url = url.format(_pageNo = pageNo, _realmIds = realmIds, _orderType = orderType, _periodType = periodType)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    referer = 'https://www.acfun.cn/v/list' + str(list_id) + '/index.htm'
    result = get_result_page(url, user_agent, referer)
    # 解析文章列表json
    js = json.loads(result)
    article_list = list()
    data = None
    if (js['message'] == 'OK' and js['code'] == 200):
        data = js['data']
    if data != None:
        total_page = data['totalPage']
        dic_article_list = data['articleList']
        page_No = data['pageNo']
        for a in dic_article_list:
            # str深浅拷贝问题
            article_list.append(Article(a['id'], a['title'], a['comment_count']))

    for a in article_list:
        print(a)


    b = 2
    a = 1


if __name__ == '__main__':
    main()
