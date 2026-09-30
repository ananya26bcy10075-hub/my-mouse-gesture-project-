README / Setup and Usage Guide
A Python project that uses a webcam, MediaPipe hand landmarks, OpenCV, and PyAutoGUI to control the
computer mouse with hand gestures.
Features
• Real-time hand tracking
• Index-finger cursor control
• Thumb-index pinch used as a click
• Cursor smoothing to reduce jitter
• Live webcam feedback
• Press Q to exit
Requirements
Python 3.x
Webcam
pip install opencv-python mediapipe pyautogui
How to Run
1. Save the supplied code as gesture_controller.py.
2. Open a terminal in the project folder.
3. Install the packages shown above.
4. Run: python gesture_controller.py
5. Move the index finger to control the cursor.
6. Bring the thumb and index fingertip together to click.
7. Press q while the camera window is active to stop.
How It Works
MediaPipe returns normalized hand landmarks. Landmark 8 is the index fingertip and landmark 4 is the thumb tip.
The index coordinates are mapped to the monitor resolution. The Euclidean distance between the two fingertips is
then checked; if it is below 30 pixels, pyautogui.click() is called.
Libraries
Library Purpose
OpenCV Webcam capture, frame processing and display
MediaPipe Hand detection and landmark tracking
PyAutoGUI Operating-system mouse movement and clicking
math Fingertip distance calculation
Important Notes
• The program controls the real OS mouse.
• PyAutoGUI FAILSAFE is disabled in the supplied code.
• The current pinch condition may cause repeated clicks if fingers remain close.
Gesture Controller using Hand Tracking Page 2
