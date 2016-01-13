__author__ = 'monkey'


# 去掉重复的字符串
def Cutdown(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    list = []
    for each in lines:
        if each in list:
            pass
        else:
            list.append(each)
    return list

# 保存过滤掉重复的列表
def writeToFile(list):
    f = open('new.txt', 'a')
    for each in list:
        f.writelines(each)
    f.close()

if __name__ == '__main__':
    filename = input('please input filename:\n')
    list = Cutdown(filename);
    writeToFile(list)