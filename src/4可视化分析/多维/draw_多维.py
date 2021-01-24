import os


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child


if __name__ == "__main__":
    filepwd = eachFile("data")
    