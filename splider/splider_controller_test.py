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
        # 爬取前检查数据库中是否存在article信息，和是否需要更新
        al = Article(12190119, 27, '1', 1577634368000, 27)
        ret = session.query(SQLArticles).filter(SQLArticles.aid == al.aid).scalar()
        # 不存在则新建
        if ret is None:
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
            al.latest_floor = comment_list[0].floor_num
            print(al)
            session.add(SQLArticles(aid=str(al.aid),
                                    comment_count=str(al.comment_count),
                                    latest_floor=str(al.latest_floor),
                                    latest_comment_time=str(al.latest_comment_time)))
        elif ret.latest_comment_time <= al.latest_comment_time:
            comment_list = comment_helper.get_new_comments_by_aid(al.aid, al.latest_floor)
            for cl in comment_list:
                if cl.cid == 0:
                    continue
                session.add(SQLComments(cid=str(cl.cid),
                                        aid=str(cl.aid),
                                        floor_num=str(cl.floor_num),
                                        uid=str(cl.uid),
                                        content=str(cl.content)))
            al.latest_floor = comment_list[0].floor_num
            ret = session.query(SQLArticles).filter(SQLArticles.aid == al.aid).update(
                {SQLArticles.comment_count: ret.comment_count + len(cl),
                 SQLArticles.latest_floor: al.latest_floor,
                 SQLArticles.latest_comment_time: al.latest_comment_time}
            )

        break
    session.commit()

    a = 1


if __name__ == '__main__':
    main()
