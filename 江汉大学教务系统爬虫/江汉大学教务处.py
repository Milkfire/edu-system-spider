import requests
import md5
import hashlib

# 登陆网址和验证码网址
index_url = 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx'
yzm_url = 'http://210.42.72.73:888/jwweb/sys/ValidateCode.aspx'

# 先创建一个会话，方便之后的Cookies管理
session = requests.session()
# 登陆的POST请求头
# 在这里重点强调一点关于Referer的属性，因为这个在本爬虫里面起到关键作用，可能是因为系统的防御机制
# Referer是反应你的请求来自哪个地方的值，一般简单网站都不会控制这个属性，了解一下就行了
# 如果没有该属性会出现一个页面错误的HTML消息，什么请联系管理员巴拉巴拉之类的废话，出现这种情况多半是该原因
headers = {
    'Host': '210.42.72.73:888',
    'Origin': 'http://210.42.72.73:888',
    'Pragma': 'no-cache',
    'Referer': 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',

}
# 这个是验证码图片的GET请求
# 如果缺少Referer属性会在登陆时显示验证码错误，我猜应该是缺少该属性时抓取的验证码图片不是此时登陆时需要的验证码
pic_headers = {
    'Referer': 'http://210.42.72.73:888/jwweb/_data/index_LOGIN.aspx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
# 访问验证码网址，并将返回的二进制图片保存在本地'yzm.jpg'中
yzm_pic = session.get(yzm_url, headers=pic_headers)
with open('yzm.jpg', 'wb') as f:
    f.write(yzm_pic.content)
# 收集用户的登陆信息，进行接下来的登陆行为
user_name = input("请输入学号：")
pwd = input("请输入密码：")
# 这里打开本地验证码图片观看后填写
yzm = input("请输入验证码：")
# 然后模仿系统对密码和验证码的加密过程
pwd2 = md5.pwdMD5(pwd)
yzm2 = md5.yzmMD5(yzm)
# 得到应该提交的表单内容
post_data = {
    # 密码
    'dsdsdsdsdxcxdfgfg': pwd2,
    # 验证码
    'fgfggfdgtyuuyyuuckjg': yzm2,
    # 身份
    'Sel_Type': 'STU',
    # 学号
    'txt_asmcdefsddsd': '172207300123',
}
# 模拟登陆行为
login_html = session.post(index_url, data=post_data, headers=headers)
# 打印抓取结果看是否登陆成功
# 后续应该会完善此处
print(login_html.text)
# main_url = 'http://210.42.72.73:888/jwweb/MAINFRM.aspx'
# 课表的网址
curriculum_url = 'http://210.42.72.73:888/jwweb/znpk/Pri_StuSel_Drawimg.aspx?type=2&w=1060&h=680&xnxq=20181&px=0'
# 课表的请求头
curriculum_headers = {
    'Referer': 'http://210.42.72.73:888/jwweb/znpk/Pri_StuSel_rpt.aspx?m=c4QfQA9ahP48kw8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
# 通过GET请求获得课表图片并写入本地'curriculum.jpg'
curriculum = session.get(curriculum_url, headers=curriculum_headers)
with open('curriculum.jpg', 'wb') as f:
    f.write(curriculum.content)
