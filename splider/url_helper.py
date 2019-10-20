
class HeaderHelper:
    article_header_template = {'Host': 'webapi.acfun.cn',
                       'User-Agent': '',
                       'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Origin': 'https://www.acfun.cn',
                       'Connection': 'keep-alive',
                       'Referer': '',
                       'Cache-Control': 'max-age=0'
                               }
    comments_header_template = {'Host': 'www.acfun.cn',
                                'User-Agent': "",
                                'Accept': 'application/json, text/plain, */*',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                                'Connection': 'keep-alive',
                                'DNT': '1',
                                'Referer': "",
                                'TE': 'Trailers'
    }
    article_referer_url_template = 'https://www.acfun.cn/v/list{_list_id}/index.htm'
    comments_referer_url_template = 'https://www.acfun.cn/a/ac{_aid}'
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'

    def __init__(self):
        return

    def get_article_header(self, list_id, user_agent=None):
        if user_agent is None:
            user_agent = self.default_user_agent;
        self.article_header_template['User-Agent'] = user_agent
        self.article_header_template['Referer'] = self.article_referer_url_template.format(_list_id=list_id)
        return self.article_header_template

    def get_comments_header(self, aid, user_agent=None):
        if user_agent is None:
            user_agent = self.default_user_agent
        self.comments_header_template['User-Agent'] = user_agent
        self.comments_header_template['Referer'] = self.comments_referer_url_template.format(_aid=aid)
        return self.comments_header_template


class ArticlesUrlHelper:
    article_url_template = 'https://webapi.acfun.cn/query/article/list?pageNo={_pageNo}&size=10&realmIds={' \
                           '_realmIds}&originalOnly=false&orderType={_orderType}&periodType={' \
                           '_periodType}&filterTitleImage=true '


    def __init__(self):
        return

    def get_url(self, realmIds, pageNo=1, orderType=1, periodType=-1):
        realmIds = realmIds.replace(',', '%2C')
        return self.article_url_template.format(_pageNo=pageNo, _realmIds=realmIds, _orderType=orderType,
                                                _periodType=periodType)

class CommentsUrlHelper:
    url_template = 'https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId={_aid}&sourceType=3&page={_page}&pivot'

    def __init__(self):
        return


