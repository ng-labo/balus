#!/usr/bin/env python3

import subprocess
import os, time
import json

import satellites
import slack

NODESTAT = 'node_stat.json'
sshcmd = [ '/usr/bin/ssh', '-q', '-F/dev/null', '-oPasswordAuthentication=no', '-oKbdInteractiveAuthentication=no', '-oUseRoaming=no', '-oStrictHostKeyChecking=no' ,'-oConnectTimeout=20', '-oServerAliveCountMax=120', '-oServerAliveInterval=1', '-oControlPath=/tmp/%r@%h:%p', '-oControlMaster=auto', '-oControlPersist=yes', '-p', '22' ]

node_stat = dict.fromkeys(satellites.satellites)
try:
    node_stat = json.load(open(NODESTAT))
except:
    print('not found node_stat.json')

def recover(node, curstat):
    if curstat == 'ok':
        slack.sendmsg(node + ":NG")
    node_stat[node] = 'ng'
    sshcmd.append(node)
    sshcmd.append('exit')
    sshcmd.append('0')
    ret = 'ng'
    try:
        subprocess.run(sshcmd)
        ret = 'ok'
    except:
        pass
    return ret

for node in satellites.satellites:
    socketfile = '/tmp/'  + node + ':22'
    try:
        os.stat(socketfile)
        node_stat[node] = 'ok'
    except:
        node_stat[node] = recover(node, node_stat[node])
        if node_stat[node] == 'ok':
            slack.sendmsg(node + ":RECOVERED")

json.dump(open(NODESTAT, 'w'))
