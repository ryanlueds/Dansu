import pygame
import cv2

KEYPOINT_INFO = dict(
    nose=0,
    left_eye=1,
    right_eye=2,
    left_elbow=7,
    right_elbow=8,
    left_wrist=9,
    right_wrist=10,
    left_hip=11,
    right_hip=12
)
    
def filter_keypoints(keypoints):
    head = calculate_centroid([
        keypoints[KEYPOINT_INFO.get('nose')],
        keypoints[KEYPOINT_INFO.get('left_eye')],
        keypoints[KEYPOINT_INFO.get('right_eye')],
    ])
    left_hand = calculate_centroid([
        keypoints[KEYPOINT_INFO.get('left_wrist')]
    ])
    right_hand = calculate_centroid([
        keypoints[KEYPOINT_INFO.get('right_wrist')]
    ])
    hips = calculate_centroid([
        keypoints[KEYPOINT_INFO.get('left_hip')],
        keypoints[KEYPOINT_INFO.get('right_hip')]
    ])

    return [head, left_hand, right_hand, hips]


def calculate_centroid(pts):
    tot_x = 0
    tot_y = 0

    for (x, y) in pts:
        tot_x += x
        tot_y += y
    
    tot_x /= len(pts)
    tot_y /= len(pts)

    return (int(tot_x), int(tot_y))


def pose_to_vector(pose, screen, cap):
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # pygame screen has x coordinates flipped
    x = int(screen.get_width() - ((pose[0] / width) * screen.get_width()))
    
    y = int((pose[1] / height) * screen.get_height())

    return pygame.Vector2(x, y)