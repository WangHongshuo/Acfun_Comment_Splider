import time
from comment_helper import CommentHelper


def main():
    start_time = time.time()

    comment_helper = CommentHelper()
    comment_helper.get_all_comments_by_aid(11735561)

    print('采集时间: ' + str(time.time() - start_time) + 's')

    # 存入comments sql的数据：cid（唯一）, aid, floor, uid, content
    for c in comment_helper.comments_list:
        print(c)

    b = 2
    a = 1


if __name__ == '__main__':
    main()
