from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
# 支持 MySQL的UNSIGNED INTEGER
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BIGINT
from sqlalchemy.orm import sessionmaker
import re


# SQLHelper整体应考虑防注入，封装好增查的功能
class SQLHelper:
    __Base_Comments = declarative_base()
    __Base_Articles = declarative_base()

    # Comments表
    class SQLComments(__Base_Comments):
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
    class SQLArticles(__Base_Articles):
        __tablename__ = "articles"
        aid = Column(BIGINT(unsigned=True), autoincrement=False, primary_key=True)
        comment_count = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
        latest_floor = Column(INTEGER(unsigned=True), nullable=False, server_default='0')
        latest_comment_time = Column(BIGINT(unsigned=True), nullable=False, server_default='0')

        def __repr__(self):
            tpl = "articles(aid = {}, comment_count = {}, latest_floor = {}"
            return tpl.format(self.aid, self.comment_count, self.latest_floor, self.latest_comment_time)

    __engine = None
    __login_cmd = 'mysql+pymysql://{_username}:{_password}@localhost:3306/{_database_name}'
    __session = None
    __username = str()
    __password = str()
    __database_name = str()

    def __init__(self, username, password, database_name):
        self.__username = username
        self.__password = password
        self.__database_name = database_name
        self.__engine = create_engine(
            self.__login_cmd.format(_username=username, _password=password, _database_name=''))
        self.__check_database(database_name)
        self.__create_session()
        return

    def __check_database(self, database_name):
        # 检查数据库是否存在
        ret = self.__engine.execute("show databases")
        databases = ret.fetchall();
        if not self.__is_object_exist(databases, database_name):
            ret = self.__engine.execute("create database " + database_name)
        # if not ret:
        #     raise RuntimeError("Create database acfun_comments failed.")
        login_cmd = self.__login_cmd.format(_username=self.__username, _password=self.__password,
                                            _database_name=database_name)
        self.__engine = create_engine(login_cmd)
        # 检查表是否存在
        ret = self.__engine.execute("show tables")
        tables = ret.fetchall()
        if not self.__is_object_exist(tables, 'comments'):
            self.__Base_Comments.metadata.create_all(self.__engine)
        if not self.__is_object_exist(tables, 'articles'):
            self.__Base_Articles.metadata.create_all(self.__engine)

    def __is_object_exist(self, object, object_name):
        for o in object:
            if object_name == o._row[0]:
                return True
        return False

    def __create_session(self):
        self.__session = sessionmaker(bind=self.__engine)

    def save_article_list(self, article_list):

        return

    def save_comment_list(self, comment_list):

        return
