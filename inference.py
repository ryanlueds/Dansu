import cv2
import numpy as np
from mmpose.apis import MMPoseInferencer

cap = cv2.VideoCapture(0)

# build the inferencer with 3d model alias
inferencer = MMPoseInferencer(pose2d='human')

# Run the loop.
while True:

    # Read the return flag and the frame.
    ret, frame = cap.read()

    # If no frame/ invalid frame was returned, break the loop.
    if not ret:
        break

    # The MMPoseInferencer API employs a lazy inference approach,
    # creating a prediction generator when given input
    result_generator = inferencer(frame, return_vis=True)
    result = next(result_generator)
    frame = result['visualization'][0]

    # Display
    output_frame = cv2.resize(frame, (1400,800))
    cv2.imshow('res', output_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()