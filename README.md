# Vision-Based LED Control Using Hand Gestures

A computer vision and embedded systems project that uses real-time hand gesture recognition to control physical LEDs connected to an Arduino UNO.

## Project Overview

This project combines Python-based computer vision with Arduino hardware. A webcam captures hand movements, MediaPipe detects hand landmarks, and Python determines which fingers are raised. The resulting five-bit pattern is transmitted to an Arduino UNO over serial communication to control five LEDs independently.

## System Architecture

Webcam → OpenCV → MediaPipe Hand Tracking → Finger Detection Logic → Serial Communication → Arduino UNO → LEDs

## Features

- Real-time hand tracking using a webcam
- Detection of 21 hand landmarks using MediaPipe
- Recognition of raised and lowered fingers
- Five-bit gesture representation
- Serial communication between Python and Arduino
- Independent control of five physical LEDs

## Hardware Requirements

- Arduino UNO R3
- Five LEDs
- Five 220Ω or 330Ω current-limiting resistors
- Breadboard and jumper wires
- USB cable
- Computer with a webcam

## Software Requirements

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino IDE

## Project Structure

```text
Vision-Based-LED-Control-Using-Hand-Gestures/
└── Vision_LED_Project/
    ├── camera_test.py
    ├── hand_landmarker.task
    ├── hand_tracking.py
    ├── serial_test.py
    └── vision_led_control.py
```

## LED Pin Mapping

| Finger | Arduino Pin |
|---|---|
| Thumb | D3 |
| Index | D4 |
| Middle | D5 |
| Ring | D6 |
| Little | D7 |

Each LED must have its own current-limiting resistor.

## Gesture Representation

Each finger is represented by one binary digit.

| Gesture | Pattern |
|---|---|
| Open palm | `11111` |
| Closed fist | `00000` |
| Index finger only | `01000` |

A `1` represents a raised finger, while a `0` represents a lowered finger. The bit order is Thumb, Index, Middle, Ring, Little.

## How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe identifies 21 landmarks on the detected hand.
3. Python evaluates the finger positions to determine which fingers are raised.
4. The application converts the result into a five-bit pattern.
5. PySerial sends the pattern to the Arduino UNO over USB serial communication.
6. The Arduino processes the received pattern and switches the corresponding LEDs ON or OFF.

## Setup

1. Install Python and the required libraries:

   ```bash
   pip install opencv-python mediapipe pyserial
   ```

2. Open the Arduino sketch in Arduino IDE and upload it to the UNO. The sketch must implement the serial protocol used by `vision_led_control.py`.

3. Connect the five LEDs to digital pins D3–D7 through individual resistors, with their cathodes connected to GND.

4. Connect the Arduino to the computer using USB.

5. Check the Arduino's COM port and update the `PORT` setting in `vision_led_control.py` if necessary.

6. Run the integrated application:

   ```bash
   python vision_led_control.py
   ```

## Learning Outcomes

- Computer vision fundamentals
- Hand landmark detection
- Python application development
- Serial communication using PySerial
- Arduino digital I/O control
- Integration of software and embedded hardware

## Future Improvements

- Gesture-based control of additional devices
- Improved finger detection under different lighting conditions
- A graphical interface for monitoring gestures
- Extension to ESP32-based wireless control

---

**Technologies:** Python · OpenCV · MediaPipe · PySerial · Arduino UNO · Embedded Systems
