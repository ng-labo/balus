#!/usr/bin/python3
#-*- coding: utf-8 -*-
#
# before calling, target A record must exist already.
# this script will update A record address just only.
#
import sys
import json, urllib.parse

ip = sys.argv[1]

import vultrapi
MYDOMAIN = vultrapi.MYDOMAIN
APIKEY = vultrapi.APIKEY

headers = {'API-Key': APIKEY}
hh = http.client.HTTPSConnection('api.vultr.com')
hh.request("GET", "/v1/dns/records?domain=" + MYDOMAIN, headers=headers)

rs = hh.getresponse()
print(rs.status, rs.reason)
ls = json.loads(rs.read().decode('utf-8'))

for e in ls:
    if e['type'] == 'A' and e['name'] == 'private':
        if e['data'] == ip:
            print("not to update")
            continue
        data = {}
        data['domain'] = MYDOMAIN
        data['type'] = e['type']
        data['name'] = e['name']
        data['RECORDID'] = e['RECORDID']
        data['data'] = ip
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        params = urllib.parse.urlencode(data)
        hh.request("POST", "/v1/dns/update_record", params, headers)
        rs = hh.getresponse()
        print(rs.status, rs.reason)
        if rs.status==200:
            print("update A record to", ip)
