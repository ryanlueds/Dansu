import pygame
import configs
import cv2


def filter_keypoints(keypoints):
    head = calculate_centroid([
        keypoints[configs.KEYPOINT_INFO.get('nose')],
        keypoints[configs.KEYPOINT_INFO.get('left_eye')],
        keypoints[configs.KEYPOINT_INFO.get('right_eye')],
    ])
    lw = keypoints[configs.KEYPOINT_INFO.get('left_wrist')]
    le = keypoints[configs.KEYPOINT_INFO.get('left_elbow')]
    rw = keypoints[configs.KEYPOINT_INFO.get('right_wrist')]
    re = keypoints[configs.KEYPOINT_INFO.get('right_elbow')]
    left_hand = (lw[0] + .25*(lw[0] - le[0]),
                 lw[1] + .25*(lw[1] - le[1]))
    right_hand = (rw[0] + .25*(rw[0] - re[0]),
                  rw[1] + .25*(rw[1] - re[1]))
    hips = calculate_centroid([
        keypoints[configs.KEYPOINT_INFO.get('left_hip')],
        keypoints[configs.KEYPOINT_INFO.get('right_hip')]
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


'''
v1 and v2 are pygame.Vector2 objects
'''
def euclidean_distance(v1, v2):
    #print("v1, ",v1)
    #print("v2, ",v2)
    x1, y1 = v1.xy
    x2, y2 = v2.xy

    return ((x1 - x2)**2 + (y1 - y2)**2)**.5