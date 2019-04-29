#!/usr/bin/env python3

LOCATIONS = [ 'tokyo', 'moscow' ]

import sys
HOST = 'tokyo'
DOMAIN = 'domain'
if len(sys.argv)>1: HOST = sys.argv[1]
if len(sys.argv)>2: DOMAIN = sys.argv[2]

from scapy.all import *

ping4 = {}
ping6 = {}
for dst in LOCATIONS:
    if HOST==dst:continue
    target = '.'.join([dst, DOMAIN])
    ping4[dst] = IP(dst=target)/ICMP()
    ping6[dst] = IPv6(dst=target)/ICMPv6EchoRequest()

for dst in LOCATIONS:
    if HOST==dst:continue
    t = time.time()
    r4 = sr1(ping4[dst], verbose=0, timeout=5)
    r6 = sr1(ping6[dst], verbose=0, timeout=5)
    r4hopn = r4 and 64-r4.ttl or "-"
    r6hopn = r6 and 64-r6.hlim or "-"
    print(dst, r4hopn, r6hopn)

