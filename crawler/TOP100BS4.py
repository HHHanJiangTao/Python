import requests
import re
import json
import time
import logging
from dLog import dLog
import os
from bs4 import BeautifulSoup

log = dLog('crawler','w',logging.DEBUG,logging.DEBUG)

def get_one_page(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text.encode().decode('utf-8')
    return None

def parse_one_page(html):
    soup = BeautifulSoup(html,'lxml')
    with open('html.txt','w',encoding='utf-8') as fp:
        fp.write(soup.prettify())
        fp.close()
    for item in soup.find_all(attrs={'class':'board-index'}):
        parent = item.find_parent()
        # print(type(parent))
        # print(parent.i.string)
        # print(parent.a.find(attrs = {'class':'board-img'}).attrs['data-src'])
        # print(parent.find(attrs = {'class':'name'}).string)
        # print(parent.find(attrs = {'class':'star'}).string.strip()[3:] if len(parent.find(attrs = {'class':'star'}).string) > 3 else '')
        # print(parent.find(attrs = {'class':'releasetime'}).string.strip()[5:] if len(parent.find(attrs = {'class':'star'}).string) > 5 else '')
        # print(parent.find(attrs = {'class':'integer'}).string + parent.find(attrs = {'class':'fraction'}).string)
        yield{
            'index' : parent.i.string,
            'image' : parent.a.find(attrs = {'class':'board-img'}).attrs['data-src'],
            'name'  : parent.find(attrs = {'class':'name'}).string,
            'actor' : parent.find(attrs = {'class':'star'}).string.strip()[3:] if len(parent.find(attrs = {'class':'star'}).string) > 3 else '',
            'time'  : parent.find(attrs = {'class':'releasetime'}).string.strip()[5:] if len(parent.find(attrs = {'class':'star'}).string) > 5 else '',
            'score' : parent.find(attrs = {'class':'integer'}).string + parent.find(attrs = {'class':'fraction'}).string
        }

def write_to_file(s):
    with open('TOP100BS4.txt',mode='a+',encoding='utf-8') as f:
        f.write(json.dumps(s,ensure_ascii=False) + '\n')
        f.close()

def crawler(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
        

if __name__ == "__main__":
    for i in range(0,10,1):
        crawler(i*10)
        time.sleep(1)
    pass
