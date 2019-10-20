from urllib import request
import json
import gzip
import time
import math


class Comment:

    def __init__(self, cid, floor, user_name, content, aid, uid):
        # comment id
        self.cid = cid
        self.floor = floor
        # user id
        self.uid = uid
        self.content = content
        # article id
        self.aid = aid

    def __str__(self):
        return 'aid: ' + str(self.aid) + ' floor: ' + str(self.floor) + ' cid: ' + str(self.cid) + \
               ' uid: ' + str(self.uid) + '\n' + 'content: ' + self.content + '\n'
