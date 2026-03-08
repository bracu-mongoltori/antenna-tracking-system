# Run this script to generate the README.md file with all the raw markdown content.
cat << 'EOF' > README.md
# ESP32 Antenna Azimuth Motor Controller 📡

This is a complete PlatformIO project designed to control the **azimuth motor** of an antenna tracking system. It uses an ESP32 DevKit V1 and an Active-LOW mechanical relay module to rotate your antenna left or right. You simply send text commands over the Serial Monitor to control the movement.

It includes a **Safety Timeout (Deadman Switch)** feature that automatically stops the motor if the serial connection drops or no commands are received, preventing your antenna from rotating endlessly if the USB is unplugged.

## 🛠️ Hardware Setup

Because we are using an Active-LOW relay module, the wiring needs to be specific to prevent backfeeding or unexpected relay triggering on boot.

* **Microcontroller:** ESP32 DevKit V1

* **Relays:** 4-Channel Active-LOW mechanical relay board.

* **Power:** External 5V power supply powering both the ESP32 (via `VIN`) and the relays.

**Wiring Connections:**

* `External 5V+` -> Connect to `ESP32 VIN` **AND** `Relay VCC / JD-VCC`.

* `External 5V GND` -> Connect to `ESP32 GND` **AND** `Relay GND` (All grounds must be shared).

* `ESP32 GPIO 25` -> Bridged to `IN1` and `IN2` (Controls Right movement).

* `ESP32 GPIO 26` -> Bridged to `IN3` and `IN4` (Controls Left movement).

## 🚀 Getting Started (PlatformIO)

Run these commands in your terminal to create the project, navigate into it, format the ESP32, and compile/upload your code.

**1. Create the project directory and navigate into it:**

```
mkdir esp32_relay_control
cd esp32_relay_control
```

**2. Initialize the PlatformIO project for ESP32 DevKit V1:**

```
pio project init --board esp32doit-devkit-v1
```

**3. Format (Erase Flash) the ESP32:**
*(Make sure your ESP32 is plugged via USB before running this)*

```
pio run --target erase
```

**4. Upload the code and open the Serial Monitor:**
*(Run this after saving the `platformio.ini` and `main.cpp` files below)*

```
pio run --target upload --target monitor
```

*(Note: If you ever get an `invalid header: 0xffffffff` boot loop error after erasing, press `Ctrl+C`, run `pio run -t clean`, and then run the upload command again while holding the **BOOT** button on the ESP32).*

## ⚙️ Configuration (`platformio.ini`)

Replace the contents of your `platformio.ini` file with this:

```
[env:esp32doit-devkit-v1]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino

; Set the serial monitor baud rate to match our code
monitor_speed = 115200
```

## 💻 Source Code (`src/main.cpp`)

Create a file named `main.cpp` inside the `src` folder and paste the following code:

```
#include <Arduino.h>

// Define relay pins based on your wiring
const int RELAY_RIGHT = 25; // Connected to IN1 and IN2
const int RELAY_LEFT = 26;  // Connected to IN3 and IN4

// --- SAFETY TIMEOUT (DEADMAN SWITCH) ---
// Because your ESP32 is powered via VIN, unplugging the USB cable does NOT turn it off.
// If you unplug the USB while it's moving, it will keep moving forever!
// This stops the motor if no new command is received for 3 seconds.
// (To keep it spinning forever, change this to 0, but be careful!)
unsigned long autoStopTimeout = 3000; 
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
```

## 🎮 How to Control the Antenna

Once the Serial Monitor is open (make sure it's running at `115200` baud), type one of these letters and hit Enter to move the azimuth motor:

* **`L`** or **`l`**: Turns **Left** relays ON (Pin 26 LOW).

* **`R`** or **`r`**: Turns **Right** relays ON (Pin 25 LOW).

* **`S`** or **`s`**: **Stop**! Turns all relays OFF (Pins 25 & 26 HIGH).

### Safety Features

* **Auto-Stop on Connect:** Plugging in the serial monitor resets the ESP32 and immediately halts all motor movement.

* **Auto-Stop Timeout:** If the antenna is moving and no new serial commands are received for **3 seconds**, the system automatically stops the motors. This protects your hardware if the tracking software crashes or the USB is disconnected!
EOF
