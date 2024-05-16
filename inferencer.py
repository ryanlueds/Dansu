import sys, os
MMPOSE_PATH = os.path.join(os.path.dirname(sys.path[0]), 'mmpose')
os.chdir(MMPOSE_PATH)

from mmpose.apis import inference_topdown, init_model

class Inferencer:
    _model_cfg = 'configs/body_2d_keypoint/rtmpose/body8/rtmpose-s_8xb256-420e_body8-256x192.py'
    _ckpt = 'https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-s_simcc-body7_pt-body7_420e-256x192-acd4a1ef_20230504.pth'
    _device = 'cuda:0'
    _metainfo = 'configs/_base_/datasets/coco.py'

    def __init__(self):
        # init model
        self._model = init_model(self._model_cfg, self._ckpt, device=self._device)

    def get_pose(self, frame):
        # inference on a single image
        batch_results = inference_topdown(self._model, frame)
        pred_keypoints = batch_results[0].pred_instances.keypoints[0]

        return pred_keypoints