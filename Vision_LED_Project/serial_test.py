
import serial
import time

PORT = "COM7"  # Change this to your Arduino's actual COM port
BAUD_RATE = 9600

arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow the Arduino to restart

print("Connected to Arduino!")

try:
    while True:
        pattern = input(
            "Enter five bits (e.g. 10000, 01000, 11111) or q to quit: "
        ).strip()

        if pattern.lower() == "q":
            break

        if len(pattern) != 5 or any(bit not in "01" for bit in pattern):
            print("Enter exactly five 0s or 1s.")
            continue

        arduino.write(pattern.encode("ascii"))
        print("Sent:", pattern)

finally:
    arduino.close()
    print("Serial connection closed.")
