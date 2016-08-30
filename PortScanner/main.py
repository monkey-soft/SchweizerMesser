#-*-  coding:utf-8 -*-
__author__ = 'monkey'

import argparse
import socket
import textwrap


# use socket to redge port is open
def connectScan(targetHost, targetPort):
    try:
        connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectSocket.connect((targetHost, targetPort))
        # print('[+]%d/tcp open' %tatgetPort)
        results.append('[+]%d/tcp open' %targetPort)
        connectSocket.close()
    except:
        # print('[-]%d tcp closed' %tatgetPort)
        results.append('[-]%d tcp closed' %targetPort)

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
        prog='PortScanner 1.0.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
            usage %(prog)s
                -h help
                -H <target host>
                -p <target port>
            文中说明 ：
                -h 帮助
                -H 目标主机
                -p 目标端口'''),
        epilog=textwrap.dedent('''
            made by monkey！
            本工具由猴子制作！
            '''))
    parser.add_argument('-H', dest='targetHost', type=str,    # 字符串类型要写str, 不能写String
                        help='specify target host 指定目标主机')
    parser.add_argument('-p', dest='targetPort', type=int,  nargs='*',  #　多个参数会填充到list中
                        help='specify target port 指定目标端口')
    # 获取参数
    args = parser.parse_args()
    print(args)
    targetHost = args.targetHost
    targetPorts = args.targetPort


    if (targetHost == None) | (targetPorts == None):
        print('[-] You must specify a target host and ports[s]!')
        exit(0)
    portScan(targetHost, targetPorts)


if __name__ == '__main__':
    results = []
    main()
    printResults(results)



