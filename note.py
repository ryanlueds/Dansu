import pygame
import configs

from utils import euclidean_distance

class Note:
    def __init__(self, is_slider, start_pos, start_time, end_pos=None, end_time=None):
        self.is_slider = is_slider
        self.start_pos = start_pos
        self.start_time = start_time
        self.end_pos = end_pos
        self.end_time = end_time

    
    def draw(self, surface, pose, curr_time):
        if self.is_slider:
            pass
        else:
            color = configs.COLORS.get('white')
            for p in pose:
                if euclidean_distance(self.start_pos, p) < (configs.POSE_SIZE + configs.NOTE_SIZE):
                    color = configs.COLORS.get('green')
                    break
            
            pygame.draw.circle(surface, color, self.start_pos, configs.NOTE_SIZE, width=configs.NOTE_WIDTH)

            time_radius = configs.NOTE_SIZE + ((self.start_time - curr_time)/configs.NOTE_SPEED)*(configs.TIME_SIZE - configs.NOTE_SIZE)
            pygame.draw.circle(surface, configs.COLORS.get('gray'), self.start_pos, time_radius, width=configs.NOTE_WIDTH)