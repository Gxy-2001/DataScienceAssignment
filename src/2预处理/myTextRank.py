import networkx as nx
import jieba
import jieba.analyse
import pandas as pd
import re
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


def myTextRank(text, boo):
    block_pos = text.split('\n')
    block_words = []
    for i in range(len(block_pos)):
        if len(block_pos[i]) > 1:
            temp = list(jieba.cut(block_pos[i]))
            l = []
            for word in temp:
                if (word not in stopwords) and (len(word) > 1):
                    l.append(word)
            block_words.append(l)
    kwds = textrank(block_words, 5, boo)
    return kwds


def textrank(block_words, topK, with_score=False, window=2, weighted=False):
    G = nx.Graph()
    for word_list in block_words:
        for u, v in combine(word_list, window):
            if not weighted:
                G.add_edge(u, v)
            else:
                if G.has_edge(u, v):
                    G[u][v]['weight'] += 1
                else:
                    G.add_edge(u, v, weight=1)

    pr = nx.pagerank_scipy(G)
    pr_sorted = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    if with_score:
        return pr_sorted[:topK]
    else:
        return [w for (w, imp) in pr_sorted[:topK]]


def combine(word_list, window=2):
    if window < 2: window = 2
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
    for i in range(len(result)):
        file.write(str(result[i]) + '\n')
    file.close()
    print("保存文件成功")
