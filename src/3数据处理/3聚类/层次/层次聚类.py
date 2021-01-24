import pandas as pd
import jieba
import matplotlib.pyplot as plt
from pylab import mpl
from collections import Counter
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import CountVectorizer
from tool.myTextRank import myTextRank


def func(num):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    datapd = pd.read_csv('sample_data.csv', encoding='utf-8')
    all_words = ""

    for line in datapd['content']:
        line = str(line)
        seg_list = myTextRank(line, False, 20)
        cut_words = (" ".join(seg_list))
        all_words += cut_words
    all_words = all_words.split()

    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    top_word = []
    for (k, v) in c.most_common(200):
        print("%s:%d" % (k, v))
        top_word.append(k)

    cut_words = ""
    f = open('key.txt', 'w', encoding='utf-8')
    datapd = pd.read_csv('sample_data.csv', encoding='utf-8')
    for line in datapd['content']:
        line = str(line)
        seg_list = jieba.cut(line, cut_all=False)
        final = ""
        for seg in seg_list:
            if seg in top_word:
                final += seg + " "
        cut_words += final
        f.write(final + "\n")
    print('cut_words', cut_words)
    f.close()
    text = open('key.txt', encoding='utf-8').read()
    list1 = text.split("\n")
    print(list1)

    count_vec = CountVectorizer(min_df=3)
    xx1 = count_vec.fit_transform(list1).toarray()
    word = count_vec.get_feature_names()
    print("word feature length: {}".format(len(word)))
    print(word)
    print(xx1.shape)
    print(xx1[0])

    df = pd.DataFrame(xx1)

    dist = df.corr()
    print(dist)
    print(dist.shape)

    plt.subplots(figsize=(15, 20))  # set size
    plt.tight_layout()
    plt.savefig('层次聚类.png', dpi=200)

    ac = AgglomerativeClustering(n_clusters=num, affinity='euclidean', linkage='ward')
    ac.fit(xx1)

    labels = ac.fit_predict(xx1)
    print(labels)

    plt.scatter(xx1[:, 0], xx1[:, 1], c=labels)
    plt.show()

    score0 = metrics.calinski_harabasz_score(xx1, labels)  # CH分数
    print(score0)
    score1 = metrics.silhouette_score(xx1, labels)  # 计算轮廓系数
    print()
    score2 = metrics.davies_bouldin_score(xx1, labels)  # 戴维森堡丁指数(DBI)
    print(metrics.davies_bouldin_score(xx1, labels))

    #plot_clustering(xx1, labels)
    return [score0, score1, score2]


def plot_clustering(X, labels, title=None):
    plt.figure(figsize=(10, 8))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='prism')
    if title is not None:
        plt.title(title, size=17)
    # plt.axis('off')
    # plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # data = []
    # file = open('类数.txt', 'a+', encoding='utf-8')
    # for i in range(2, 10):
    #     data = func(i)
    #     file.write(str(i) + " " + str(data[0]) + " " + str(data[1]) + " " + str(data[2]))
    func(3)
