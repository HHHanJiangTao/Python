import requests
import re
import json
import time
import logging
from dLog import dLog
import os

log = dLog('crawler','w',logging.DEBUG,logging.DEBUG)

def get_one_page(url):
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index' : item[0],
            'tmage' : item[1],
            'title' : item[2].strip(),
            'actor' : item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time'  : item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score' : item[5] + item[6]
        }

def write_to_file(s):
    with open('TOP100.txt',mode='a+',encoding='utf-8') as f:
        f.write(json.dumps(s,ensure_ascii=False) + '\n')
        f.close()

def crawler(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
        

if __name__ == "__main__":
    for i in range(0,10,1):
        crawler(i*10)
        time.sleep(1)
    pass