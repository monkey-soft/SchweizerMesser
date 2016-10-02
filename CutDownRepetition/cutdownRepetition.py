#-*-  coding:utf-8 -*-
__author__ = 'monkey'


# 去掉重复的字符串
def Cutdown(filename):
    with open(filename, 'r') as f:
        for each in f:
            if each in simplelist:
                pass
            else:
                simplelist.append(each)

# 保存过滤掉重复的列表
def writeToFile():
    with open('new.txt', 'a') as wirtedFile:
        for each in simplelist:
            wirtedFile.writelines(each)
        wirtedFile.close()

if __name__ == '__main__':
    filename = input('please input filename:\n')
    simplelist = []
    Cutdown(filename);
    writeToFile()