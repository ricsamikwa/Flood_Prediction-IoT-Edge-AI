#include <ArduinoBLE.h>

BLEService ledService("19B10000-E8F2-537E-4F6C-D104768A1214"); // BLE LED Service

// create characteristics and allow remote device to read and write  
BLEByteCharacteristic rainfallCharacteristic("19B10011-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite);

BLEByteCharacteristic waterLevelCharacteristic("2713", BLERead | BLEWrite );

const int ledPin = LED_BUILTIN; // pin to use for the LED

//parameters for water level sensor
int trigger_pin = 2;
int echo_pin = 3;
int time_taken;
int distance;

//custom functions for pulseIn, the ble module does not currently support pulseIn

// function prototype to define default timeout value
static unsigned int newPulseIn(const byte pin, const byte state, const unsigned long timeout = 1000000L);

// using a macro to avoid function call overhead
#define WAIT_FOR_PIN_STATE(state) \
  while (digitalRead(pin) != (state)) { \
    if (micros() - timestamp > timeout) { \
      return 0; \
    } \
  }

static unsigned int newPulseIn(const byte pin, const byte state, const unsigned long timeout) {
  unsigned long timestamp = micros();
  WAIT_FOR_PIN_STATE(!state);
  WAIT_FOR_PIN_STATE(state);
  timestamp = micros();
  WAIT_FOR_PIN_STATE(!state);
  return micros() - timestamp;
}



void setup() {
  Serial.begin(57600);
  while (!Serial);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("Nano BLE 01");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(rainfallCharacteristic);
  ledService.addCharacteristic(waterLevelCharacteristic);


  // add service
  BLE.addService(ledService);

  // set the initial value for the characeristics:
  waterLevelCharacteristic.writeValue(0.0);
  rainfallCharacteristic.writeValue(0);  

  // start advertising
  BLE.advertise();

  Serial.println("BLE LED Peripheral");

  //water level sensor
  pinMode(trigger_pin, OUTPUT); 
  pinMode(echo_pin, INPUT);
}

void loop() {
  // poll for BLE events  
  BLE.poll();

  //getting sensor data
  float rainsensor_value = ((analogRead(0))/950.0)*110;

  int rainfall = (int) rainsensor_value;
  
  Serial.print("Rain Amount:");  
  Serial.println(rainfall);
  digitalWrite(trigger_pin, HIGH);

  delayMicroseconds(10);

  digitalWrite(trigger_pin, LOW);

  time_taken = newPulseIn(echo_pin, HIGH);
  
  float level = (((time_taken * 0.034) / 2)/340) * 100;

  int water_level = (int) level;
  Serial.print("");  
  Serial.print("Water Level:");  
  Serial.println(water_level);

  //writing values to BLE channel
  waterLevelCharacteristic.writeValue(water_level);
  rainfallCharacteristic.writeValue(rainfall);  
  delay(200); 
}
