
import cv2
import mediapipe as mp
import serial
import time

# Change COM7 if your Arduino uses a different port
PORT = "COM7"
BAUD_RATE = 9600

# MediaPipe hand tracking setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)

arduino = None
camera = None

try:
    # Connect to Arduino
    arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Arduino connected.")

    # Open webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError(
            "Camera could not open. Close other apps using the webcam."
        )

    print("Camera opened. Press Q to quit.")

    with HandLandmarker.create_from_options(options) as tracker:
        last_pattern = ""

        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read camera frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp = int(time.monotonic() * 1000)
            result = tracker.detect_for_video(mp_image, timestamp)

            pattern = "00000"

            if result.hand_landmarks:
                hand = result.hand_landmarks[0]

                points = [
                    (int(p.x * frame.shape[1]),
                     int(p.y * frame.shape[0]))
                    for p in hand
                ]

                # Draw detected hand landmarks
                for p in points:
                    cv2.circle(frame, p, 4, (0, 255, 0), -1)

                # Basic finger-up detection
                thumb = points[4][0] < points[3][0]
                index = points[8][1] < points[6][1]
                middle = points[12][1] < points[10][1]
                ring = points[16][1] < points[14][1]
                little = points[20][1] < points[18][1]

                states = [
                    thumb, index, middle, ring, little
                ]

                pattern = "".join(
                    "1" if state else "0"
                    for state in states
                )

                # Draw connections between landmarks
                connections = (
                    mp.tasks.vision.HandLandmarksConnections
                    if hasattr(
                        mp.tasks.vision,
                        "HandLandmarksConnections"
                    )
                    else None
                )

                if connections:
                    for connection in connections.HAND_CONNECTIONS:
                        start = points[connection.start]
                        end = points[connection.end]
                        cv2.line(
                            frame, start, end,
                            (255, 0, 0), 2
                        )

                cv2.putText(
                    frame, "HAND DETECTED",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2
                )

            else:
                cv2.putText(
                    frame, "NO HAND DETECTED",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 255), 2
                )

            # Send only when the finger pattern changes
            if pattern != last_pattern:
                arduino.write(pattern.encode("ascii"))
                last_pattern = pattern
                print("LED pattern:", pattern)

            cv2.putText(
                frame, "Thumb Index Middle Ring Little",
                (10, frame.shape[0] - 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 1
            )

            cv2.putText(
                frame, pattern,
                (20, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2
            )

            cv2.imshow("Vision LED Controller", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except Exception as error:
    print("Error:", error)

finally:
    if camera is not None:
        camera.release()

    cv2.destroyAllWindows()

    if arduino is not None and arduino.is_open:
        try:
            arduino.write(b"00000")
        finally:
            arduino.close()

    print("Program closed.")
