file = open('result.txt', 'r', encoding='utf-8')
lines = file.read().split('\n')
l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
for line in lines:
    l = line.split()
    l1.append(float(l[1]))
    l2.append(float(l[2]))
    l3.append(float(l[3]))
    l4.append(float(l[4]))
    l5.append(float(l[5]))

data1 = [0, 0, 0, 0, 0]
for i in range(40, 60):
    data1[0] = data1[0] + l1[i] / 20
    data1[1] = data1[1] + l2[i] / 20
    data1[2] = data1[2] + l3[i] / 20
    data1[3] = data1[3] + l4[i] / 20
    data1[4] = data1[4] + l5[i] / 20
print(data1)
