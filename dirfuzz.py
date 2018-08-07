#!/usr/bin/env python
# encoding: utf-8

import time
import asyncio

urls = [
    'http://www.163.com/',
    'http://www.sina.com.cn/',
    'https://www.hupu.com/',
    'http://www.csdn.net/'
]

async def check_url(url):
    print(url)


async def request_url(u):
    res = await check_url(u)
    time.sleep(5)
    return res


loop = asyncio.get_event_loop()
task_list = asyncio.wait([request_url(u) for u in urls])
all_res, _ = loop.run_until_complete(task_list)
loop.close()
