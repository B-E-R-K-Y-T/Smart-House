class Sensor:
    def __init__(self, ip_address, mac_address, pin_id=None):
        self.ip_address, self.mac_address, self.pin_id = ip_address, mac_address, pin_id

    def get_ip_address(self):
        return self.ip_address

    def get_mac_address(self):
        return self.mac_address

    def get_pin_id(self):
        return self.pin_id
