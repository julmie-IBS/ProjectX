#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

 Adafruit_MPU6050 mpu;
// Set WiFi credentials
#define WIFI_SSID "xxx"
#define WIFI_PASS "julian12345"
#define UDP_PORT 4210

// UDP
WiFiUDP UDP;
char packet[255];
char reply[] = "Packet received!";
 
void setup() {
    if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }


    
  }

  
  // Setup serial port
  Serial.begin(115200);
  Serial.println();
 
  // Begin WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
 
  // Connecting to WiFi...
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  // Loop continuously while WiFi is not connected
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
 
  // Connected to WiFi
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  // Begin listening to UDP port
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
 
}

void loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Serial.print(a.acceleration.x);
    Serial.print(",");
    Serial.print(a.acceleration.y);
    Serial.print(",");
    Serial.print(a.acceleration.z);
    Serial.print(",");
    ////////////////////////////////#####################//////////////////////////////////
    Serial.print(g.gyro.x);
    Serial.print(",");
    Serial.print(g.gyro.y);
    Serial.print(",");
    Serial.println(g.gyro.z);



  
    
    String Value_String=String(a.acceleration.x) +","+String(a.acceleration.y) +","+String(a.acceleration.z)+","+ String(g.gyro.x)+","+ String(g.gyro.y)+","+ String(g.gyro.z);
    
    
    // Send return packet
    Serial.println("Packet sent ");
    UDP.beginPacket("192.168.0.100", 19945);
    UDP.print(Value_String);
    UDP.endPacket();
    delay(100);
  

}
