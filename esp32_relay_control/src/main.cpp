#include <Arduino.h>

// Define relay pins based on your wiring
const int RELAY_RIGHT = 25; // Connected to IN1 and IN2
const int RELAY_LEFT = 26;  // Connected to IN3 and IN4

// --- SAFETY TIMEOUT (DEADMAN SWITCH) ---
// Because your ESP32 is powered via VIN, unplugging the USB cable does NOT turn it off.
// If you unplug the USB while it's moving, it will keep moving forever!
// This stops the motor if no new command is received for 3 seconds.
// (To keep it spinning forever, change this to 0, but be careful!)
unsigned long autoStopTimeout = 1000; 
unsigned long lastCommandTime = 0;
bool isMoving = false;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);

  // CRITICAL STEP FOR ACTIVE-LOW RELAYS:
  // Write HIGH to the pins *before* setting them as outputs.
  // This prevents the relays from momentarily clicking ON when the ESP32 boots.
  digitalWrite(RELAY_RIGHT, HIGH); 
  digitalWrite(RELAY_LEFT, HIGH);

  // Configure relay pins as outputs
  pinMode(RELAY_RIGHT, OUTPUT);
  pinMode(RELAY_LEFT, OUTPUT);

  // Default state: STOP (Both relays OFF). 
  // Remember: HIGH = OFF, LOW = ON.
  digitalWrite(RELAY_RIGHT, HIGH);
  digitalWrite(RELAY_LEFT, HIGH);

  // Print menu to the Serial Monitor
  Serial.println("\n==========================================");
  Serial.println("--- ESP32 Antenna Motor Control Ready ---");
  Serial.println("[SAFETY] Serial connected. Motors forced to STOP.");
  Serial.println("==========================================");
  Serial.println("Hardware logic: ACTIVE-LOW");
  Serial.println("Send 'L' or 'l' for LEFT.");
  Serial.println("Send 'R' or 'r' for RIGHT.");
  Serial.println("Send 'S' or 's' for STOP.");
}

void loop() {
  // Check if data is available in the Serial buffer
  if (Serial.available() > 0) {
    char command = Serial.read();
    lastCommandTime = millis(); // Reset the safety timer whenever we get a command

    switch (command) {
      // --- LEFT COMMAND ---
      case 'L':
      case 'l':
        Serial.println("Action: LEFT (Pin 26 LOW/ON, Pin 25 HIGH/OFF)");
        digitalWrite(RELAY_RIGHT, HIGH); // Turn Right OFF
        digitalWrite(RELAY_LEFT, LOW);   // Turn Left ON
        isMoving = true;
        break;

      // --- RIGHT COMMAND ---
      case 'R':
      case 'r':
        Serial.println("Action: RIGHT (Pin 25 LOW/ON, Pin 26 HIGH/OFF)");
        digitalWrite(RELAY_LEFT, HIGH);  // Turn Left OFF
        digitalWrite(RELAY_RIGHT, LOW);  // Turn Right ON
        isMoving = true;
        break;

      // --- STOP COMMAND ---
      case 'S':
      case 's':
        Serial.println("Action: STOP (Both Relays HIGH/OFF)");
        digitalWrite(RELAY_LEFT, HIGH);  // Turn Left OFF
        digitalWrite(RELAY_RIGHT, HIGH); // Turn Right OFF
        isMoving = false;
        break;

      // --- IGNORE LINE ENDINGS ---
      case '\n':
      case '\r':
        break;

      // --- UNKNOWN COMMAND ---
      default:
        Serial.println("Unknown command. Please send L, R, or S.");
        break;
    }
  }

  // --- SAFETY AUTO-STOP LOGIC ---
  // If we are currently moving, AND the timeout feature is enabled (> 0),
  // stop the motors if it's been longer than 'autoStopTimeout' since the last command.
  if (isMoving && autoStopTimeout > 0) {
    if (millis() - lastCommandTime > autoStopTimeout) {
      Serial.println("\n[SAFETY] Connection lost or timeout reached. Auto-Stopping!");
      digitalWrite(RELAY_LEFT, HIGH);  // Turn Left OFF
      digitalWrite(RELAY_RIGHT, HIGH); // Turn Right OFF
      isMoving = false;
    }
  }
}
