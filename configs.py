import pygame



SCREEN_WIDTH = 1280     
SCREEN_HEIGHT = 720

POSE_SIZE = 60          # size of pose circles

NOTE_SIZE = 40          # size of note circles
TIME_SIZE = 200         # size of the time circle of the note
NOTE_WIDTH = 4          # width of note circle
TIME_WIDTH = 2          # width of time circle
MIN_TIME = 250          # number of miliseconds in 15 frames assuming 60fps
NOTE_SPEED = 2500       # number of milliseconds between a note spawning and time when you hit it

NOTE_SCORE = 1          # number of points for hitting a note
MAX_MULT = 4            # max multipler
CONSEC_NOTES = 5        # number of consecutive notes to increase multiplier

COLORS = dict(
    background = pygame.Color(51, 51, 51),
    head = pygame.Color(237, 28, 36),           # red
    left_hand = pygame.Color(115, 251, 253),    # blue
    right_hand = pygame.Color(163, 73, 164),    # purple
    hips = pygame.Color(255, 253, 85),          # yellow
    white = pygame.Color(255, 255, 255),
    green = pygame.Color(78, 255, 68),
    gray = pygame.Color(204, 204, 204),
    aqua = pygame.Color(100, 247, 255),
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
