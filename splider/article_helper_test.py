from article_helper import ArticleHelper
from url_config import ARTICLE_ZONE

def main():

    article_helper = ArticleHelper()
    article_list = article_helper.get_article_list(ARTICLE_ZONE[0].get('list_id'), ARTICLE_ZONE[0].get('realmIds'))

    # 存入 articles sql的内容：aid（唯一）, comment_count（用于判断是否更新comments sql）
    for a in article_list:
        print(a)

    b = 2
    a = 1


if __name__ == '__main__':
    main()
