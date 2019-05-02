from lnapi import KEY
from lnapi import ID

print(len(KEY), len(ID))

import http.client as http
import urllib.parse as urllib
import json, time
import hmac, hashlib
import requests

AP = 'dynamic.lunanode.com'


CATEGORY = 'vm'
ACTION = 'list'

handler = '%s/%s/' % (CATEGORY, ACTION )
url = 'https://%s/api/%s' % ( AP, handler ) 
print(handler)

rq = {}
rq['api_id'] = ID
rq['api_partialkey'] = KEY[:64]

request_raw = json.dumps(rq)
nonce = str(time.time())

hasher = hmac.new(bytes(KEY, 'utf-8'), bytes('{handler}|{raw}|{nonce}'.format(handler=handler, raw=request_raw, nonce=nonce), 'utf-8'), hashlib.sha512)
signature = hasher.hexdigest()


headers = {}
headers['Content-Type'] = 'application/x-www-form-urlencoded'
data = {'req': request_raw, 'signature': signature, 'nonce': nonce}
print(data)

conn = http.HTTPSConnection(AP)
conn.request('POST', '/api/' + handler, urllib.urlencode(data), headers)
rs = conn.getresponse()
print(rs.status, rs.reason)
print(rs.read())

