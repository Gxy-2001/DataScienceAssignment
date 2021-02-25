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


def extract_keywords(i):
    df = pd.read_csv('热门微博.csv', index_col=0, )
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
    dit = {}
    for i in range(1):
        print(i)
        data, d = extract_keywords(i)
        pairs = zip(d, data)
        pairs = sorted(pairs, reverse=True)
        cnt = 0
        for j in pairs:
            if j[1] in dit:
                dit[j[1]] = dit[j[1]] + j[0]
            else:
                dit[j[1]] = j[0]
            cnt = cnt + 1
    d = dit.keys()
    data = dit.values()
    pairs = zip(list(data), list(d))
    pairs = sorted(pairs, reverse=True)
    print(pairs)

    result = [x[1] for x in pairs]
    print(result)

    file = open('data/热门带权值.txt', 'a+', encoding='utf-8')
    for i in range(200):
        file.write(str(pairs[i]) + '\n')
    file.close()
    file = open('data/热门.txt', 'a+', encoding='utf-8')
    for i in range(200):
        file.write(str(pairs[i][1]) + '\n')
    file.close()
    print("保存文件成功")

    # s = '蒙哥奶奶:武汉冠状肺炎病毒这个周末有了出人意料的变化。先是泰国确诊了2例，接着是日本确诊了1例，另外还有新加坡疑似有2例，这5' \
    #     '位当事人的共同点就是近期去过武汉。然后就有人调侃，这次的肺炎病毒比较有觉悟，只出国，不出武汉市。把话说白了就是根据武汉对外的人' \
    #     '流量，按概率算，网友们担心有可能已经向省外扩散，只是还没被发现？今天微博上有几个相关话题，但这种重大社会新闻不能信路边社，还' \
    #     '是以官方公告为准，武汉又新增了17例确诊病例，一共确诊62例，目前死亡人数2人。到19日晚为止，内地其余城市还未官宣有确诊病例，目前' \
    #     '官方的说法是疫情整体可控，不能排除人传人的可能性，但持续人传人的风险较低。我担心的是马上就到春运了，网友们最好在人流大的公共场' \
    #     '所戴口罩，未雨绸缪总是没错的。鉴于疫情有了诸多发展，周一生物疫苗板块的股票大概率会受到刺激，根据我的主观感觉，这次的刺激会比第' \
    #     '一波要强烈.'
    #
    # print(myTextRank(s, True, 10))
    # print(jieba.analyse.textrank(s))
