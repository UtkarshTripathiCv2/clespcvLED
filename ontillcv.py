import cv2
import requests
from ultralytics import YOLO

model = YOLO('best.pt')
esp32_ip = "http://192.168.84.24"

cap = cv2.VideoCapture(0)

print("Starting Detection...")

last_state = False  # Track previous state

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    drone_detected = False

    results = model(frame, conf=0.6)

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            if model.names[class_id] == 'drone':
                drone_detected = True

        annotated_frame = r.plot()

    # 🔥 STATE CHANGE LOGIC
    try:
        if drone_detected and not last_state:
            requests.get(f"{esp32_ip}/drone_on", timeout=1)
            print("🟢 Drone detected → LED ON")

        elif not drone_detected and last_state:
            requests.get(f"{esp32_ip}/drone_off", timeout=1)
            print("🔴 Drone lost → LED OFF")

    except Exception as e:
        print("ERROR:", e)

    last_state = drone_detected

    # Display
    if drone_detected:
        cv2.putText(annotated_frame, "DRONE DETECTED!", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("YOLOv8 Drone Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
