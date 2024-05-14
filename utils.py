import math
import cv2
import numpy as np

WHITE = (255, 255, 255)

def euclidean_distance(pt1, pt2):
    return ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**.5
    
def draw_keypoint_ids(frame, keypoints, keypoint_scores):
    blank_image = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)
    # blank_image = frame

    # Loop through all the given keypoints.
    for i, (x, y) in enumerate(keypoints):
        
        # Draw the circle and text on the frame.
        cv2.circle(blank_image, (int(x), int(y)), 2, (255, 0, 0), -1)
        cv2.putText(frame, f"{round(keypoint_scores[i], 2)}", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, cv2.LINE_AA)

    return blank_image

def calculate_centroid(pts):
    tot_x = 0
    tot_y = 0

    for (x, y) in pts:
        tot_x += x
        tot_y += y
    
    tot_x /= len(pts)
    tot_y /= len(pts)

    return (int(tot_x), int(tot_y))