#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import asyncio
import requests

urls = [
    'http://www.163.com/',
    'http://www.sina.com.cn/',
    'https://www.hupu.com/',
    'http://www.csdn.net/'
]

def generate_dict(domain):
    dir_dict = []
    with open("./web_dir.dic") as d:
        for dir_keyword in d:
            dir_keyword = dir_keyword.strip()
            target_url = domain + '/' + dir_keyword
            dir_dict.append(target_url)
    return dir_dict


async def check_url(url):
    r = requests.get(url)
    if r.status_code != 400:
        print(r.url)
    else:
        print("404 error")


async def request_url(u):
    res = await check_url(u)
    time.sleep(0.5)
    return res


def main():
    domain = sys.argv[1]
    urls = generate_dict(domain)
    loop = asyncio.get_event_loop()
    task_list = asyncio.wait([request_url(u) for u in urls])
    all_res, _ = loop.run_until_complete(task_list)
    loop.close()


if __name__ == "__main__":
    main()
