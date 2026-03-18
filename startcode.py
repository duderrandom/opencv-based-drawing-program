import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Webcam
cap = cv2.VideoCapture(1)
h_cam, w_cam = 480, 640
cap.set(3, w_cam)
cap.set(4, h_cam)

# Create a blank canvas to draw on
canvas = np.zeros((h_cam, w_cam, 3), np.uint8)

# Coordinates for the previous point (to draw lines)
px, py = 0, 0

while True:
    success, frame = cap.read()
    
    # 1. BRAKE CHECK: If the camera is warming up, skip this loop iteration
    if not success or frame is None:
        print("Camera warming up...")
        continue

    # 2. PRO-TIP: Flip the frame immediately so it feels like a mirror
    frame = cv2.flip(frame, 1)
    
    # 3. CONVERT: This is where it was crashing; now it's safe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # ... (rest of your hand tracking logic)
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Landmark 8 is the Index Finger Tip
            # Landmark 12 is the Middle Finger Tip
            idx_tip = hand_lms.landmark[8]
            mid_tip = hand_lms.landmark[12]
            
            cx, cy = int(idx_tip.x * w_cam), int(idx_tip.y * h_cam)
            m_cx, m_cy = int(mid_tip.x * w_cam), int(mid_tip.y * h_cam)

            # Check if Index finger is UP and Middle finger is DOWN (Drawing Mode)
            # Simple heuristic: If index tip is higher than middle tip
            if idx_tip.y < mid_tip.y:
                cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                
                if px == 0 and py == 0:
                    px, py = cx, cy
                
                # Draw on the canvas
                cv2.line(canvas, (px, py), (cx, cy), (0, 255, 0), 5)
                px, py = cx, cy
            else:
                # Hover/Selection Mode (Reset previous points)
                px, py = 0, 0
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

    # Combine the canvas and the live feed
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Virtual Canvas", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()