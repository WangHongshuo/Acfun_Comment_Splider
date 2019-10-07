from selenium import webdriver
import time
import copy
from urllib import request
import json
import requests
import os
import gzip


class Comment:
    floor = ""
    user_name = ""
    text = ""

    def Comment(self):
        self.text
        self.floor
        self.name


def get_result_page(url):
    header = {'Host': 'www.acfun.cn',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
              'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Connection': 'keep-alive',
              'DNT': '1',
              'Referer': 'https://www.acfun.cn/a/ac11301146',
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
    url = 'https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId=11301146&sourceType=3&page=1&pivotCommentId=0&newPivotCommentId=0'
    result = get_result_page(url)
    # 解析评论json
    js = json.loads(result)
    b = 2
    a = 1


if __name__ == '__main__':
    main()
