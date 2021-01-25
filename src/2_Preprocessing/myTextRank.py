import networkx as nx
import jieba
import jieba.analyse
import pandas as pd
from pre import clean_text


def readLines(filename):
    fopen = open(filename, 'r', encoding='utf-8')
    data = []
    for x in fopen.readlines():
        if x.strip() != '':
            data.append(x.strip())
    fopen.close()
    return data


stopwords = readLines('stop_words.txt')


def myTextRank(text, boo, leng=5):
    text = clean_text(text)
    block_words = []
    if len(text) > 1:
        temp = list(jieba.cut(text))
        l = []
        for word in temp:
            if (word not in stopwords) and (len(word) > 1):
                l.append(word)
        block_words.append(l)
    kwds = textrank(block_words, leng, boo)
    return kwds


def textrank(block_words, topK, with_score=False):
    G = nx.Graph()
    for word_list in block_words:
        for u, v in combine(word_list, 2):
            G.add_edge(u, v)
    pr = nx.pagerank_scipy(G)
    pr_sorted = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    if with_score:
        return pr_sorted[:topK]
    else:
        return [w for (w, imp) in pr_sorted[:topK]]


def combine(word_list, window=2):
    for x in range(1, window):
        if x >= len(word_list):
            break
        word_list2 = word_list[x:]
        res = zip(word_list, word_list2)
        for r in res:
            yield r


def extract_keywords():
    df = pd.read_csv('simple.csv', index_col=0, )
    data = []
    d = []
    for x in df['微博正文']:
        l = myTextRank(str(x), True)
        for i in l:
            word = i[0]
            score = float(i[1])
            if word not in data:
                data.append(word)
                d.append(score)
            else:
                d[data.index(word)] = d[data.index(word)] + score
    return data, d


if __name__ == "__main__":
    data, d = extract_keywords()
    # print(data)
    # print(d)
    pairs = zip(d, data)
    pairs = sorted(pairs, reverse=True)
    print(pairs)

    result = [x[1] for x in pairs]
    print(result)

    file = open('示例关键词.txt', 'a+', encoding='utf-8')
    for i in range(100):
        file.write(str(result[i]) + '\n')
    file.close()
    print("保存文件成功")

    s = '2月9日凌晨1点40分，我县接到紧急通知，需要再增派5名相关医务人员，赴湖北支援新冠肺炎救治工作' \
        '。驰援号角再次吹响！8时便确定了上报名单。中午12时15分，安吉5' \
        '名医务人员仅在十小时内，安排好工作，安抚好家人，完成集结，整装出发！他们分别是县人民医院黄志辉、' \
        '县中医院邱蔚晨和周海月、安吉二院叶苑、安吉三院王志英，作为浙江省第三批抗击新冠肺炎紧急医疗队成员驰援湖北' \
        '。此前，我县已有县人民医院汪学丽、罗玉红2名医务人员驰援武汉 '

    print(myTextRank(s, False, 10))
    print(jieba.analyse.textrank(s))
