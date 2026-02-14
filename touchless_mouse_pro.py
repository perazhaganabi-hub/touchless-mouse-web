import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
smoothening = 7
click_delay = 0.3
last_click_time = 0
dragging = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Landmark positions
            index_x = int(hand_landmarks.landmark[8].x * w)
            index_y = int(hand_landmarks.landmark[8].y * h)

            middle_x = int(hand_landmarks.landmark[12].x * w)
            middle_y = int(hand_landmarks.landmark[12].y * h)

            thumb_x = int(hand_landmarks.landmark[4].x * w)
            thumb_y = int(hand_landmarks.landmark[4].y * h)

            # Convert to screen
            screen_x = np.interp(index_x, (100, w-100), (0, screen_width))
            screen_y = np.interp(index_y, (100, h-100), (0, screen_height))

            # Smooth movement
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Distances
            dist_thumb = math.hypot(thumb_x - index_x, thumb_y - index_y)
            dist_middle = math.hypot(middle_x - index_x, middle_y - index_y)

            current_time = time.time()

            # LEFT CLICK
            if dist_thumb < 30 and current_time - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = current_time
                cv2.putText(frame, "LEFT CLICK", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # RIGHT CLICK
            if dist_middle < 30 and current_time - last_click_time > click_delay:
                pyautogui.rightClick()
                last_click_time = current_time
                cv2.putText(frame, "RIGHT CLICK", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # DRAG MODE (Index + Middle close)
            if dist_middle < 25:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
                    cv2.putText(frame, "DRAGGING", (20,130),
                                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # SCROLL (Index up/down movement)
            if index_y < 100:
                pyautogui.scroll(20)
            elif index_y > h-100:
                pyautogui.scroll(-20)

    cv2.imshow("Touchless Mouse PRO", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
