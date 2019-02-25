import re

import requests


"""
教务系统爬虫
主要核心思路：
1.通过访问学校VPN网站并且模仿登陆进入内网
2.跳转教务系统页面抓取cookie和验证码后模拟登陆
3.携带cookie访问需要的网页解析后得到爬取数据
"""


# 登陆VPN网站
def link_VPN(session, headers):
    url = session.get('http://jwxt.tcu.edu.cn/loginAction.do')
    username = input('校园网账号：')
    password = input('校园网密码：')
    data = {
        "auth_type": "local",
        "username": username,
        "password": password,
    }
    session.post("http://webvpn.tcu.edu.cn/wengine-auth/login/", headers=headers, data=data)


# 登陆教务系统
def login_eduSystem(session, headers):
    login = session.get('http://jwxt.tcu.edu.cn')
    # 将验证码图片保存到本地进行人工识别
    validataCode_image = session.get('http://jwxt.tcu.edu.cn/validateCodeAction.do', headers=headers)
    with open('validataCode.jpg', 'wb') as code:
        code.write(validataCode_image.content)
    validataCode = input('请输入验证码:')
    login_data = {
        "zjh1": "",
        "tips": "",
        "lx": "",
        "evalue": "",
        "eflag": "",
        "fs": "",
        "dzslh": "",
        "zjh": "1705080208",
        "mm": "1705080208",
        "v_yzm": validataCode,
    }
    login = session.post('http://jwxt.tcu.edu.cn/loginAction.do', headers=headers, data=login_data)


# 爬取本学期各项成绩
def get_semesterGrade():
    inquire_grade = session.get('http://jwxt.tcu.edu.cn/bxqcjcxAction.do',headers = headers)
    # title是第一行标题
    # table是每行成绩数据
    title = []
    table = []
    title_1 = re.compile('class="sortable">\r\n\t\t\t\t\t\t(.*?)\r\n\t\t\t\t\t</th>')
    tit1 = re.findall(title_1, inquire_grade.text)
    title_2 = re.compile('class="sortable">(.*?)</th>')
    tit2 = re.findall(title_2, inquire_grade.text)
    title.extend(tit1)
    title.extend(tit2)
    text = re.compile('<td align="center">(.*?)</td>',re.S)
    t = re.findall(text, inquire_grade.text)
    for i in range(len(t)):
        table[i] = t[i].strip()


# 爬取本学期课表
def get_semesterCurr():
    curriculum = session.get("http://jwxt.tcu.edu.cn/xkAction.do?actionType=6",headers = headers)
    class_time = re.compile('<td width="11%">(.*?)</td>')
    time = re.findall(class_time, curriculum.text)
    print(time)
    class_content = re.compile(r'<td>&nbsp;\r\n\r\n(.*?)\r\n\r\n</td>',re.S)
    content = re.findall(class_content, curriculum.text)
    for i in range(len(content)):
        if(content[i] == '&nbsp;'):
            content[i] = ''
            content[i] = content[i].strip(' ')
    print(content)


def main():
    session = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    link_VPN(session, headers)
    login_eduSystem(session, headers)
    get_semesterGrade()
    get_semesterCurr()

main()
# print(t)
# print('{:^10}   {:^10}   {:^30}   {:^15}   {:^6}   {:^10}   {:^15}   {:^15}   {:^6}   {:^6}   {:^4}   {:^15}'.format
#     (title[0], title[1], title[2], title[3], title[4], title[5], title[6], title[7], title[8], title[9], title[10], title[11]))
# for i in range(int(len(t)/12)):
#     print("{:^10}   {:^10}   {:^30}   {:^15}   {:^6}   {:^10}   {:^15}   {:^15}   {:^6}   {:^6}   {:^4}   {:^15}".format
#         (t[i*12+0], t[i*12+1], t[i*12+2], t[i*12+3], t[i*12+4], t[i*12+5], t[i*12+6], t[i*12+7], t[i*12+8], t[i*12+9], t[i*12+10], t[i*12+11]))
