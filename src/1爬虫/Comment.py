import requests
import csv
from lxml import etree
from datetime import datetime, timedelta
from threading import Thread
from math import ceil
from time import sleep
from random import randint
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()

headers = {
    "User-Agent": UserAgent().chrome,
    'Cookie': 'your cookie'
}


class WeiboCommentScrapy(Thread):

    def __init__(self, wid):
        global headers
        Thread.__init__(self)
        self.headers = headers
        self.result_headers = ['主页', '昵称', '性别', '所在地', '微博数', '关注数', '粉丝数', '内容', '赞数', '发布时间', ]
        self.wid = wid
        self.start()

    def parse_time(self, publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = timedelta(minutes=int(minute))
            publish_time = (datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

    def getPublisherInfo(self, url):
        res = requests.get(url=url, headers=self.headers, verify=False)
        html = etree.HTML(res.text.encode('utf-8'))
        head = html.xpath("//div[@class='ut']/span[1]")[0]
        head = head.xpath('string(.)')[:-3].strip()
        keyIndex = head.index("/")
        nickName = head[0:keyIndex - 2]
        sex = head[keyIndex - 1:keyIndex]
        location = head[keyIndex + 1:]
        footer = html.xpath("//div[@class='tip2']")[0]
        weiboNum = footer.xpath("./span[1]/text()")[0]
        weiboNum = weiboNum[3:-1]
        followingNum = footer.xpath("./a[1]/text()")[0]
        followingNum = followingNum[3:-1]
        followsNum = footer.xpath("./a[2]/text()")[0]
        followsNum = followsNum[3:-1]
        return nickName, sex, location, weiboNum, followingNum, followsNum

    def get_one_comment_struct(self, comment):
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])
        content = comment.xpath(".//span[@class='ctt']/text()")
        if '回复' in content or len(content) == 0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()
            if len(content) == 0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':') + 1:]
        else:
            content = content[0]
        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]
        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]
        publish_time = self.parse_time(publish_time)
        nickName, sex, location, weiboNum, followingNum, followsNum = self.getPublisherInfo(url=userURL)
        return [userURL, nickName, sex, location, weiboNum, followingNum, followsNum, content, praisedNum, publish_time]

    def write_to_csv(self, result, isHeader=False):
        with open('comment/' + self.wid + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if isHeader == True:
                writer.writerows([self.result_headers])
            writer.writerows(result)

    def run(self):
        commentNum = 50
        pageNum = ceil(commentNum / 10)
        for page in range(pageNum):
            result = []
            res = requests.get('https://weibo.cn/comment/{}?page={}'.format(self.wid, page + 1), headers=self.headers,
                               verify=False)
            html = etree.HTML(res.text.encode('utf-8'))
            comments = html.xpath("/html/body/div[starts-with(@id,'C')]")
            for i in range(len(comments)):
                result.append(self.get_one_comment_struct(comments[i]))
            if page == 0:
                self.write_to_csv(result, isHeader=True)
            else:
                self.write_to_csv(result, isHeader=False)
            sleep(randint(1, 5))


if __name__ == "__main__":
    WeiboCommentScrapy(wid='IrMDgksAc')
