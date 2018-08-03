#!/usr/bin/env python
# encoding: utf-8

import sys
import asyncio
import aiodns

tasks = []


def main():
    print(sys.argv[1])
    domain = sys.argv[1]

    loop = asyncio.get_event_loop()

    with open('./bitquark_20160227_subdomains_popular_1000') as f:
        for domain_keyword in f:
            domain_keyword = domain_keyword.strip()
            subdomain = domain_keyword+'.'+domain

            try:
                resolver = aiodns.DNSResolver(loop=loop)
                f = resolver.query(subdomain, 'A')
                result = loop.run_until_complete(f)
                print(subdomain)
            except Exception as e:
                result = "NO DNS"

    loop.close()


if __name__ == '__main__':
    main()
