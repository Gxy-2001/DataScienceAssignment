import os

import pandas as pd
import jieba
from pylab import mpl
from collections import Counter

from scipy.cluster.hierarchy import ward, dendrogram
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import CountVectorizer
from myTextRank import myTextRank
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child

def label2rank(labels_list):
    series = pd.Series(labels_list)
    list1 = series[series != -1].tolist()
    n = len(set(list1))
    cnt = Counter(list1)
    key = [cnt.most_common()[i][0] for i in range(n)]
    value = [i for i in range(1, n + 1)]
    my_dict = dict(zip(key, value))
    my_dict[-1] = -1
    rank_list = [my_dict[i] for i in labels_list]
    return rank_list


def feature_reduction(matrix, pca_n_components=50, tsne_n_components=2):
    data_pca = PCA(n_components=pca_n_components).fit_transform(matrix) if pca_n_components is not None else matrix
    data_pca_tsne = TSNE(n_components=tsne_n_components).fit_transform(
        data_pca) if tsne_n_components is not None else data_pca
    print('data_pca_tsne.shape=', data_pca_tsne.shape)
    return data_pca_tsne


def func(file):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    datapd = pd.read_csv(file, encoding='utf-8')
    all_words = ""

    for line in datapd['微博正文']:
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
    datapd = pd.read_csv(file, encoding='utf-8')
    for line in datapd['微博正文']:
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
    count_vec = CountVectorizer(min_df=3)
    xx1 = count_vec.fit_transform(list1).toarray()
    df = pd.DataFrame(xx1)

    dist = df.corr()
    linkage_matrix = ward(dist)
    fig, ax = plt.subplots(figsize=(15, 20))  # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=count_vec.get_feature_names() );
    plt.tight_layout()
    plt.savefig('层次聚类树图.png', dpi=200)

    ac = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    ac.fit(xx1)

    labels = ac.fit_predict(xx1)


    plt.scatter(xx1[:, 0], xx1[:, 1], c=labels)
    plt.show()

    score0 = metrics.calinski_harabasz_score(xx1, labels)  # CH分数
    print(score0)
    score1 = metrics.silhouette_score(xx1, labels)  # 计算轮廓系数
    print()
    score2 = metrics.davies_bouldin_score(xx1, labels)  # 戴维森堡丁指数(DBI)
    print(metrics.davies_bouldin_score(xx1, labels))

    labels = ac.labels_
    df['label'] = labels
    ranks = label2rank(labels)
    df['rank'] = ranks
    print(df.head())

    df['matrix'] = xx1.tolist()

    df_non_outliers = df[df['label'] != -1].copy()

    data_pca_tsne = feature_reduction(df_non_outliers['matrix'].tolist(), pca_n_components=3, tsne_n_components=2)

    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    data_pca_tsne = data_pca_tsne.tolist()
    label = df_non_outliers['label']

    plt.figure()
    x = [i[0] for i in data_pca_tsne]
    y = [i[1] for i in data_pca_tsne]
    plt.scatter(x, y, c=label)
    plt.savefig('层次PCA.jpg')
    plt.show()

    return [score0, score1, score2]


if __name__ == "__main__":
    file = eachFile('data')
    func(file[0])
