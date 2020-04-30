from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif dev.addr == "f9:93:a1:9a:df:af":
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

while True:
    for dev in devices:
        if dev.addr == "f9:93:a1:9a:df:af":
            print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print("  %s = %s" % (desc, value))
        else:
            print("BLE device not on our list!")
            




