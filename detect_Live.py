import time
import winsound

import cv2
import folium
import geocoder
import torch

# =========================
# LOAD YOLOv5 MODEL
# =========================
model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="D:/road-defect-detection-yolov5-main/runs/train/exp2/weights/best.pt"
)

# Lower confidence for better detection
model.conf = 0.10

# =========================
# START CAMERA
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

# =========================
# VARIABLES
# =========================
last_alert_time = 0
last_saved_time = 0
locations = []


# =========================
# GPS FUNCTION
# =========================
def get_location():
    try:
        g = geocoder.ip("me")
        if g.latlng is None:
            return [17.3850, 78.4867]  # fallback
        return g.latlng
    except:
        return [17.3850, 78.4867]


# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not working ❌")
        break

    # Resize for speed
    frame = cv2.resize(frame, (640, 480))

    # Run detection
    results = model(frame)

    # Convert for OpenCV
    annotated_frame = results.render()[0].copy()

    detected = False

    # =========================
    # DETECTION LOOP
    # =========================
    for *box, conf, cls in results.xyxy[0]:
        label = model.names[int(cls)]

        print("DEBUG:", label, float(conf))

        if conf > 0.10:
            detected = True
            print("✅ Detected:", label, "Confidence:", float(conf))

    # =========================
    # ALERT + MAP
    # =========================
    if detected:
        current_time = time.time()

        # 🔊 Alert sound
        if current_time - last_alert_time > 3:
            print("🚨 POTHOLE DETECTED!")
            winsound.Beep(1000, 500)
            last_alert_time = current_time

        # 📍 Save location
        if current_time - last_saved_time > 10:
            lat, lon = get_location()
            print("📍 Location:", lat, lon)

            locations.append((lat, lon))

            # Create map
            m = folium.Map(location=[lat, lon], zoom_start=15)

            for loc in locations:
                folium.Marker(loc, popup="Pothole").add_to(m)

            m.save("pothole_map.html")
            print("🗺 Map updated!")

            last_saved_time = current_time

    # =========================
    # DISPLAY
    # =========================
    cv2.putText(annotated_frame, "AI Pothole Detection", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Pothole Detection", annotated_frame)

    # Exit key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# =========================
# CLEANUP
# =========================
cap.release()
cv2.destroyAllWindows()
