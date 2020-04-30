import bluepy.btle as btle

p = btle.Peripheral("de:fc:54:87:b0:04")
services=p.getServices()
s = p.getServiceByUUID(list(services)[2].uuid)
c = s.getCharacteristics()[0]
c.write(bytes("0001".encode())
p.disconnect()
