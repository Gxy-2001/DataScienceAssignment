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
    for x in df['评论内容']:
        data.append(x)
    for x in df['评论者粉丝数']:
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
    senList = readLines2('dict/BosonNLP_sentiment_score.txt')
    senDict = defaultdict()
    for s in senList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]

    exList = readLines2('dict/extra.txt')
    exDict = defaultdict()
    for x in exList:
        exDict[x.split(' ')[0]] = x.split(' ')[1]

    notList = readLines2('dict/notDict.txt')
    degreeList = readLines2('dict/degreeDict.txt')
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(' ')[0]] = d.split(' ')[1]

    return senDict, notList, degreeDict, exDict


def classifyWords(wordDict, senDict, notList, degreeDict, exDict):
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = float(str(senDict[word]))
        elif word in exDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = float(str(exDict[word]))
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = float(str(degreeDict[word]))
    return senWord, notWord, degreeWord


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
        SOPMI_data, fens = readLines(x)
        i = 0
        for d in SOPMI_data:
            if (str(fens[i]).isdigit() and int(fens[i]) < 10000) or (
                    str(fens[i]).count(".") == 1 and not str(fens[i]).startswith(".") and not str(fens[i]).endswith(
                    ".") and float(fens[i]) < 10000):
                datafen = sent2word(d)
                datafen_dist = listToDist(datafen)
                data_1 = classifyWords(datafen_dist, words_vaule[0], words_vaule[1], words_vaule[2], words_vaule[3])
                data_2 = scoreSent(data_1[0], data_1[1], data_1[2], returnsegResult(SOPMI_data[0]))
                if data_2 > 0.5 or data_2 < 0:
                    score_var.append(data_2)
            i = i + 1
        i = 0
        text_save(x.replace('data', 'result_comment'), score_var)
        score_var = []

    # files = eachFile('result_comment')
    # file = open('评论result.txt', 'a+', encoding='utf-8')
    # for x in files:
    #     fopen = open(x, 'r', encoding='utf-8')
    #     num = 0
    #     sum = 0
    #     for j in fopen.readlines():
    #         num = num + 1
    #         sum = sum + float(j)
    #     t = 0
    #     for j in range(len(x)):
    #         if x[j] == 'I':
    #             t = j
    #             break
    #     file.write(x[t:-4] + "   " + str(sum / num) + '\n')

    # file = open('评论result.txt', 'r', encoding='utf-8')
    # l = file.read().split('\n')
    # file2 = open('评论差值.txt', 'a+', encoding='utf-8')
    # for x in l:
    #     ls = x.split('  ')
    #     file2.write(str(4.8832 - float(ls[1]) )+ '\n')
