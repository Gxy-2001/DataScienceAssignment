import requests
import random
import re
import sys
import csv
from lxml import etree
from collections import OrderedDict
from urllib.parse import quote
from time import sleep
from datetime import datetime, timedelta
from fake_useragent import UserAgent

Cookie = 'your Cookie'

User_Agent = UserAgent().random
mystart_day = 10
mystart_time = 10
boo = True


class WeiboTopicScrapy:

    def __init__(self, keyword, start_time, end_time):
        self.headers = {
            'Cookie': Cookie,
            'User_Agent': User_Agent
        }
        self.keyword = keyword
        self.start_time = time_params_formatter(start_time, offset_hour=-8)
        self.end_time = time_params_formatter(end_time, offset_day=-1, offset_hour=-7)
        self.got_num = 0
        self.weibo = []
        self.run()

    def garbled(self, info):
        info = (info.xpath('string(.)').replace(u'\u200b', '').encode(
            sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        return info

    def get_long_weibo(self, weibo_link):
        html = requests.get(weibo_link, headers=self.headers).content
        selector = etree.HTML(html)
        info = selector.xpath("//div[@class='c']")[1]
        wb_content = self.garbled(info)
        wb_time = info.xpath("//span[@class='ct']/text()")[0]
        weibo_content = wb_content[wb_content.find(':') +
                                   1:wb_content.rfind(wb_time)]
        return weibo_content

    def get_weibo_content(self, info):
        weibo_id = info.xpath('@id')[0][2:]
        weibo_content = self.garbled(info)
        weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
        a_text = info.xpath('div//a/text()')
        if u'全文' in a_text:
            weibo_link = 'https://weibo.cn/comment/' + weibo_id
            wb_content = self.get_long_weibo(weibo_link)
            if wb_content:
                weibo_content = wb_content
        return weibo_content

    def get_publisher_info(self, link):
        html = requests.get(link, headers=self.headers).content
        selector = etree.HTML(html)
        html = selector
        user_info = html.xpath('//div[@class="ut"]/span[@class="ctt"]')[0]
        user_info = user_info.xpath('string(.)').strip()
        user_info = ' '.join(user_info.split())
        kindex = user_info.index(' ')
        username = user_info[:kindex]
        sex = user_info[kindex + 1:user_info.index('/')]
        province = user_info[user_info.index('/') + 1:user_info.rindex(' ')]

        following = html.xpath('//div[@class="tip2"]/a[1]/text()')[0]
        following = following[3:-1]
        followd = html.xpath('//div[@class="tip2"]/a[2]/text()')[0]
        followd = followd[3:-1]
        return username, sex, province, following, followd

    def getweibo(self, info):
        weibo = OrderedDict()
        is_original = False if len(info.xpath("div/span[@class='cmt']")) > 3 else True
        if is_original:
            weibo['id'] = info.xpath('@id')[0]
            weibo['id'] = weibo['id'][2:]
            publisher_link = info.xpath('div/a/@href')[0]

            weibo['publisher_name'], weibo['publisher_sex'], weibo['publisher_province'], \
            weibo['publisher_following'], weibo['publisher_followed'] = self.get_publisher_info(publisher_link)

            weibo['content'] = self.get_weibo_content(info)

            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.garbled(str_time[0])
            publish_time = str_time.split('来自')[0]
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

            weibo['publish_time'] = publish_time

            footer = {}
            pattern = r'\d+'
            str_footer = info.xpath('div')[-1]
            str_footer = self.garbled(str_footer)
            str_footer = str_footer[str_footer.rfind('赞'):]
            weibo_footer = re.findall(pattern, str_footer, re.M)

            up_num = int(weibo_footer[0])
            # print('点赞数: ' + str(up_num))
            footer['up_num'] = up_num

            retweet_num = int(weibo_footer[1])
            # print('转发数: ' + str(retweet_num))
            footer['retweet_num'] = retweet_num

            comment_num = int(weibo_footer[2])
            # print('评论数: ' + str(comment_num))
            footer['comment_num'] = comment_num
            weibo['up_num'] = footer['up_num']
            weibo['retweet_num'] = footer['retweet_num']
            weibo['comment_num'] = footer['comment_num']
        else:
            weibo = None
        return weibo

    def run(self):
        global mystart_day, mystart_time
        wrote_num = 0
        page1 = 0
        random_pages = random.randint(1, 5)
        pageNum = 50000
        for page in range(1, pageNum):
            Referer = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&page={}'.format(quote(self.keyword),
                                                                                                 page - 1)
            headers = {
                'Cookie': Cookie,
                'User-Agent': User_Agent,
                'Referer': Referer
            }
            params = {
                'hideSearchFrame': '',
                'keyword': self.keyword,
                'advancedfilter': '1',
                'starttime': self.start_time,
                'endtime': self.end_time,
                'sort': 'time',
                'page': page
            }
            res = requests.get(url='https://weibo.cn/search/mblog', params=params, headers=headers)
            html = etree.HTML(res.text.encode('utf-8'))
            weibos = html.xpath("//div[@class='c' and @id]")
            if len(weibos) == 0 or page > 10:
                mystart_time = mystart_time + 1
                if mystart_time == 23:
                    mystart_day = (mystart_day + 1) % 30
                    mystart_time = 1
                start()

            for i in range(0, len(weibos)):
                aweibo = self.getweibo(info=weibos[i])
                if aweibo:
                    self.weibo.append(aweibo)
                    self.got_num += 1

            if page % 4 == 0:
                result_headers = ['微博id', '发布者昵称', '发布者性别', '发布者地区', '发布者关注数', '发布者粉丝数', '微博正文', '发布时间', '点赞数', '转发数',
                                  '评论数', ]
                result_data = [w.values() for w in self.weibo][wrote_num:]
                with open('topic/' + 'some keyWords' + "5." + str(mystart_day) + '.csv', 'a', encoding='utf-8-sig',
                          newline='') as f:
                    writer = csv.writer(f)
                    global boo
                    if boo:
                        boo = False
                        writer.writerows([result_headers])
                    writer.writerows(result_data)
                wrote_num = self.got_num

            if page - page1 == random_pages and page < pageNum:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 3)



