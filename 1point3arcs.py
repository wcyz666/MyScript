# -*- coding:utf-8 -*-  

import urllib2, urllib, cookielib, md5, re
from myInfo import my1point3Username as username
from myInfo import my1point3Password as password

def processMD5(password):
    m = md5.md5()
    m.update(password)
    return m.hexdigest()
    
def generateLoginInfo(username, password):
    info = {}
    info['username'] = username
    info['password'] = processMD5(password)
    info['cookietime'] = 2592000
    info['quickforward'] = 'yes'
    info['handlekey'] = 'ls'
    return urllib.urlencode(info)

def generatePopUpUrl(token):
    return "http://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&%s&infloat=yes&handlekey=dsu_paulsign&inajax=1&ajaxtarget=fwin_content_dsu_paulsign" % (token)
    
def generateQianDaoInfo(token):
    return "formhash=%s&qdxq=kx&qdmode=2&todaysay=&fastreply=0" % (token)
    
def request(_url, _data=None):
    req = urllib2.Request(url=_url, data=_data)
    req.add_header('User-Agent', r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    return opener.open(req)
    
    

Login_Url = "http://www.1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
BBS_Url = "http://www.1point3acres.com/bbs"
QianDao_URL = "http://www.1point3acres.com/bbs/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1"

cookie = cookielib.CookieJar() 

#login   
request(Login_Url, _data=generateLoginInfo(username, password))

#get webpage
response = request(BBS_Url)
page = response.read()[:15000]
target_str = page[page.find('id=dsu_paulsign:sign&'):]
m = re.search(r'id=dsu_paulsign:sign&(\w+)', target_str)
token = ""
if m:
    token = m.group(1)

    request(generatePopUpUrl(token))

    response = request(QianDao_URL, _data=generateQianDaoInfo(token)).read()

    if "return_win" in response:
        print u"恭喜你签到成功!"
else:
    print u"你已经签到了！"

