import bluepy.btle as btle

p = btle.Peripheral("f9:93:a1:9a:df:af")
services=p.getServices()
s = p.getServiceByUUID(list(services)[2].uuid)
c = s.getCharacteristics()[0]
value = c.read(bytes("0001")
print("The value "+value)
# p.disconnect()
