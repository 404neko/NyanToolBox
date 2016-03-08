#google_cache_dump.py

import os
import hashlib
import requests
from bs4 import BeautifulSoup

OUTPUT = 'output'
PROXY = {
            'http':'http://127.0.0.1:8118',
            'https':'https://127.0.0.1:8118'
}

header = {
            'User-Agent':'Mozilla/4.0 (Windows; MSIE 6.0; Windows NT 5.2)',
}

#old_fun
def FileNameFiler(String,Replacment='_'):
    List=['/','\\','*',':','?','"','<','>','|']
    New=''
    for i in String:
        if i not in List:
            New+=i
        else:
            New+=Replacment
    return New

#old_fun
def CreatFolder(Path):
    if Path.find('/')==-1:
        if not os.path.exists(Path):
            os.mkdir(Path)
    else:
        Path=Path.split('/')
        Path0=''
        for PathItem in Path:
            Path0=Path0+PathItem+'/'
            if not os.path.exists(Path0):
                os.mkdir(Path0)

def get_md5(data):
    hash_ = hashlib.md5()
    hash_.update(data)
    return hash_.hexdigest()

def page(num):
    if num-1==0:
        return 0
    else:
        return num*10-10

def get(url):
    return requests.get(url, headers = header, proxies = PROXY)

google_domain = 'http://www.google.com'
url_base = google_domain + '/search?q=%s&start=%s'

def main(keyword,end,protocol='http://'):
    for i in range(1,end):
        respon = get(url_base % (keyword,str(page(i))))
        content = respon.content
        soup = BeautifulSoup(content,'lxml')
        node = soup.findAll('div',{'id':'ires'})[0]
        node = node.ol
        for g in node:
            title = g.h3.a.text

            #link = protocol + g.findAll('cite')[0].text
            cache_link = g.findAll('a',{'class':'Z_Zkb'})
            if len(cache_link)>=1:
                cache_link = google_domain+cache_link[0]['href']
            else:
                print 'No cache: ' + protocol+g.findAll('cite')[0].text
                continue

            try:
                url = link
            except:
                url = cache_link
            uid = get_md5(url)[:4]

            file_name = FileNameFiler(title)
            respon = get(url)
            content = respon.content
            file_handle = open(OUTPUT+os.sep+file_name + '_' + uid + '.html','wb')
            file_handle.write(content)
            file_handle.close()

CreatFolder(OUTPUT)
main('site:0nly3nd.sinaapp.com',5+1)