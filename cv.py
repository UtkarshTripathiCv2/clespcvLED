import cv2
import requests
import time
from ultralytics import YOLO

# Load model
model = YOLO('best.pt')

# ESP32 IP
esp32_ip = "http://192..fbfbss4"

# Camera
cap = cv2.VideoCapture(0)

print("Starting Detection...")

# Cooldown system
last_trigger_time = 0
cooldown = 2  # seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    drone_detected = False

    # Run detection with confidence threshold
    results = model(frame, conf=0.6)

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]

            if label == 'drone':
                drone_detected = True

        annotated_frame = r.plot()

    # Cooldown logic
    current_time = time.time()

    if drone_detected and (current_time - last_trigger_time > cooldown):
        try:
            requests.get(f"{esp32_ip}/drone_detected", timeout=0.1)
            print("🚁 Drone detected! Signal sent.")
            last_trigger_time = current_time
        except requests.exceptions.RequestException:
            pass

    # Display alert text
    if drone_detected:
        cv2.putText(annotated_frame, "DRONE DETECTED!", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Show live feed
    cv2.imshow("YOLOv8 Drone Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
