import sys
print(sys.executable)

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Run the loop.
while True:

    # Read the return flag and the frame.
    ret, frame = cap.read()

    # If no frame/ invalid frame was returned, break the loop.
    if not ret:
        break

    # Get the frame height and width.
    frame_w, frame_h = frame.shape[0], frame.shape[1]

    # Display
    output_frame = cv2.resize(frame, (800,800))
    cv2.imshow('res', output_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()