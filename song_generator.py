import json
import configs
import random

filename = '../Exojoust/song.json'

song_template = {
    'song': []
}

for i in range(1, 61):
    song_template['song'].append({
        'is_slider': False,
        'start_pos': (random.randint(int(configs.SCREEN_WIDTH * .2), int(configs.SCREEN_WIDTH * .8)), random.randint(int(configs.SCREEN_HEIGHT * .2), int(configs.SCREEN_HEIGHT * .8))),
        'start_time': 2000 * i
    })

json_object = json.dumps(song_template, indent=4)

with open(filename, "w") as outfile:
    outfile.write(json_object)