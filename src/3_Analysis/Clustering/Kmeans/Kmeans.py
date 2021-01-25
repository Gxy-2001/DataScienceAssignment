import pandas as pd
import re
import jieba.posseg as pseg
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn import metrics


def clean_text(text, name=True, ):
    if name:
        for i in range(len(text)):
            if text[i] == ':' or text[i] == '：':
                text = text[i + 1:-1]
                break

    zh_puncts1 = "，；、。！？（）《》【】"
    URL_REGEX = re.compile(
        r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)

    EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
    text = re.sub(EMAIL_REGEX, "", text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    lb, rb = 1, 6
    text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0" "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r"#\S+#", "", text)
    text = text.replace("\n", " ")

    text = re.sub(r"(\s)+", r"\1", text)
    stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直', 'u3000', '24', '12',
                  '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
    for x in stop_terms:
        text = text.replace(x, "")
    allpuncs = re.compile(
        r"[，\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
    text = re.sub(allpuncs, "", text)

    return text.strip()


def get_words_by_flags(words, flags=None):
    flags = ['n.*', 'v.*'] if flags is None else flags
    words = [w for w, f in words if w != ' ' and re.match('|'.join(['(%s$)' % flag for flag in flags]), f)]
    return words


def stop_words_cut(words, stop_words_path):
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
        stopwords.append(' ')
        words = [word for word in words if word not in stopwords]
    return words


def pseg_cut(x):
    return pseg.lcut(x, HMM=True)


def preProcess(df):
    df['content'] = df['content'].map(lambda x: clean_text(x))
    df['content_cut'] = df['content'].map(lambda x: pseg_cut(x))
    df['content_cut'] = df['content_cut'].map(lambda x: get_words_by_flags(
        x, flags=['n.*', 'v.*', 'eng', 't', 's', 'j', 'l', 'i']))
    df['content_cut'] = df['content_cut'].map(lambda x: stop_words_cut(
        x, 'stop_words.txt'))
    df['content_'] = df['content_cut'].map(lambda x: ' '.join(x))


def flat(l):
    for k in l:
        if not isinstance(k, (list, tuple)):
            yield k
        else:
            yield from flat(k)


def get_single_frequency_words(list1):
    list2 = flat(list1)
    cnt = Counter(list2)
    list3 = [i for i in cnt if cnt[i] == 1]
    return list3


def feature_extraction(series, vec_args):
    vec_args_list = ['%s=%s' % (i[0],
                                "'%s'" % i[1] if isinstance(i[1], str) else i[1]
                                ) for i in vec_args.items()]
    vec_args_str = ','.join(vec_args_list)
    vectorizer1 = TfidfVectorizer(vec_args_str)
    matrix = vectorizer1.fit_transform(series)
    return matrix


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


if __name__ == '__main__':
    filepath = 'example_data.csv'
    df = pd.read_csv(filepath, index_col=0, )
    preProcess(df)
    word_library_list = list(set(flat((df['content_cut']))))
    single_frequency_words_list = get_single_frequency_words(df['content_cut'])
    max_features = (len(word_library_list) - len(single_frequency_words_list))
    matrix = feature_extraction(df['content_'],
                                vec_args={'max_df': 0.95, 'min_df': 1, 'max_features': max_features})
    kmeans = KMeans(n_clusters=2, random_state=9).fit(matrix)

    score = metrics.calinski_harabasz_score(matrix.toarray(), kmeans.labels_)
    print(score)
    print(metrics.silhouette_score(matrix.toarray(), kmeans.labels_))  # 计算轮廓系数)
    print(metrics.davies_bouldin_score(matrix.toarray(), kmeans.labels_))

    labels = kmeans.labels_
    df['label'] = labels
    ranks = label2rank(labels)
    df['rank'] = ranks
    print(df.head())

    df['matrix'] = matrix.toarray().tolist()

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
    plt.savefig('kmeans示例.jpg')
    plt.show()
