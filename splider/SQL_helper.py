from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
# 支持 MySQL的UNSIGNED INTEGER
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import sessionmaker
import re

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

# SQLHelper整体应考虑防注入
class SQLHelper:
    __engine = None
    __login_cmd = 'mysql+pymysql://{_username}:{_password}@localhost:3306/{_database_name}'
    __username = str()
    __password = str()

    def __init__(self):
        return

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__engine = create_engine(self.__login_cmd.format(_username=username, _password=password, _database_name=''))
        return

    def __check_database(self):
        ret = self.__engine.execute("show databases")
        databases = ret.fetchall();
        if not self.__is_database_exist(databases, 'acfun_comments'):
            ret = self.__engine.execute("create database acfun_comments")
        login_cmd = self.__login_cmd.format(_username=self.__username, _password=self.__password, _database_name='acfun_comments')
        self.__engine = create_engine(login_cmd)

    def __is_database_exist(self, databases, database_name):
        for d in databases:
            if database_name == d._row[0]:
                return True
        return False