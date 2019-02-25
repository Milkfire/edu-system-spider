import requests
import hashlib
import re


def md5(pwd):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(pwd.encode(encoding='utf-8'))
    return hl.hexdigest()


# 对字符串加工处理
def working(string):
    string = string[0:30].upper()
    return string


# 密码编译
def pwdMD5(pwd):
    # MD5加密后加'盐'
    pwd = md5(pwd)
    pwd1 = '172207300123' + working(pwd) + '11072'
    # 对加'盐'密码再次MD5加密
    pwd1 = md5(pwd1)
    pwd2 = working(pwd1)
    return pwd2


# 验证码编译
def yzmMD5(yzm):
    yzm = md5(yzm.upper())
    yzm1 = md5(working(yzm) + '11072')
    yzm2 = working(yzm1)
    return yzm2


index_url = 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx'
yzm_url = 'http://210.42.72.73:888/jwweb/sys/ValidateCode.aspx'
session = requests.session()
headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'Content-Length': '591',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=10xqnyjqkkjqor45gng4xk45',
    'Host': '210.42.72.73:888',
    'Origin': 'http://210.42.72.73:888',
    'Pragma': 'no-cache',
    # 'Referer': 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
pic_headers = {
    'Referer': 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
index_html = session.get(index_url,headers=headers)
pic_pattern = re.compile('<td align="center" rowspan="3" ><img id="imgCode" src="..(.*?)" onclick=')
pic_url = re.findall(pic_pattern,index_html.text)
# yzm_url = 'http://210.42.72.73:888/jwweb'+pic_url[0]
# yzm_url = 'http://210.42.72.73:888/jwweb/sys/ValidateCode.aspx'
yzm_pic = session.get(yzm_url, headers=pic_headers)
with open('yzm.jpg', 'wb') as f:
    f.write(yzm_pic.content)
user_name = '172207300123'  #input("请输入学号：")
pwd = 'yang1321' #input("请输入密码：")
yzm = input("请输入验证码：")
pwd2 = pwdMD5(pwd)
yzm2 = yzmMD5(yzm)
post_data = {
    '__VIEWSTATE': 'dDw2ODQ1MDg1MDA7Oz5HxP9gFS3WlqjSvPw6ewfRgfrjYA==',
    'pcInfo': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36undefined5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36 SN:NULL',
    'typeName': '(unable to decode value)',
    'dsdsdsdsdxcxdfgfg': pwd2,
    'fgfggfdgtyuuyyuuckjg': yzm2,
    'Sel_Type': 'STU',
    'txt_asmcdefsddsd': '172207300123',
    'txt_pewerwedsdfsdff': '',
    'txt_sdertfgsadscxcadsads': '',
    'sbtState': '',
    'txt_mm_lxpd': '',
}
login_html = session.post(index_url,data=post_data,headers=headers)
print(login_html.text)

