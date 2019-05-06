sshcmd = [ '/usr/bin/ssh', '-q', '-F/dev/null', '-oPasswordAuthentication=no', '-oKbdInteractiveAuthentication=no', '-oUseRoaming=no', '-oStrictHostKeyChecking=no' ,'-oConnectTimeout=20', '-oServerAliveCountMax=120', '-oServerAliveInterval=1', '-oControlPath=/tmp/%r@%h:%p', '-oControlMaster=auto', '-oControlPersist=yes', '-p', '22' ]

import subprocess
import os

import satellites

for node in satellites.satellites:
    socketfile = '/tmp/'  + node + ':22'
    try:
        os.stat(socketfile)
        print(node, "ok")
    except:
        print(node, "ng")
        sshcmd.append(node)
        sshcmd.append('exit')
        sshcmd.append('0')
        subprocess.run(sshcmd)


