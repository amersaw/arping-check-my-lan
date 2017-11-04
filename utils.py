import os, pwd
import logging

def getAllInterfaces():
    return os.listdir('/sys/class/net/')


def isInterfaceUp(iface):
    with open('/sys/class/net/' + iface + '/operstate', 'r') as f:
        content = f.read()
        return content == 'up\n'

def getInterfaceConnectionInfo(iface):
    res = {}
    ifconfig = os.popen('ifconfig ' + iface + ' | grep "inet "').read()
    ifconfig = ifconfig.rstrip('\n')
    tmp = [i for i in ifconfig.split(' ') if i != '']
    for i in range(0, len(tmp), 2):
        res[tmp[i]] = tmp[i+1]
    res['nm'] = sum([str(bin(int(t))).count('1') for t in res['netmask'].split('.')])
    return res

def getNetworkAddress(netInfo):
    print(netInfo)
    netmask = netInfo['netmask'].split('.')
    ip = netInfo['inet'].split('.')
    res = []
    for p in range(4):
        res.append(str(int(ip[p]) & int(netmask[p])))
    return str.join('.', res)

def getDefInterface():
    interfaces = getAllInterfaces()
    for iface in interfaces:
        if  iface != 'lo' and isInterfaceUp(iface):
            return iface
    return None


def getCurrentUID():
    try:
        username = os.environ['HOME'].split('/')[-1]
        logging.debug('Current username is : ' + username)
        return pwd.getpwnam(username)[2]
    except Exception as ex:
        logging.error(ex)
        return None

def ownPath(path):
    currentUID = getCurrentUID()
    if currentUID:
        os.chown(path, currentUID, currentUID)
    else:
        logging.error("Couldn't obtain the curren user ID")
