#!/usr/bin/env python3

import subprocess
import os, stat, time
import json
import traceback

from defines import *
import slack

def sockname(hostname):
   return "/tmp/%s@%s:%d" % ( 'nao', hostname, 22 )

def init_node_stat():
    node_stat = dict.fromkeys(NODES)
    try:
        node_stat = json.load(open(NODESTAT))
    except:
        print('not found node_stat.json')
    return node_stat

def okaysocket(node):
    socketfile = sockname(node)
    ret = False
    try:
        s = os.stat(socketfile)
        ret = stat.S_ISSOCK(s.st_mode)
    except:
        traceback.print_exc()
    return ret

def recover(node, curstat):
    if curstat == 'ok':
        slack.sendmsg(node + ":NG")
    sshcmd = list(SSHCMDTMPL)
    sshcmd.append(node)
    sshcmd.append('exit')
    sshcmd.append('0')
    ret = 'ng'
    try:
        r =subprocess.run(sshcmd)
        if r.returncode==0:
            ret = 'ok'
    except:
        pass
    return ret

def main():
    node_stat = init_node_stat()
    for node in NODES:
        hostname = node + '.' + DOMAIN
        st = okaysocket(hostname)
        if st==True:
            node_stat[node] = 'ok'
        else:
            node_stat[node] = recover(hostname, node_stat[node])
            if node_stat[node] == 'ok':
                slack.sendmsg(node + ":RECOVERED")

    json.dump(node_stat, open(NODESTAT, 'w'))

main()
