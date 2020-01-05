from url_helper import HeaderHelper, ArticlesUrlHelper
from url_config import ARTICLE_ZONE
from article_helper import ArticleHelper, Article
from comment_helper import CommentHelper
from urllib import request
import json
import gzip
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
# 支持 MySQL的UNSIGNED INTEGER
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BIGINT
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# Comments表
class SQLComments(Base):
    __tablename__ = "comments"
    cid = Column(BIGINT(unsigned=True), autoincrement=False, primary_key=True)
    # 使用server_default='0'设置默认值为0，需要是字符串
    aid = Column(BIGINT(unsigned=True), nullable=False, server_default='0')
    floor_num = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    uid = Column(BIGINT(unsigned=True), nullable=False, server_default='0')
    content = Column(VARCHAR(1000), nullable=True)

    def __repr__(self):
        tpl = "comments(cid = {}, aid = {}, floor_num = {}, uid = {}, content = {}"
        return tpl.format(self.cid, self.aid, self.floor_num, self.uid, self.content)


# articles表
class SQLArticles(Base):
    __tablename__ = "articles"
    aid = Column(BIGINT(unsigned=True), autoincrement=False, primary_key=True)
    comment_count = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    latest_floor = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
    latest_comment_time = Column(BIGINT(unsigned=True), nullable=False, server_default='0')

    def __repr__(self):
        tpl = "articles(aid = {}, comment_count = {}, latest_floor = {}"
        return tpl.format(self.aid, self.comment_count, self.latest_floor, self.latest_comment_time)


def save_comments_to_DB(session, comments):
    for cl in comments.data:
        # 封禁的用户评论仍然可被爬，且cid = 0，cid为主键
        if cl.cid == 0:
            continue
        session.add(SQLComments(cid=str(cl.cid),
                                aid=str(comments.article_id),
                                floor_num=str(cl.floor_num),
                                uid=str(cl.uid),
                                content=str(cl.content)))


def main():
    engine = create_engine('mysql+pymysql://root:q123456@localhost:3306/acfun_comments')
    # 创建comments表和articles表
    Session = sessionmaker(bind=engine)
    session = Session()

    article_helper = ArticleHelper()
    article_list = article_helper.get_article_list(ARTICLE_ZONE[0].get('list_id'), ARTICLE_ZONE[0].get('realmIds'))
    comment_helper = CommentHelper()
    comments = None
    for al in article_list:
        # 爬取前检查数据库中是否存在article信息，和是否需要更新
        al = Article(12190119, 26, '1', 1577634368000, 26)
        ret = session.query(SQLArticles).filter(SQLArticles.aid == al.aid).scalar()
        # 不存在则新建
        if ret is None:
            comments = comment_helper.get_comments_by_aid(al.aid, 0)
            al.latest_floor = comments.latest_floor()
            session.add(SQLArticles(aid=str(al.aid),
                                    comment_count=str(al.comment_count),
                                    latest_floor=str(al.latest_floor),
                                    latest_comment_time=str(al.latest_comment_time)))
        # 数据库中评论上次更新时间落后于最新时间则更新
        elif ret.latest_comment_time < al.latest_comment_time:
            comments = comment_helper.get_comments_by_aid(al.aid, ret.latest_floor)
            ret = session.query(SQLArticles).filter(SQLArticles.aid == al.aid).update(
                {SQLArticles.comment_count: ret.comment_count + comments.size(),
                 SQLArticles.latest_floor: comments.latest_floor(),
                 SQLArticles.latest_comment_time: al.latest_comment_time}
            )
        save_comments_to_DB(session, comments)
        print(comments)
        break
    session.commit()

    a = 1


if __name__ == '__main__':
    main()
