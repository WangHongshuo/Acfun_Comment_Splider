from selenium import webdriver
import time
import copy


class Comment:
    floor = ""
    user_name = ""
    text = ""

    def Comment(self):
        self.text
        self.floor
        self.name


def main():
    url = 'https://www.acfun.cn/a/ac11294787'
    driver = webdriver.Firefox()
    driver.get(url)
    # 加入延时防止获取数据不全
    time.sleep(5)
    # 获取盖楼模式的楼顶评论
    fc_comment_list = driver.find_elements_by_xpath(
        "//div[@class='fc-comment-list']/div[@class='main-comment-item']/div[@class='content']/div["
        "@class='fc-comment-item']")
    comments = list()
    comment = Comment()
    for i in fc_comment_list:
        # 分割出评论floor，user_name，text
        str = i.text.split("\n")
        floor_user_name = str[0].split(" ")
        comment.floor = floor_user_name[0][1:]
        comment.user_name = floor_user_name[1]
        str = str[1:-2]
        comment.text = ""
        for j in str:
            comment.text = comment.text + j + "\n"
        comment.text = comment.text[:-1]
        comments.append(copy.deepcopy(comment))

    a = 1


if __name__ == '__main__':
    main()
