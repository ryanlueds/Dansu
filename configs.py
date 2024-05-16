import pygame

COLOR_BACKGROUND = pygame.Color(51, 51, 51, a=255)

COLOR_RED = pygame.Color(237, 28, 36, a=100)
COLOR_BLUE = pygame.Color(115, 251, 253, a=100)
COLOR_GREEN = pygame.Color(117, 250, 141, a=100)
COLOR_YELLOW = pygame.Color(255, 253, 85, a=100)


POSE_SIZE = 40

COLORS = dict(
    background = pygame.Color(51, 51, 51, a=255),
    head = pygame.Color(237, 28, 36, a=-200),
    left_hand = pygame.Color(115, 251, 253, a=3),
    right_hand = pygame.Color(117, 250, 141, a=3),
    hips = pygame.Color(255, 253, 85, a=100)

)

#What if we do
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
