from url_helper import HeaderHelper, ArticlesUrlHelper
from url_config import ARTICLE_ZONE
from article_helper import ArticleHelper
from comment_helper import CommentHelper
from urllib import request
import json
import gzip
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
# 支持 MySQL的UNSIGNED INTEGER
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# Comments表
class SQLComments(Base):
    __tablename__ = "comments"
    cid = Column(INTEGER(unsigned=True), autoincrement=False, primary_key=True)
    # 使用server_default='0'设置默认值为0，需要是字符串
    aid = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    floor_num = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    uid = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    content = Column(VARCHAR(1000), nullable=True)

    def __repr__(self):
        tpl = "comments(cid = {}, aid = {}, floor_num = {}, uid = {}, content = {}"
        return tpl.format(self.cid, self.aid, self.floor_num, self.uid, self.content)


# articles表
class SQLArticles(Base):
    __tablename__ = "articles"
    aid = Column(INTEGER(unsigned=True), autoincrement=False, primary_key=True)
    comment_count = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    last_floor = Column(INTEGER(unsigned=True), nullable=False, server_default='0')

    def __repr__(self):
        tpl = "articles(aid = {}, comment_count = {}, last_floor = {}"
        return tpl.format(self.aid, self.comment_count, self.last_floor)


def get_article_last_comment_floor(session, aid: int) -> int:
    ret = session.query(SQLArticles).filter_by(aid=str(aid)).all()
    if len(ret) == 1:
        return ret[0].last_floor
    return -1


def main():
    engine = create_engine('mysql+pymysql://root:q123456@localhost:3306/acfun_comments')
    # 创建comments表和articles表
    Session = sessionmaker(bind=engine)
    session = Session()

    article_helper = ArticleHelper()
    article_list = article_helper.get_article_list(ARTICLE_ZONE[0].get('list_id'), ARTICLE_ZONE[0].get('realmIds'))
    comment_helper = CommentHelper()

    for al in article_list:
        # 爬取前检查数据库中是否存在

        comment_list = comment_helper.get_all_comments_by_aid(al.aid)
        for cl in comment_list:
            # 封禁的用户评论仍然可被爬，且cid = 0，cid为主键

            if cl.cid == 0:
                continue
            session.add(SQLComments(cid=str(cl.cid),
                                    aid=str(cl.aid),
                                    floor_num=str(cl.floor_num),
                                    uid=str(cl.uid),
                                    content=str(cl.content)))
        session.commit()
        al.last_floor = comment_list[0].floor_num
        session.add(SQLArticles(aid=str(al.aid),
                                comment_count=str(al.comment_count),
                                last_floor=str(al.last_floor)))
    session.commit()

    a = 1


if __name__ == '__main__':
    main()
