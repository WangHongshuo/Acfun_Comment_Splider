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

# 判断数据库是否存在
def is_database_exist(databases, database_name):
    for d in databases:
        if (database_name == d._row[0]):
            return True
    return False


def main():
    engine = create_engine('mysql+pymysql://root:q123456@localhost:3306/')

    # 判断数据库是否存在
    ret = engine.execute("show databases")
    databases = ret.fetchall();
    if not is_database_exist(databases, 'acfun_comments'):
        ret = engine.execute("create database acfun_comments")
    engine = create_engine('mysql+pymysql://root:q123456@localhost:3306/acfun_comments')

    # 创建comments表和articles表
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
