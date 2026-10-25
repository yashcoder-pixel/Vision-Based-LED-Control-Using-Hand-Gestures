
import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Webcam could not be opened.")
    raise SystemExit(1)

print("Webcam connected. Press Q to exit.")

while True:
    success, frame = camera.read()

    if not success:
        print("ERROR: Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    cv2.imshow("OpenCV Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

