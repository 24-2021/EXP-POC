# CNVD-2021-30167-NC-BeanShell-RCE
用于CNVD-2021-30167：用友NC BeanShell RCE，检测+验证+批量

用法示例：

python 用友beanshell-rce.py -h ##查看帮助

![clipboard](https://user-images.githubusercontent.com/75511051/142760849-b7291753-d89e-46bc-a9f3-17458762be5a.png)

python用友beanshell-rce.py --check http://exp.com/ ##检测网站是否存在该漏洞

![clipboard2](https://user-images.githubusercontent.com/75511051/142760872-8ab50f65-da1f-41f7-8a1d-f2603bec62a2.png)

python用友beanshell-rce.py -u http://exp.com command ##示例检测网站是否存在该漏洞

![clipboard3](https://user-images.githubusercontent.com/75511051/142760875-5d142ad5-d248-4c36-bf04-4d4c0d1c0c36.png)


python 用友beanshell-rce.py --file url.txt  ##批量检测网站是否存在该漏洞

![clipboard4](https://user-images.githubusercontent.com/75511051/142760879-66685509-f069-477b-b130-eecc4daec1aa.png)


