import utils
import arping
import logging
from fileStorage import fileStorage
import sys


def parseArgs(args):
    import getopt
    parsedArgs = getopt.getopt(args,'i:')
    argsDict = {}
    for i in parsedArgs[0]:
        if(len(i) > 0):
            argsDict[i[0]] = i[1]
    return argsDict

def handleDifferent(fs, mac, ip):
    print('Note: the "{}" machine is now having a new IP address:'.format(mac))
    print('\tOld IP address : {}'.format(fs.getIP(mac)))
    print('\tNew IP address : {}'.format(ip))
    resp = input('Update IP ? (yes/no)').lower()
    if resp == 'yes':
        fs.add(mac, ip)

def getManuf(mac):
    try:
        from manuf import manuf
        parser = manuf.MacParser(manuf_name='manuf/manuf')
        print('\n')
        m = parser.get_all(mac)
        if m.manuf:
            manufacture = '{} {}'.format(
                m.manuf,
                '('+m.comment+')' if m.comment else ''
            )
        else:
            manufacture = '-'
        return manufacture
    except:
        return '-'


def handleMissed(fs, mac, ip):
    manufacture = getManuf(mac)
    print('ATTENTION: a new machine had been detected with the following details')
    print('\tMAC Address : {}'.format(mac))
    print('\tIP Address  : {}'.format(ip))
    print('\tManufacture : {}'.format(manufacture))
    resp = input('Do you confirm that you are arware of this device' +
    ', by confirming that it\'ll be added to the whitelist'+
    ' and you\'ll not be notified about it anymore? (yes/no):')
    resp = resp.lower()
    if resp == 'yes':
        fs.add(mac, ip)
    return resp == 'yes'


def main():
    logging.basicConfig(level=logging.CRITICAL)

    argsDic = parseArgs(sys.argv[1:])
    if '-i' in argsDic and argsDic['-i']:
        iface = argsDic['-i']
    else:
        iface = utils.getDefInterface()
    fs = fileStorage(iface)
    loadingRes = fs.load()
    if(iface != None):
        netInfo = utils.getInterfaceConnectionInfo(iface)
        toArping = netInfo['inet'] + '/' + str(netInfo['nm'])
        print('Pinging....')
        addresses = arping.arping(toArping)
        _match = _different = _missed = _added = _ignored = 0
        if loadingRes:
            for mac,ip in  addresses:
                checkRes = fs.check(mac, ip)
                if checkRes == 'DIFFERENT':
                    handleDifferent(fs, mac, ip)
                    _different += 1
                if checkRes == 'MISSED':
                    added = handleMissed(fs, mac, ip)
                    _missed += 1
                    if added:
                        _added += 1
                    else:
                        _ignored += 1
                if checkRes == 'MATCH':
                    _match += 1
        else:
            print('first time')
            for mac,ip in addresses:
                fs.add(mac,ip)

        print('{} machines detected.'.format(len(addresses)))
        if loadingRes:
            print('\t{} Matched.'.format(_match))
            print('\t{} Missed ({} added, {} ignored).'.format(_missed, _added, _ignored))
            print('\t{} Different IP.'.format( _different))

        fs.dump()
    else:
        logging.error('No up interfase')




if __name__ == '__main__':
    main()
