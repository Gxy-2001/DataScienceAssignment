file = open('result.txt', 'r', encoding='utf-8')
lines = file.read().split('\n')
date = []
score = []
for i in lines:
    l = i.split('  ')
    date.append(l[0])
    score.append(l[1][1:7])
print(date)
