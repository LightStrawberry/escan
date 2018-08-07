#!/usr/bin/env python
# encoding: utf-8

import sys
import asyncio
import aiodns
import requests
import json
import argparse


class Escan():
    def __init__(self, target_domain, output_path, show_expired, domain_dict):
        self.target_domain = target_domain
        self.output_path = output_path
        self.show_expired = show_expired
        self.subdomains = []
        if domain_dict:
            self.domain_dict = domain_dict
        else:
            self.domain_dict = './bitquark_20160227_subdomains_popular_1000'
        self.dns = "114.114.114.114"


    def dns_scan(self):
        loop = asyncio.get_event_loop()
        dns = "114.114.114.114"
        subdomains = []

        with open(self.domain_dict) as f:
            for domain_keyword in f:
                domain_keyword = domain_keyword.strip()
                subdomain = domain_keyword+'.'+self.target_domain

                try:
                    resolver = aiodns.DNSResolver(loop=loop, nameservers=[self.dns])
                    f = resolver.query(subdomain, 'A')
                    result = loop.run_until_complete(f)
                    print("[-] {s}".format(s=subdomain))
                    self.subdomains.append(subdomain)
                except Exception as e:
                    result = "NO DNS"
                    #print("NO DNS")
        loop.close()


    def ctfr_scan(self):
        subdomains = []
        req = requests.get("https://crt.sh/?q=%.{d}&output=json".format(d=self.target_domain))

        if req.status_code != 200:
            print("[X] Information not available!")
            exit(1)

        json_data = json.loads('[{}]'.format(req.text.replace('}{', '},{')))

        for (key,value) in enumerate(json_data):
            subdomains.append(value['name_value'])

        subdomains = sorted(set(subdomains))

        if self.show_expired:
            loop = asyncio.get_event_loop()
            for s in subdomains:
                try:
                    resolver = aiodns.DNSResolver(loop=loop, nameservers=[self.dns])
                    f = resolver.query(s, 'A')
                    result = loop.run_until_complete(f)
                    print("[-] {s}".format(s=s))
                    self.subdomains.append(s)
                except Exception as e:
                    pass
        else:
            for s in subdomains:
                print("[-] {s}".format(s=s))
                self.subdomains.append(s)


    def search_engine_scan(self):
        pass


    def output_result(self):
        subdomains = sorted(set(self.subdomains))
        for s in subdomains:
            with open(self.output_path,"a") as f:
                f.write(s + '\n')
                f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest="target_domain", type=str, help="target domain", required=True)
    parser.add_argument('-o', dest="output_path", type=str, help="output path")
    parser.add_argument('-e', dest="show_expired", action="store_true", help="show expired")
    parser.add_argument('-D', dest="subdomain_dict", type=str, help="subdomain dict path")
    args = parser.parse_args()

    escan = Escan(args.target_domain, args.output_path, args.show_expired, args.subdomain_dict)

    print(">> start dns scan ...")
    escan.dns_scan()
    print(">> start ctfr scan ...")
    escan.ctfr_scan()
    if args.output_path:
        escan.output_result()

if __name__ == '__main__':
    main()
