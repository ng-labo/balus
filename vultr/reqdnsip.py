#!/usr/bin/python3
#-*- coding: utf-8 -*-
#
# before calling, target A record must exist already.
# this script will update A record address just only.
#
import sys
import json, urllib.parse
import http.client

ip = sys.argv[1]

import vultrapi
MYDOMAIN = vultrapi.MYDOMAIN
APIKEY = vultrapi.APIKEY

headers = {'Authorization': f"Bearer {APIKEY}"}
hh = http.client.HTTPSConnection('api.vultr.com')
hh.request("GET", f"/v2/domains/{MYDOMAIN}/records", headers=headers)

rs = hh.getresponse()
print(rs.status, rs.reason)
ls = json.loads(rs.read().decode('utf-8'))

for e in ls['records']:
    if e['type'] == 'A' and e['name'] == 'private':
        if e['data'] == ip:
            print("not to update")
            continue
        data = {}
        data['type'] = e['type']
        data['name'] = e['name']
        data['data'] = ip
        headers['Content-Type'] = 'application/json'
        params = json.dumps(data)
        hh.request("PATCH", f"/v2/domains/{MYDOMAIN}/records/{e['id']}", params, headers)
        rs = hh.getresponse()
        print(rs.status, rs.reason)
        if rs.status in [200, 204]:
            print("update A record to", ip)