def time_params_formatter(params_time, offset_day=0, offset_hour=-8):
    [temp_year, temp_month, temp_day, temp_hour] = [int(e) for e in params_time.split('-')]
    temp_date = datetime(year=temp_year, month=temp_month, day=temp_day, hour=temp_hour)
    temp_offset = timedelta(days=offset_day, hours=offset_hour)
    res_time = (temp_date + temp_offset).strftime('%Y-%m-%d-%H')
    return res_time


def start():
    keyword = ['疫情', '武汉', '肺炎', '新型', '冠状病毒', '感染', '口罩', '医院', '病毒', '确诊', '患者', '加油', "病例", '防控', '隔离', '新冠', '一线',
               '湖北', '传播', '治疗', '医护人员', '出院', '健康', '发热', '消毒', '症状', '治愈', '新增', '致敬', '社区', '物资', '防护', '酒精',
               ]
    start_time = '2020-01-01-00'
    global mystart_time
    global mystart_day
    global boo
    if mystart_time > 23:
        mystart_time = 0
        boo = True
    temp_day = str(mystart_day)
    temp_time = str(mystart_time)
    if len(temp_day) == 1:
        temp_day = "0" + temp_day
    if len(temp_time) == 1:
        temp_time = "0" + temp_time
    end_time = '2020-02-{}-{}'.format(temp_day, temp_time)
    WeiboTopicScrapy(keyword=keyword[random.randint(0, len(keyword))], start_time=start_time, end_time=end_time)


if __name__ == '__main__':
    start()
