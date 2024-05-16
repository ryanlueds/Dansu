import pygame

# pose libraries
import cv2
from inferencer import Inferencer

# game configs
import configs

from utils import pose_to_vector, filter_keypoints

# pygame setup
pygame.init()
pygame.display.set_caption('All You Need is Dance')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

inferencer = Inferencer()
cap = cv2.VideoCapture(0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read the return flag and the frame.
    ret, frame = cap.read()
    if not ret:
        raise Exception('No frame / invalid frame was returned')

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(configs.COLORS.get('background'))

    skeleton = filter_keypoints(inferencer.get_pose(frame))
    pose = [pose_to_vector(p, screen, cap) for p in skeleton]

    for k in configs.POSE_INFO.keys():
        pose_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        pose_surface.set_alpha(configs.COLORS.get('pose_alpha'))
        pygame.draw.circle(pose_surface, configs.COLORS.get(k), pose[configs.POSE_INFO.get(k)], configs.POSE_SIZE)
        screen.blit(pose_surface, (0,0)) 

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
pygame.quit()