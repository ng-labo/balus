import http.client as httpc
import json

import slackids
pathes = slackids.incominghooks

def sendmsg(msg):
    if type(msg)==type(''):
        msg = { 'text': msg }
    if type(msg)!=type({}):
        raise RuntimeError
    if msg.get('text') is None:
        raise RuntimeError
    conn = httpc.HTTPSConnection('hooks.slack.com')
    for p in pathes:
        conn.request('POST', p, json.dumps(msg), { 'Content-type': 'application/json' })
        r = conn.getresponse()

