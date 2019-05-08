import re, sys
import maxminddb

asnresolver = maxminddb.open_database('GeoLite2-ASN.mmdb')
ccresolver = maxminddb.open_database('GeoLite2-Country.mmdb')
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
        asninfo = asnresolver.get(ip)
        asn = asninfo and asninfo['autonomous_system_number'] or '-----'
        org = asninfo and asninfo['autonomous_system_organization'] or '-'
        ccinfo = ccresolver.get(ip)
        cc = ccinfo and ccinfo['country']['iso_code'] or '--'
        print(ip, cc, asn, org, user)
