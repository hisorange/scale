class Interface:
  def __init__(self, name, ip, netmask, gateway, broadcast):
      self.name = name
      self.ip = ip
      self.netmask = netmask
      self.gateway = gateway
      self.broadcast = broadcast

  def __str__(self):
      return "name: " + self.name + "\nip: " + self.ip + "\nnetmask: " + self.netmask + "\ngateway: " + self.gateway + "\nbroadcast: " + self.broadcast
