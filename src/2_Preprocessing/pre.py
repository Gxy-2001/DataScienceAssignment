import re


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


if __name__ == '__main__':
    print(clean_text(
        '回复@让我再看你一眼 //让我再看你一眼·:#高以翔[超话]# 以翔 这个点了睡意全无  节日现在对于我们就是一种悲伤  '
        '没有了你世界都乱了 新冠肺炎疫情爆发让多少家庭除夕夜不能团聚  如果你在肯定会教我们正确的心态对待 会为逆行英雄'
        '打call 会做慈善捐助  因为你是Godfrey@高以翔Godfrey @全世界最好的高以翔Godfrey 仙桃  显示地图 原图http://t.cn/Ir1YpaAb0'))
