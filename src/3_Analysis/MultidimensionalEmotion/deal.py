import os


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child


if __name__ == '__main__':
    files = eachFile('result')
    file = open('../../4_Visualization/多维/SOPMI_data/result.txt', 'a+', encoding='utf-8')
    for x in files:
        fopen = open(x, 'r', encoding='utf-8')
        data = [0, 0, 0, 0, 0]
        num = 0
        for j in fopen.readlines():
            num = num + 1
            j = j.strip()
            if j == '0':
                data[0] = data[0] + 1
            elif j == '1':
                data[1] = data[1] + 1
            elif j == '2':
                data[2] = data[2] + 1
            elif j == '3':
                data[3] = data[3] + 1
            elif j == '4':
                data[4] = data[4] + 1
        t = 0
        for j in range(len(x)):
            if x[j].isdigit():
                t = j
                break
        file.write(
            x[t:-4] + "  " + str(data[0] / num)[0:6] + '  ' + str(data[1] / num)[0:6] + '  ' + str(data[2] / num)[0:6]
            + '  ' + str(data[3] / num)[0:6] + '  ' + str(data[4] / num)[0:6] + '\n')
