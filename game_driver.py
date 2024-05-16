# for command line arguments
import getopt, sys

import pygame

# pose libraries
import cv2
from inferencer import Inferencer

# game configs
import configs

from utils import pose_to_vector, filter_keypoints
from render_utils import load_song, filter_note


# pygame setup
pygame.init()
pygame.display.set_caption('All You Need is Dance')
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

# display loading screen
screen.fill(configs.COLORS.get('background'))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Initializing...', True, configs.COLORS.get('white'), configs.COLORS.get('background'))
text_rect = text.get_rect()
text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
screen.blit(text, text_rect)
pygame.display.flip()

# whether the camera should be turned off
argumentList = sys.argv[1:]
camera = True
try:
    arguments, values = getopt.getopt(argumentList, 'n', ['no_camera'])
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-n", "--no_camera"):
            camera = False
             
except getopt.error as err:
    print (str(err))

# load song
song = load_song('../ExoJoust/song.json')

# keep track of notes on screen
notes_on_screen = []
note_index = 0

# load model
inferencer = Inferencer()
cap = cv2.VideoCapture(0)

# start clock after loading everything
clock = pygame.time.Clock()
running = True
total_time = 0
reset_clock = 0
dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            break

    # update total time
    if reset_clock > 20:
        total_time += clock.get_time()
    else:
        total_time = 0 # first 20 frames take forever to load
        reset_clock += 1

    # Read the return flag and the frame.
    ret, frame = cap.read()
    if not ret:
        cap.release()
        cv2.destroyAllWindows()
        raise Exception('No frame / invalid frame was returned')

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(configs.COLORS.get('background'))

    # load pose
    skeleton = filter_keypoints(inferencer.get_pose(frame))
    pose = [pose_to_vector(p, screen, cap) for p in skeleton]

    # load notes
    if note_index < len(song):
        if total_time > song[note_index][0].start_time - configs.NOTE_SPEED:
            for note in song[note_index]:
                notes_on_screen.append(note)
            note_index += 1

    # remove notes that should have disappeared
    notes_on_screen[:] = [note for note in notes_on_screen if not filter_note(note, total_time)]

    # draw camera
    if camera:
        frame = cv2.resize(frame, (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 0)
        camera_surface = pygame.Surface((frame.shape[0], frame.shape[1]), pygame.SRCALPHA)
        camera_surface.set_alpha(configs.COLORS.get('pose_alpha'))
        pygame.surfarray.blit_array(camera_surface, frame)
        screen.blit(camera_surface, (0, 0))

    # draw notes
    notes_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    for note in notes_on_screen:
        note.draw(notes_surface, pose, total_time)
    screen.blit(notes_surface, (0,0))

    # draw pose
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