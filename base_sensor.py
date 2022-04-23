# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

class Sensor:
    def __init__(self, address, mac_address):
        self.ip_address = '127.0.0.1' if address == 'localhost' else address
        self.mac_address = mac_address

    def get_ip_address(self):
        return self.ip_address

    def get_mac_address(self):
        return self.mac_address

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def set_mac_address(self, mac_address):
        self.mac_address = mac_address
