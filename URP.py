import requests


def getURL(url):
    r = requests.get(url)
    return r.text


def main():
    url = "http://172.16.88.101:9001/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '81',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=ahdMvwMW3LFv8-Cow-BGw',
        'Host': '172.16.88.101:9001',
        'Origin': 'http://172.16.88.101:9001',
        'Referer': 'http://172.16.88.101:9001/logout.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    username = 1705080208
    password = 1705080208
    date = {
        'zjh1': '',
        'tips': '',
        'lx': '',
        'evalue': '',
        'eflag': '',
        'fs': '',
        'dzslh': '',
        'zjh': '1705080208',
        'mm': '1705080208',
        'v_yzm': '6guh'
    }
    #tcu_session = requests.session()
    res = requests.post(url + 'loginAction.do', headers, date)
    #print(res.status_code)
    print(res.text)
    #html = getURL(url)
    #print(html)


main()
