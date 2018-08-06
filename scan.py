#!/usr/bin/env python
# encoding: utf-8

import sys
import asyncio
import aiodns
import requests
import json

tasks = []


def dns_scan():
    print(sys.argv[1])
    domain = sys.argv[1]

    loop = asyncio.get_event_loop()

    dns = "114.114.114.114"

    with open('./bitquark_20160227_subdomains_popular_1000') as f:
        for domain_keyword in f:
            domain_keyword = domain_keyword.strip()
            subdomain = domain_keyword+'.'+domain

            try:
                resolver = aiodns.DNSResolver(loop=loop, nameservers=[dns])
                f = resolver.query(subdomain, 'A')
                result = loop.run_until_complete(f)
                print(subdomain)
            except Exception as e:
                result = "NO DNS"
                #print("NO DNS")

    loop.close()


def ctfr_scan():

    domain = sys.argv[1]
    target = domain
    subdomains = []

    req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=target))

    if req.status_code != 200:
        print("[X] Information not available!")
        exit(1)

    json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

    #for (key,value) in enumerate(json_data):
    #    subdomains.append(value['name_value'])

    print(json_data)


def main():
    #dns_scan()
    ctfr_scan()

if __name__ == '__main__':
    main()
