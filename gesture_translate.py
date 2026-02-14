import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture_text = "No Hand Detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            total_fingers = count_fingers(hand_landmarks)

            if total_fingers == 0:
                gesture_text = "FIST - STOP"
            elif total_fingers == 1:
                gesture_text = "ONE"
            elif total_fingers == 2:
                gesture_text = "TWO - PEACE"
            elif total_fingers == 3:
                gesture_text = "THREE"
            elif total_fingers == 4:
                gesture_text = "FOUR"
            elif total_fingers == 5:
                gesture_text = "FIVE - HELLO"

    cv2.putText(img, gesture_text, (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                (0, 255, 0), 3)

    cv2.imshow("Gesture Translator", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
