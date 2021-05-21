# IoT-Edge-AI Flood Early Warning System

Author: Eric Samikwa
Dependencies :
+ python 3
+ tensorflow 
+ bluepy

Once running:
+ See https://thingspeak.com/channels/990314 
(for real-time rainfall and water level sensor readings and predicted flood alert status)
+ See generated flood eary warning messages on twitter: @EdgeFloodPredi1

+ Devices:
+ Raspberry 3B+
+ Arduino nano 33 BLE(s)
+ Water level sensor(s)
+ Octopus Rain sensor (Rainfall)
+ 
+ Alternatively:
To use thunderboard sense 2 *(with external sensors): replace line "from IoT_sensing.ble_scanner import *" with "from IoT_sensing.tbsense_scan import *" in main.py

