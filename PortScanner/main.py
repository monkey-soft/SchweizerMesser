#-*-  coding:utf-8 -*-
__author__ = 'monkey'

import argparse
import socket
import textwrap      # 文字格式化类
import threading


# 使用信号量提供一个锁，使得当前只有一个线程能打印消息
screenLock = threading.Semaphore(value=1)

# use socket to redge port is open
def connectScan(targetHost, targetPort):
    try:
        connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectSocket.connect((targetHost, targetPort))
        # print('[+]%d/tcp open' %tatgetPort)
        results.append('[+]%d/tcp open' %targetPort)
        # 加锁
        screenLock.acquire()
    except:
        # 加锁
        screenLock.acquire()
        # print('[-]%d tcp closed' %tatgetPort)
        results.append('[-]%d tcp closed' %targetPort)
    finally:
        screenLock.release()
        connectSocket.close()

# scan the targethost having all opened ports
def portScan(targetHost, targetPorts):
    try:
        targetIP = socket.gethostbyname(targetHost)
    except:
        print("[-] Cannot resolve '%s':UnKnown host" %targetHost)
        return

    try:
        targetName = socket.gethostbyaddr(targetIP)
        print('\n[+] Scan Results for:' + targetName[0])
    except:
        print('\n[+] Scan Results for:' + targetIP)

    socket.setdefaulttimeout(1)
    for port in targetPorts:
        print('Scanning port ' + str(port))
        connectScan(targetHost, int(port))

# print all results
def printResults(resultlist):
    for r in resultlist:
        print(r)

def main():
    parser = argparse.ArgumentParser(
        prog='PortScanner 1.1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
            usage %(prog)s
                -h help
                -H <target host>
                -p <target port>
                -a <all port>
            文中说明 ：
                -h 帮助
                -H 目标主机
                -p 目标端口, 不指定就默认扫描常见端口; all 参数为扫描全部端口
                -a 全部端口'''),
        epilog=textwrap.dedent('''
            made by monkey！
            本工具由猴子制作！
            '''))
    parser.add_argument('-H', dest='targetHost', type=str,              # 字符串类型要写str, 不能写String
                        help='specify target host(required) 指定目标主机(必须)', required=True)
    parser.add_argument('-p', dest='targetPort', type=int,  nargs='*',  #　多个参数会填充到list中
                        help='specify target port 指定目标端口')
    parser.add_argument('-a', dest='isAll',  type=str,
                        help='specify all posts (1-65535)')
    # 获取参数
    args = parser.parse_args()
    print(args)
    targetHost = args.targetHost
    targetPorts = args.targetPort
    isAll = argparse.isAll

    if (targetHost == None | targetPorts == None):
        print('[-] You must specify a target host and ports[s]!')
        exit(0)

    # # 当用户不指定端口, 即扫描常见的端口
    if (len(targetPorts) == 0):
        targetPorts = [21,22,23,25,53,80,81,109,110,111,123,135,137,139,161,162,389,443,512,513,873,
                       1080,1158,1433,1521,1900,2049,2100,2222,2601,2604,2082,2083,3128,3312,3306,
                       3311,3312,3389,4440,5050,5672,5900,6082,6379,6788,6789,7001,7777,8000,8080,8081,
                       8088,8089,8090,8099,8161,8649,8888,9000,9080,9090,9200,9300,9999,10050,11211,
                       27017,28017,37777,50000,50060,50070]


    portScan(targetHost, targetPorts)

if __name__ == '__main__':
    results = []
    main()
    printResults(results)



