#!/usr/bin/env python
# encoding: utf-8

import asyncio
import aiodns

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
f = resolver.query('baidu.com', 'A')
result = loop.run_until_complete(f)

print(result)
