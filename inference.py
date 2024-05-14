import sys, os
MMPOSE_PATH = os.path.join(os.path.dirname(sys.path[0]), 'mmpose')
os.chdir(MMPOSE_PATH)

import cv2

from mmpose.apis import inference_topdown, init_model
from mmpose.visualization import FastVisualizer

model_cfg = 'configs/body_2d_keypoint/rtmpose/body8/rtmpose-s_8xb256-420e_body8-256x192.py'
ckpt = 'https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-s_simcc-body7_pt-body7_420e-256x192-acd4a1ef_20230504.pth'
device = 'cuda:0'
metainfo = 'configs/_base_/datasets/coco.py'

# init model
model = init_model(model_cfg, ckpt, device=device)

visualizer = FastVisualizer(
    model.dataset_meta,
    radius=2,
    line_width=1,
    kpt_thr=0.3
)

cap = cv2.VideoCapture(0)


# Run the loop.
while True:

    # Read the return flag and the frame.
    ret, frame = cap.read()

    # If no frame/ invalid frame was returned, break the loop.
    if not ret:
        break

    # inference on a single image
    batch_results = inference_topdown(model, frame)

    pred_instances = batch_results[0].pred_instances

    visualizer.draw_pose(frame, pred_instances)

    cv2.imshow('MMPose Demo [Press/Hold \'q\' to Exit]', frame)

    if cv2.waitKey(1) == ord('q'):
        break


cv2.destroyAllWindows()