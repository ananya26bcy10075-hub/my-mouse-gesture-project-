import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Get your physical monitor screen resolution
screen_width, screen_height = pyautogui.size()

# Disable PyAutoGUI's fail-safe to prevent accidental crashes at corner boundaries
pyautogui.FAILSAFE = False

# Start capturing video from the default webcam
cap = cv2.VideoCapture(0)

# Smoothness variables to prevent mouse jittering
prev_x, prev_y = 0, 0
smoothing = 5 

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally so it acts like a mirror
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # MediaPipe requires RGB images, but OpenCV reads in BGR
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand skeletal structure on the screen overlay
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract coordinates for Index Finger Tip (ID 8) and Thumb Tip (ID 4)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Convert normalized coordinates (0.0 to 1.0) to screen pixel coordinates
            ix, iy = int(index_tip.x * w), int(index_tip.y * h)
            tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Map the finger positions from the camera frame size to full screen resolution
            target_x = int(index_tip.x * screen_width)
            target_y = int(index_tip.y * screen_height)

            # Apply a linear interpolation smoothing algorithm to reduce hand shaking
            curr_x = prev_x + (target_x - prev_x) / smoothing
            curr_y = prev_y + (target_y - prev_y) / smoothing
            
            # Move the actual OS mouse cursor
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Calculate the Euclidean distance between Thumb tip and Index tip
            distance = math.hypot(tx - ix, ty - iy)

            # If the distance is less than 30 pixels, register it as a click
            if distance < 30:
                cv2.circle(frame, (ix, iy), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                pyautogui.delay(0.2) # Short delay to prevent accidental double-clicks

    # Display the live feedback camera window
    cv2.imshow("Gesture Controller (Press 'q' to Quit)", frame)

    # Break loop safely when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
