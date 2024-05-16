import json
import pygame
from note import Note

def load_song(file_name):
    f = open(file_name)
    data = json.load(f)

    # sort song by when notes appear
    notes = sorted(data['song'], key=lambda x: int(x['start_time']))

    # [[note1, note2, note3], [note4]]
    song = []

    for n in notes:
        is_slider = n['is_slider'] == 'True'
        start_pos = pygame.Vector2(tuple(map(int, n['start_pos'].split(','))))
        start_time = int(n['start_time'])

        note = None
        if is_slider:
            end_pos = pygame.Vector2(tuple(map(int, n['end_pos'].split(','))))
            end_time = int(n['end_time'])
            note = Note(is_slider, start_pos, start_time, end_pos=end_pos, end_time=end_time)
        else:
            note = Note(is_slider, start_pos, start_time)

        if not song:
            song.append([note])
        else:
            if song[-1][0].start_time == note.start_time:
                song[-1].append(note)
            else:
                song.append([note])

    return song


'''
Returns true if note should be filtered out
'''
def filter_note(note, clock_time):
    if note.is_slider and clock_time > note.end_time:
        return True
    if not note.is_slider and clock_time > note.start_time:
        return True
    
    return False