from bluepy.btle import Scanner, DefaultDelegate
from time import sleep

def getArduinoNanoBLEBoards():
    nanoBLE = []
    scanner = Scanner(0)
    devices = scanner.scan(3)
    for dev in devices:
        scanData = dev.getScanData()
        for (adtype, desc, value) in scanData:
            if desc == 'Complete Local Name':
                if 'Nano BLE #' in value:
                    deviceId = int(value.split('#')[-1])
                    nanoBLE.append(dev)

    return nanoBLE

# while True:
#     scanner = Scanner()
#     devices = scanner.scan(10.0)

#     for dev in devices:
#         if dev.addr == "f9:93:a1:9a:df:af":
#             print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
#             for (adtype, desc, value) in dev.getScanData():
#                 print("  %s = %s" % (desc, value))
#             sleep(4)
#         else:
#             print("Discovered device", dev.addr, " unknown!")
#     sleep(10)

def dataLoop(nanoBLEs):
    for nanoBle in nanoBLEs:
        print("Device %s (%s), RSSI=%d dB" % (nanoBle.addr, nanoBle.addrType, nanoBle.rssi))
        # for (adtype, desc, value) in dev.getScanData():
        #             print("  %s = %s" % (desc, value))
        sleep(4)

if __name__ == '__main__':

    while True:
        nanoBLEs = getArduinoNanoBLEBoards()
        if len(nanoBLEs) == 0:
            print("No arduino nano BLE devices found!")
        else:
            dataLoop(nanoBLEs)

        sleep(5)

