import json
import requests
import re
from requests.exceptions import RequestException
from multiprocessing import pool, Pool


def get_one_page(url):#得到HTML代码
    my_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = my_headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def HTML_pase(html):
    Regular_Expressions = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?title="(.*?)".*?star">(.*?)</p>.*?'
                                     'releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?">(.*?)</i>',re.S)#正则表达式
    content = re.findall(Regular_Expressions,html)
    for item in content:
        yield {
            "排    名:": item[0],
            "电 影 名:": item[1],
            "主    演" : item[2].strip()[3:],
            "上映时间" : item[3],
            "评    分" : item[4] + item[5]
        }
def file_Write(content):
    with open('C:\\Users\\detail\\Desktop\\maoyan.txt', 'a',encoding='utf-8') as file:
        print(json.dumps(content,ensure_ascii=False))
        file.write(json.dumps(content,ensure_ascii=False) + "\n")
    file.close()

def main(offset):
    url = 'https://maoyan.com/board/4?' + "offset=" + str(offset)
    text = get_one_page(url)
    for item in HTML_pase(text):
        print(item)
        file_Write(item)


if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i * 10 for i in range(0, 10)])
    for i in range(0,10):
        main(str(i*10))