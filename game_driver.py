# for command line arguments
import getopt, sys

import pygame

# pose libraries
import cv2
from inferencer import Inferencer

# game configs
import configs

from utils import pose_to_vector, filter_keypoints, euclidean_distance
from render_utils import load_song, filter_note, draw_line_round_corners_polygon


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

# CLI arguments
arg_list = sys.argv[1:]
camera = True
debug = False
try:
    args, values = getopt.getopt(arg_list, 'nd', ['no_camera', 'debug'])
    for curr_arg, curr_val in args:
        if curr_arg in ('-n', '--no_camera'):
            camera = False
        elif curr_arg in ('-d', '--debug'):
            debug = True
             
except getopt.error as err:
    print (str(err))

# load song
song = load_song('../ExoJoust/notesong.json')

# smoothed pose
pose = [
    pygame.Vector2(-1,-1),
    pygame.Vector2(0,0),
    pygame.Vector2(0,0),
    pygame.Vector2(0,0)
]

#Smoothing values, way lower rn, for more realistic, maybe .8 and 5
smoothingInc = .8
smoothThresh = 5

# keep track of notes on screen
notes_on_screen = []
note_index = 0

# keep track of score and multiplier
score = 0
multiplier = 1
consec_notes = 0

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
            running = False

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

    # pose prediction of body keypoints from webcam
    real_pose = [pose_to_vector(p, screen, cap) for p in filter_keypoints(inferencer.get_pose(frame))]

    #Checks if this is the first time pose is got
    if pose[0] == pygame.Vector2(-1,-1):
        pose = real_pose
    else:
        for num in range(len(pose)):
            # Main Issue im noticing is jittering in certain positions that remains, unsure of how to fix, movement is definitely smoother
            # Maybe add some bound, that way moving slightly doesn't move at all?
            newx = pose[num].x + ((real_pose[num].x - pose[num].x) * smoothingInc)
            newy = pose[num].y + ((real_pose[num].y - pose[num].y) * smoothingInc)
            new = pygame.Vector2(newx,newy)
            if euclidean_distance(pose[num],new) >= smoothThresh:
                pose[num] = new

    # load notes
    if note_index < len(song):
        if total_time > song[note_index][0].start_time - configs.NOTE_SPEED:
            for note in song[note_index]:
                notes_on_screen.append(note)
            note_index += 1

    # check if notes are intersecting the pose
    for note in notes_on_screen:
        note.check_intersecting(pose)

    # remove notes that should have disappeared
    # add score to notes when you hit them
    tmp = []
    for note in notes_on_screen:
        if (not note.is_slider and total_time < note.start_time) or (note.is_slider and total_time < note.end_time):
            tmp.append(note)
            continue
        if not note.is_slider and total_time > note.start_time:
            if note.is_intersecting:
                consec_notes += 1
                if consec_notes > configs.CONSEC_NOTES:
                    consec_notes = 0
                    multiplier = min(multiplier + 1, configs.MAX_MULT)
                score += configs.NOTE_SCORE * multiplier
            else:
                consec_notes = 0
                multiplier = 1
    notes_on_screen = tmp

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

    # draw score
    font = pygame.font.SysFont(None, 48)
    text_surf = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text_surf, (configs.SCREEN_WIDTH - 350, 50))
    text_surf = font.render(f'Multiplier: {multiplier}', True, (255, 255, 255))
    screen.blit(text_surf, (configs.SCREEN_WIDTH - 350, 100))

    # draw song progress
    progress_surface = pygame.Surface((screen.get_width(), 35), pygame.SRCALPHA)
    pygame.draw.rect(
        progress_surface,
        configs.COLORS.get('white'),
        pygame.Rect(0, 0, min(total_time / song[-1][0].start_time * screen.get_width(), screen.get_width()), 35)
    )
    screen.blit(progress_surface, (0, 0))

    # draw notes
    notes_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    for note in notes_on_screen:
        note.draw(notes_surface, total_time)
    screen.blit(notes_surface, (0,0))

    # draw pose
    for k in configs.POSE_INFO.keys():
        pose_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        pose_surface.set_alpha(configs.COLORS.get('pose_alpha'))
        if k == 'hips':
            draw_line_round_corners_polygon(
                pose_surface,
                pose[configs.POSE_INFO.get(k)],
                pose[configs.POSE_INFO.get(k) + 1],
                configs.COLORS.get(k),
                configs.POSE_SIZE
            )
        else:
            pygame.draw.circle(pose_surface, configs.COLORS.get(k), pose[configs.POSE_INFO.get(k)], configs.POSE_SIZE)
        screen.blit(pose_surface, (0,0))

        if debug:
            font = pygame.font.SysFont(None, 32)
            text_surf = font.render(f'{round(pose[configs.POSE_INFO.get(k)].x)}, {round(pose[configs.POSE_INFO.get(k)].y)}', True, (255, 255, 255))
            screen.blit(text_surf, (pose[configs.POSE_INFO.get(k)].x, pose[configs.POSE_INFO.get(k)].y))
            if k == 'hips':
                text_surf = font.render(f'{round(pose[configs.POSE_INFO.get(k) + 1].x)}, {round(pose[configs.POSE_INFO.get(k) + 1].y)}', True, (255, 255, 255))
                screen.blit(text_surf, (pose[configs.POSE_INFO.get(k) + 1].x, pose[configs.POSE_INFO.get(k) + 1].y))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

cap.release()
cv2.destroyAllWindows()
pygame.quit()