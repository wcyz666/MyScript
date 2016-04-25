import urllib2, urllib, cookielib, time, json
from myInfo import my_cmu_id, my_cmu_pass
from bs4 import BeautifulSoup
import query_config
from query_config import query_param, current

cookie = cookielib.CookieJar()
Project_Url = "https://theproject.zone"
Submit_Url = "https://theproject.zone/twitter/submit/"


class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def __init__(self):
        pass

    def http_error_302(self, _req, fp, code, msg, headers):
        infour = urllib.addinfourl(fp, headers, _req.get_full_url())
        infour.status = code
        infour.code = code
        return infour

    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


def get_last_rps(pageid, taskid):
    req_rps = urllib2.Request(
        "https://theproject.zone/student/submissions/14/%d/?task=%d&_=%s" % (pageid, taskid, str(int(time.time() * 1000))))
    req_rps.add_header("X-Requested-With", "XMLHttpRequest")
    opener_rps = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response_rps = opener_rps.open(req_rps)
    page = json.loads(response_rps.read())
    try:
        result = page['data'][1][6]
        return result
    except:
        return ""


req = urllib2.Request(Project_Url)
req.add_header('User-Agent',
               r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36" +
               r"(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
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
req = urllib2.Request(url=auth_post_url, data=urllib.urlencode(
    {
        "j_username": my_cmu_id,
        "j_password": my_cmu_pass,
        'j_continue': 1,
        '_eventId_proceed': 'Login'
    }))
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

soup = BeautifulSoup(response.read(), 'html.parser')
node = soup.find('form')
auth_post_url2 = node['action']
nodes = soup.find_all('input')

post_data = {}
for node in nodes:
    if node.attrs.get('name') is not None:
        post_data[node.attrs['name']] = node.attrs['value']

req = urllib2.Request(url=auth_post_url2, data=urllib.urlencode(post_data))
opener = urllib2.build_opener(MyHTTPRedirectHandler, urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

req = urllib2.Request(Project_Url)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

req = urllib2.Request("https://theproject.zone/student/submissions/14/69")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

count = 0


while True:
    reload(query_config)
    config = query_param[current]
    req = urllib2.Request(url=Submit_Url, data=urllib.urlencode(config))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    page = response.read()

    if " Submitted successfully" in page:

        count += 1
        print current + " Submitted successfully, #" + str(count) + " submission, at " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        print " Last RPS: " + get_last_rps(config['page'], config['task'])
    time.sleep(5)