import pygame

POSE_SIZE = 40

COLORS = dict(
    background = pygame.Color(51, 51, 51),
    head = pygame.Color(237, 28, 36),
    left_hand = pygame.Color(115, 251, 253),
    right_hand = pygame.Color(117, 250, 141),
    hips = pygame.Color(255, 253, 85),
    pose_alpha = 128
)


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

POSE_INFO = dict(
    head=0,
    left_hand=1,
    right_hand=2,
    hips=3
)
