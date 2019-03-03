import re
from bs4 import BeautifulSoup
import requests
from lxml import etree
import json

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
    # username = input('校园网账号：')
    # password = input('校园网密码：')
    data = {
        "auth_type": "local",
        "username": "1705080207",  # username,
        "password": "19970515",  # password,
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
        "zjh": "1705080209",
        "mm": "1705080209",
        "v_yzm": validataCode,
    }
    login = session.post('http://jwxt.tcu.edu.cn/loginAction.do', headers=headers, data=login_data)


# 爬取本学期各项成绩
def get_semesterGrade(session, headers):
    inquire_grade = session.get('http://jwxt.tcu.edu.cn/bxqcjcxAction.do', headers=headers)
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
    text = re.compile('<td align="center">(.*?)</td>', re.S)
    t = re.findall(text, inquire_grade.text)
    for i in range(len(t)):
        table[i] = t[i].strip()


def cache(cache, class_num):
    cache["class_pyfa"] = ''.join(class_num[0].split())
    cache["class_num"] = ''.join(class_num[1].split())
    cache["class_name"] = ''.join(class_num[2].split())
    cache["class_order"] = ''.join(class_num[3].split())
    cache["grade"] = ''.join(class_num[4].split())
    cache["class_attribute"] = ''.join(class_num[5].split())
    cache["test"] = ''.join(class_num[6].split())
    cache["teacher"] = (''.join(class_num[7].split()))[:-1]
    cache["learn"] = ''.join(class_num[9].split())
    cache["class_status"] = ''.join(class_num[10].split())
    return cache


# 爬取本学期课表
def get_semesterCurr(session, headers):
    curriculum = session.get("http://jwxt.tcu.edu.cn/xkAction.do?actionType=6", headers=headers)
    tree = etree.HTML(curriculum.text)
    # print(tree.xpath('//tr[@onmouseout="this.className=\'even\';"]'))
    tr_list = tree.xpath('//tr[@onmouseout="this.className=\'even\';"]')
    cache = {}
    class_list = []
    # count = 0
    for i_content in tr_list:
        class_info = {}
        class_num = i_content.xpath('./td/text()')
        if len(class_num) > 7:
            # 培养方案
            class_info["class_pyfa"] = ''.join(class_num[0].split())
            # 课程号
            class_info["class_num"] = ''.join(class_num[1].split())
            # 课程名
            class_info["class_name"] = ''.join(class_num[2].split())
            # 课序号
            class_info["class_order"] = ''.join(class_num[3].split())
            # 学分
            class_info["grade"] = ''.join(class_num[4].split())
            # 课程属性
            class_info["class_attribute"] = ''.join(class_num[5].split())
            # 考试类型
            class_info["test"] = ''.join(class_num[6].split())
            # 教师
            class_info["teacher"] = (''.join(class_num[7].split()))[:-1]
            # 修读方式
            class_info["learn"] = ''.join(class_num[9].split())
            # 选课状态
            class_info["class_status"] = ''.join(class_num[10].split())
            # 对class_info进行缓存（采用copy方法进行浅拷贝即可）
            cache = class_info.copy()
            # 周次
            class_info["week"] = ''.join(class_num[11].split())
            # 星期
            class_info["week_day"] = ''.join(class_num[12].split())
            # 节次
            class_info["session"] = ''.join(class_num[13].split())
            # 节数
            class_info["section_num"] = ''.join(class_num[14].split())
            # 校区
            class_info["campus"] = ''.join(class_num[15].split())
            # 教学楼
            class_info["teach_build"] = ''.join(class_num[16].split())
            # 教室
            class_info["classroom"] = ''.join(class_num[17].split())
        else:
            class_info = cache
            # 周次
            class_info["week"] = ''.join(class_num[0].split())
            # 星期
            class_info["week_day"] = ''.join(class_num[1].split())
            # 节次
            class_info["session"] = ''.join(class_num[2].split())
            # 节数
            class_info["section_num"] = ''.join(class_num[3].split())
            # 校区
            class_info["campus"] = ''.join(class_num[4].split())
            # 教学楼
            class_info["teach_build"] = ''.join(class_num[5].split())
            # 教室
            class_info["classroom"] = ''.join(class_num[6].split())
        class_list.append(class_info)
    for class_info in class_list:
        print(class_info)
    with open ('class.json', 'w') as f:
        json.dump(class_list, f)

def main():
    session = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    link_VPN(session, headers)
    login_eduSystem(session, headers)
    # get_semesterGrade(session, headers)
    get_semesterCurr(session, headers)


main()
# print(t)
# print('{:^10}   {:^10}   {:^30}   {:^15}   {:^6}   {:^10}   {:^15}   {:^15}   {:^6}   {:^6}   {:^4}   {:^15}'.format
#     (title[0], title[1], title[2], title[3], title[4], title[5], title[6], title[7], title[8], title[9], title[10], title[11]))
# for i in range(int(len(t)/12)):
#     print("{:^10}   {:^10}   {:^30}   {:^15}   {:^6}   {:^10}   {:^15}   {:^15}   {:^6}   {:^6}   {:^4}   {:^15}".format
#         (t[i*12+0], t[i*12+1], t[i*12+2], t[i*12+3], t[i*12+4], t[i*12+5], t[i*12+6], t[i*12+7], t[i*12+8], t[i*12+9], t[i*12+10], t[i*12+11]))
