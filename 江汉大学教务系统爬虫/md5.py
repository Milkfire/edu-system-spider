import hashlib

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
