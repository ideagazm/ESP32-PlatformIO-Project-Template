/**
 * Example ESP32 PlatformIO Project
 * 
 * This is a simple example to demonstrate the build system.
 * Replace this file with your own main.cpp or main.ino
 */

#include <Arduino.h>

// Define LED pin (GPIO 2 is commonly used for built-in LED on ESP32)
#define LED_PIN 2

void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    
    // Initialize LED pin
    pinMode(LED_PIN, OUTPUT);
    
    Serial.println("ESP32 PlatformIO Project Template");
    Serial.println("Replace src/main.example.cpp with your own code!");
}

void loop() {
    // Blink the LED
    digitalWrite(LED_PIN, HIGH);
    delay(1000);
    digitalWrite(LED_PIN, LOW);
    delay(1000);
    
    Serial.println("Hello from ESP32!");
}