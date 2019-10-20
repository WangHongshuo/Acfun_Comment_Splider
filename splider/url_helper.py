from email.utils import formatdate


class HeaderHelper:
    header_template = {'Host': 'webapi.acfun.cn',
                       'User-Agent': '',
                       'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Origin': 'https://www.acfun.cn',
                       'Connection': 'keep-alive',
                       'If-Modified-Since': '',
                       'Referer': '',
                       'Cache-Control': 'max-age=0'
                       }

    def __init__(self):
        return

    def get_header(self, user_agent, referer):
        self.header_template['User-Agent'] = user_agent
        self.header_template['Referer'] = referer
        self.header_template['If-Modified-Since'] = formatdate(None, usegmt=True)
        return self.header_template


class ArticlesUrlHelper:
    article_url_template = 'https://webapi.acfun.cn/query/article/list?pageNo={_pageNo}&size=10&realmIds={' \
                           '_realmIds}&originalOnly=false&orderType={_orderType}&periodType={' \
                           '_periodType}&filterTitleImage=true '
    referer_url_template = 'https://www.acfun.cn/v/list{_list_id}/index.htm'

    def __init__(self):
        return

    def get_url(self, realmIds, pageNo=1, orderType=1, periodType=-1):
        realmIds = realmIds.replace(',', '%2C')
        return self.article_url_template.format(_pageNo=pageNo, _realmIds=realmIds, _orderType=orderType,
                                                _periodType=periodType)

    def get_referer_url(self, list_id):
        return self.referer_url_template.format(_list_id=list_id)


class CommentsUrlHelper:
    def __init__(self):
        return
