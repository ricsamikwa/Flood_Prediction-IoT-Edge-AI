# Flood Prediction Using IoT and Artificial Neural Networks with Edge Computing

Contributor(s): Eric Samikwa

## Dependencies :
+ python 3
+ tensorflow 
+ bluepy

Once running:
+ See https://thingspeak.com/channels/990314 
(for real-time rainfall and water level sensor readings and predicted flood alert status)
+ See generated flood eary warning messages on twitter: @EdgeFloodPredi1

+ Devices:
+ Raspberry
+ Arduino nano 33 BLE(s)
+ Water level sensor(s)
+ Octopus Rain sensor
+ 
+ Alternatively:
To use thunderboard sense 2 *(with external sensors): replace line "from IoT_sensing.ble_scanner import *" with "from IoT_sensing.tbsense_scan import *" in main.py

Paper: https://ieeexplore.ieee.org/abstract/document/9291641

### Citation

Please cite the paper as follows: Samikwa, Eric, Thiemo Voigt, and Joakim Eriksson. "Flood Prediction Using IoT and Artificial Neural Networks with Edge Computing." 2020 International Conferences on Internet of Things (iThings) and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData) and IEEE Congress on Cybermatics (Cybermatics). IEEE, 2020. 
```
@inproceedings{samikwa2020flood,
  title={Flood Prediction Using IoT and Artificial Neural Networks with Edge Computing},
  author={Samikwa, Eric and Voigt, Thiemo and Eriksson, Joakim},
  booktitle={2020 International Conferences on Internet of Things (iThings) and IEEE Green Computing and Communications (GreenCom) and IEEE Cyber, Physical and Social Computing (CPSCom) and IEEE Smart Data (SmartData) and IEEE Congress on Cybermatics (Cybermatics)},
  pages={234--240},
  year={2020},
  organization={IEEE}
}
```
