import re
from collections import defaultdict
import os
import jieba
import pandas as pd


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


def sent2word(sentence):
    clean = clean_text(sentence)
    segList = jieba.cut(clean)
    segResult = []
    for w in segList:
        segResult.append(w)
    stopwords = readStop('dict/stop_words.txt')
    newSent = []
    for word in segResult:
        if word + '\n' in stopwords:
            continue
        else:
            newSent.append(word)
    return newSent


def returnsegResult(sentence):
    segResult = []
    segList = jieba.cut(sentence)
    for w in segList:
        segResult.append(w)
    return segResult


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child


def readStop(filename):
    fopen = open(filename, 'r', encoding='utf-8')
    data = []
    for x in fopen.readlines():
        if x.strip() != '':
            data.append(x.strip())
    fopen.close()
    return data


def readLines(filename):
    df = pd.read_csv(filename, index_col=0, )
    data = []
    fens = []
    for x in df['微博正文']:
        data.append(x)
    for x in df['发布者粉丝数']:
        fens.append(x)
    return data, fens


def readLines2(filename):
    fopen = open(filename, 'r', encoding='utf-8')
    data = []
    for x in fopen.readlines():
        if x.strip() != '':
            data.append(x.strip())

    fopen.close()
    return data


def words():
    le = readLines2('dict/乐.txt')
    hao = readLines2('dict/好.txt')
    ai = readLines2('dict/哀.txt')
    wu = readLines2('dict/恶.txt')
    ju = readLines2('dict/惧.txt')
    return [le, hao, ai, wu, ju]


def classifyWords(wordDict, le, hao, ai, wu, ju):
    # le = defaultdict()
    # hao = defaultdict()
    # ai = defaultdict()
    # wu = defaultdict()
    # ju = defaultdict()
    res = [0, 0, 0, 0, 0]
    for word in wordDict.keys():
        if word in le:
            res[0] = res[0] + 1
        elif word in hao:
            res[1] = res[1] + 1
        elif word in ai:
            res[2] = res[2] + 1
        elif word in wu:
            res[3] = res[3] + 1
        elif word in ju:
            res[4] = res[4] + 1
    max = res[0]
    t = 0
    for i in range(5):
        if res[i] > max:
            t = i
    return t


def scoreSent(senWord, notWord, degreeWord, segResult):
    score = 0
    senLoc = list(senWord.keys())
    notLoc = list(notWord.keys())
    degreeLoc = list(degreeWord.keys())
    senloc = -1
    for i in range(0, len(segResult)):
        W = 1
        if i in senLoc:
            senloc += 1
            score += W * float(senWord.get(i))
            if senloc < len(senLoc) - 1:
                j = senLoc[senloc]
                while j < senLoc[senloc + 1]:
                    if j in notLoc:
                        W *= -1
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
                    j += 1
    return score


def listToDist(wordlist):
    data = {}
    for x in range(0, len(wordlist)):
        data[wordlist[x]] = x
    return data


def text_save(filename, data):
    file = open(filename.replace('csv', 'txt'), 'a+')
    for i in range(len(data)):
        file.write(str(data[i]) + '\n')
    file.close()
    print("保存文件成功")


if __name__ == "__main__":
    filepwd = eachFile("data")
    score_var = []
    words_vaule = words()
    for x in filepwd:
        data, fens = readLines(x)
        i = 0
        for d in data:
            if str(fens[i]).isdigit() and int(fens[i]) < 10000:
                datafen = sent2word(d)
                datafen_dist = listToDist(datafen)
                data_1 = classifyWords(datafen_dist, words_vaule[0], words_vaule[1], words_vaule[2], words_vaule[3],
                                       words_vaule[4])
                score_var.append(data_1)
            i = i + 1
        i = 0
        text_save(x.replace('data', 'result'), score_var)
        score_var = []
