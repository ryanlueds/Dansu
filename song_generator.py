import json
import configs
import random
import csv

Jason = r'ExoJoust/notesong.json'
Ceaser = r'ExoJoust/notesong.csv'

song_template = {
    'song': []
}

def make_json(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            #print(rows['X'])
            #print(rows['TIME'])
            song_template['song'].append({
                'is_slider': False,
                'start_pos': (int(rows['X']), int(rows['Y'])),
                'start_time': int(rows['TIME'])
            })
        
        # for rows in csvReader:
        #     key = rows['Some']
        #     data[key] = rows
    json_object = json.dumps(song_template, indent=4)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json_object)
         

make_json(Ceaser, Jason)



