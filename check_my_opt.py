import urllib2, urllib, cookielib, time, json
from myInfo import my_opt_receipt
from bs4 import BeautifulSoup

cookie = cookielib.CookieJar()
OPT_Url = "https://egov.uscis.gov/casestatus/landing.do"
OPT_submit_url = "https://egov.uscis.gov/casestatus/mycasestatus.do"

req = urllib2.Request(OPT_Url)
req.add_header('User-Agent',
               r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36" +
               r"(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.open(req)

req = urllib2.Request(url=OPT_submit_url, data=urllib.urlencode(
    {
        "changeLocale": "",
        "appReceiptNum": my_opt_receipt,
        "initCaseSearch": "CHECK+STATUS"
    })
)
req.add_header('User-Agent',
               r"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36" +
               r"(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
req.add_header("Host", "egov.uscis.gov")
req.add_header("Origin", "https://egov.uscis.gov")
req.add_header("Referer", "https://egov.uscis.gov/casestatus/landing.do")
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(req)

soup = BeautifulSoup(response.read(), 'html.parser')
text = soup.find('div', {
    "class": "rows text-center"
}).find("p").text

print text
