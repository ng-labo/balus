#!/usr/bin/env python3
# -*- code: utf-8 -*-
import re, sys
import maxminddb

asnresolver = maxminddb.open_database('GeoLite2-ASN.mmdb')
ccresolver = maxminddb.open_database('GeoLite2-Country.mmdb')

cache = {'IP': {}, 'USER': {}, '_counter':0 }

def process(ip, user):
    if cache['IP'].get(ip) is None:
        asninfo = asnresolver.get(ip)
        asn = asninfo and asninfo.get('autonomous_system_number') and asninfo['autonomous_system_number'] or '-----'
        org = asninfo and asninfo.get('autonomous_system_organization') and asninfo['autonomous_system_organization'] or '-'
        ccinfo = ccresolver.get(ip)
        cc = ccinfo and ccinfo['country']['iso_code'] or '--'
        cache['IP'][ip] = { 'count': 0, 'asn': asn, 'org': org, 'cc': cc }
    if cache['USER'].get(user) is None:
        cache['USER'][user] = { 'count': 0 }
    cache['IP'][ip]['count'] += 1
    cache['USER'][user]['count'] += 1
    cache['_counter'] += 1
    if (cache['_counter']%100) == 0:
        print("====================", datetime.datetime.now().strftime('%c'))
        for ip, v in sorted(cache['IP'].items()):
            print("%-15s %5d %s %6d %s" % (ip, v['count'], v['cc'], v['asn'], v['org']))

while True:
    line = sys.stdin.readline()
    a =re.search(r'Failed password for invalid user (\w)+ from (\d)+\.(\d)+\.(\d)+\.(\d)+', line)
    if a:
        i = a.group(0).split()
        user = i[5]
        ip = i[7]
    else:
        a =re.search(r'Failed password for (\w)+ from (\d)+\.(\d)+\.(\d)+\.(\d)+', line)
        if a:
            i = a.group(0).split()
            user = i[3]
            ip = i[5]
    if a:
        process(ip, user)
