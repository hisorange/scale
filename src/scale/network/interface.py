class Interface:
    def __init__(self, name, ip, netmask, gateway, broadcast):
        self.name: str = name
        self.ip: str = ip
        self.netmask: str = netmask
        self.gateway: str = gateway
        self.broadcast: str = broadcast

    def __str__(self):
        return "name: " + self.name + "\nip: " + self.ip + "\nnetmask: " + self.netmask + "\ngateway: " + self.gateway + "\nbroadcast: " + self.broadcast

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "ip": self.ip,
            "netmask": self.netmask,
            "gateway": self.gateway,
            "broadcast": self.broadcast
        }

    def from_dict(d: dict):
        return Interface(d["name"], d["ip"], d["netmask"], d["gateway"], d["broadcast"])
