from url_helper import HeaderHelper, ArticlesUrlHelper
from url_config import ARTICLE_ZONE

def main():
    article_url_helper = ArticlesUrlHelper()
    header_helper = HeaderHelper()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'

    referer_url = article_url_helper.get_referer_url(ARTICLE_ZONE[0].get('list_id'))
    header = header_helper.get_header(user_agent, referer_url)
    article_url = article_url_helper.get_url(ARTICLE_ZONE[0].get('realmIds'))

    a = 1

if __name__ == '__main__':
    main()