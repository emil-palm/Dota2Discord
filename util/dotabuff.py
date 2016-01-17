from lxml import html
import requests

def get_username_from_uid(uid):
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'})
    page = s.get("http://dotabuff.com/players/%s" % uid)
    tree = html.fromstring(page.content)
    #users = tree.xpath('//div.header-content-title/h1/text()')
    users = tree.xpath('/html/body/div[1]/div[7]/div[2]/div[1]/div[1]/div[2]/h1/text()')
    if len(users) > 0:
        return users[0]
    else:
        return None

