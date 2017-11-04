import utils
import os
import json
import logging
class fileStorage:
    def __init__(self, interface):
        self.configDirPath = os.path.expanduser('~/.arping')
        self.machinesFile = os.path.join(self.configDirPath,
            interface+'.json')
        self.machines = {}

    def load(self):
        try:
            if not os.path.exists(self.machinesFile):
                return False
            with open(self.machinesFile, 'r') as f:
                self.machines = json.load(f)
                logging.debug('Loaded machines from machines file')
            return True
        except Exception as ex:
            logging.error(ex)
            return False

    def dump(self):
        if not os.path.exists(self.configDirPath):
            logging.debug('Creating config directory')
            os.makedirs(self.configDirPath)
            logging.debug('Changing confing dir owner/group to the current user')
            utils.ownPath(self.configDirPath)
        with open(self.machinesFile, 'w') as f:
            json.dump(self.machines, f)
            logging.debug('Writing machines to machines file')
        utils.ownPath(self.machinesFile)

    def add(self, mac, ip):
        if mac in self.machines:
            pass
        else:
            pass
        self.machines[mac] = ip

    def getIP(self,mac):
        return self.machines[mac] if mac in self.machines else None

    def reset(self):
        self.machines = {}
        pass

    def check(self, mac, ip):
        if mac in self.machines:
            return "MATCH" if self.machines[mac] == ip else "DIFFERENT"
        else:
            return "MISSED"
