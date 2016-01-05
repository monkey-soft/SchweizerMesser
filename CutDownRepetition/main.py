__author__ = 'monkey'


# 去掉重复的字符串
def Cutdown():
    with open('test.txt', 'r') as file:
        data = file.read()
        # 将文件中的字符串装化为列表
        oldlist = list(data)
        print("the length of oldlist :" + len(oldlist))

    newlist = []
    for i in data:
        if (i in newlist):
            pass
        else:
            if i != '\n':
                newlist.append(i)

    print("the length of newlist :" + len(newlist))
    return newlist

# 保存过滤掉重复的列表
def writeToFile(newlist):
    f = open('new.txt', 'a')
    for each in newlist:
        f.writelines(each + '\n')
    f.close()

if __name__ == '__main__':
    list = Cutdown();
    writeToFile(list)