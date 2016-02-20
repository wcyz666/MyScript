import urllib2, urllib, cookielib
from bs4 import BeautifulSoup

Project_Url = "https://theproject.zone"
Submit_Url = "https://theproject.zone/twitter/submit/"

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

cookie = cookielib.CookieJar() 
   
req = urllib2.Request(Project_Url)
req.add_header('User-Agent', r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
auth_url = response.headers['Location']

req = urllib2.Request(auth_url)
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

auth_page = "https://login.cmu.edu" + response.headers['Location']
req = urllib2.Request(auth_page)
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)


soup = BeautifulSoup(response.read(), 'html.parser')
node = soup.find('form')
auth_post_url = "https://login.cmu.edu" + node['action']
req = urllib2.Request(url=auth_post_url, data=urllib.urlencode({"j_username": "", "j_password": "", 'j_continue': 1, '_eventId_proceed': 'Login'}))
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

soup = BeautifulSoup(response.read(), 'html.parser')
node = soup.find('form')
auth_post_url2 = node['action']
nodes = soup.find_all('input')

post_data = {}
for node in nodes:
    if node.attrs.get('name') != None:
        post_data[node.attrs['name']] = node.attrs['value']

req = urllib2.Request(url=auth_post_url2, data=urllib.urlencode(post_data))
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)
		

req = urllib2.Request(Project_Url)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

req = urllib2.Request("https://theproject.zone/student/submissions/3/58")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)


req = urllib2.Request(url=Submit_Url, data=urllib.urlencode({'task': 63, 'course': 3, 'debug': 1, 'project':'p619-phase3', 'query': 'Q1', 'duration': 60, 'dns': 'ec2-52-91-238-122.compute-1.amazonaws.com'}))
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

print response.headers
print response.read()
