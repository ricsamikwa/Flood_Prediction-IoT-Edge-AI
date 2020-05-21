from bluepy.btle import Scanner, DefaultDelegate
import bluepy.btle as btle
from time import sleep

#thingspeak
# importing the requests library 
import requests   
# api-endpoint api_key
ThingSpeak_URL = "https://api.thingspeak.com/update"
ThingSpeak_API_KEY = "730IO8XA7B1UH9VV"
ThingTweet_URL = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update"
ThingTweet_API_KEY = "RJAWEKE6OTV47N21"


def getArduinoNanoBLEBoards():
    nanoBLE = []
    scanner = Scanner(0)
    devices = scanner.scan(3)
    for dev in devices:
        scanData = dev.getScanData()
        for (adtype, desc, value) in scanData:
            if desc == 'Complete Local Name':
                if 'Nano BLE' in value:
                    print("####  %s = %s" % (desc, value))
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
 
        p = btle.Peripheral(nanoBle.addr)
        services=p.getServices()
        s = p.getServiceByUUID(list(services)[2].uuid)
        # c = s.getCharacteristics()[0]
        # rainfall = c.read()
        rainfall_characteristic = s.getCharacteristics()[0]
        water_level_characteristic = s.getCharacteristics()[1]
        rainfall = rainfall_characteristic.read()
        water = water_level_characteristic.read()
        p.disconnect()
        rainfall_amount = int.from_bytes(rainfall,byteorder='big')
        water_level = int.from_bytes(water,byteorder='big')


        # PARAMS = {'api_key':ThingSpeak_API_KEY,'field1':rainfall_amount}
        # r = requests.get(url = ThingSpeak_URL, params = PARAMS)
        # if  rainfall_amount > 50:
        #     twitter_PARAMS = {'api_key':ThingTweet_API_KEY,'status':"Flood Alert: Move to ANOTHER PLACE..!!"}
        #     r2 = requests.post(url = ThingTweet_URL, params = twitter_PARAMS) 

        
        print("Rainfall Amount: ", rainfall_amount)
        print("")
        print("Water Level :", water_level)
        sleep(4)

if __name__ == '__main__':

    while True:
        nanoBLEs = getArduinoNanoBLEBoards()
        if len(nanoBLEs) == 0:
            print("No arduino nano BLE devices found!")
        else:
            dataLoop(nanoBLEs)

        sleep(5)

