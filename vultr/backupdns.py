#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import http.client, urllib.parse
import json, urllib.parse

import vultrapi
APIKEY = vultrapi.APIKEY

headers = {'API-Key': APIKEY}

def exec(domain):
    hh = http.client.HTTPSConnection('api.vultr.com')
    hh.request("GET", "/v1/dns/records?domain=" + domain, headers=headers)

    rs = hh.getresponse()
    print(rs.status, rs.reason)
    ls = json.loads(rs.read().decode('utf-8'))

    store = []
    for e in ls:
        store.append(e)
    return store

if __name__=='__main__':
    if len(sys.argv)!=2:
        print("command [domain]")
        sys.exit(1)
    domain = sys.argv[1]
    store = exec(domain)
    json.dump(store, open('DNS_'+domain+'.json', 'w'))
