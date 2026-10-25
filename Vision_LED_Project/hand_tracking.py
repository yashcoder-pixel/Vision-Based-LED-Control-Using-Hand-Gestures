
import cv2
import mediapipe as mp
import time

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

connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Cannot open webcam.")
    raise SystemExit(1)

try:
    with HandLandmarker.create_from_options(options) as landmarker:
        start_time = time.monotonic()
        previous_timestamp = -1

        while True:
            success, frame = camera.read()

            if not success:
                print("ERROR: Cannot read webcam.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            timestamp = int(
                (time.monotonic() - start_time) * 1000
            )
            timestamp = max(timestamp, previous_timestamp + 1)
            previous_timestamp = timestamp

            result = landmarker.detect_for_video(image, timestamp)

            if result.hand_landmarks:
                hand = result.hand_landmarks[0]

                points = [
                    (int(lm.x * frame.shape[1]),
                     int(lm.y * frame.shape[0]))
                    for lm in hand
                ]

                for x, y in points:
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                for a, b in connections:
                    cv2.line(
                        frame, points[a], points[b],
                        (255, 0, 0), 2
                    )

                # Fingertip is above the joint = finger raised
                thumb = points[4][0] < points[3][0]
                index = points[8][1] < points[6][1]
                middle = points[12][1] < points[10][1]
                ring = points[16][1] < points[14][1]
                little = points[20][1] < points[18][1]

                fingers = [
                    ("Thumb", thumb),
                    ("Index", index),
                    ("Middle", middle),
                    ("Ring", ring),
                    ("Little", little)
                ]

                for i, (name, is_up) in enumerate(fingers):
                    state = "UP" if is_up else "DOWN"
                    color = (0, 255, 0) if is_up else (0, 0, 255)

                    cv2.putText(
                        frame,
                        f"{name}: {state}",
                        (20, 80 + i * 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

                # Show the detected finger pattern
                pattern = "".join(
                    "1" if state else "0"
                    for _, state in fingers
                )

                cv2.putText(
                    frame,
                    f"Pattern: {pattern}",
                    (20, frame.shape[0] - 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 0),
                    2
                )

            else:
                cv2.putText(
                    frame, "NO HAND DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2
                )

            cv2.imshow("Five-Finger Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    camera.release()
    cv2.destroyAllWindows()
