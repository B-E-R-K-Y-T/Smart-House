# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

import json

from config import PATH_TO_CONF_SNR


class ConfigReader:
    def __init__(self):
        pass

    def get_characteristic(self, key: str):
        with open(file=PATH_TO_CONF_SNR, mode='r') as json_file:
            data = json.load(json_file)
            return data[key]


if __name__ == '__main__':
    par = ConfigReader()

    print(par.get_characteristic('address'))
