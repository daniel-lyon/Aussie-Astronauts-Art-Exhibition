# Import functions
import numpy as np
import matplotlib.pylab as plt
from music21 import note, stream
from skimage.transform import resize

# Read in the image
image = plt.imread('image.png')

# Image details
height = image.shape[0]
width = image.shape[1]
aspect_ratio = round(width/height, 3)

# Minimum heights and widths for different aspect ratios
if aspect_ratio == 1.778:
    min_width = 192
    min_height = 108
elif aspect_ratio == 2.333:
    min_width = 196
    min_height = 84
elif aspect_ratio == 1.333:
    min_width = 200
    min_height = 150
else:
    min_width = 200
    min_height = 200

# Resize image
if height > min_height or width > min_width:
    image = resize(image, (min_height, min_width))

# Get new image height and width
height = image.shape[0]
width = image.shape[1]

# List of notes to use
note_names = ['C2','D2','E2','G2','A2',
             'C3','D3','E3','G3','A3',
             'C4','D4','E4','G4','A4',
             'C5','D5','E5','G5','A5']
num_notes = len(note_names)
note_values = [round(i * 1/num_notes + 1/num_notes, 3) for i in range(len(note_names))]

# Volume settings
min_volume = 16 # absolute minimum = 0
max_volume = 60 # absolute maximum = 128
volume_values = [i+1 for i in range(min_volume, max_volume)]
volume_norm = [i/(min_volume+max_volume) for i in volume_values]

# Setting the duration of each note
duration_page = np.empty((height, width), dtype = int)
for y in range(width):
    for x in range(height):
    
        value = image[x][y][0] # page 0 = red
        
        if value < 0.25:
            duration_page[x][y] = 1

        elif 0.25 <= value < 0.5:
            duration_page[x][y] = 2

        elif 0.5 <= value < 0.75:
            duration_page[x][y] = 3

        elif value >= 0.75:
            duration_page[x][y] = 4

# Setting the notes to be played
notes_page = np.empty((height, width), dtype = list)
for y in range(width):
    for x in range(height):
    
        value = image[x][y][1] # page 1 = green

        for index, notes in enumerate(note_names):
            if value <= note_values[index]:
                notes_page[x][y] = notes
                break

# Setting the volume of each note
volume_page = np.empty((height, width), dtype = int)
for y in range(width):
    for x in range(height):

        value = image[x][y][2] # page 2 = blue

        for index, volume in enumerate(volume_values):
            if value <= volume_norm[index]:
                volume_page[x][y] = volume
                break

# Combine notes with duration and volume
full_audio = stream.Score()
for y in range(width):
    s = stream.Part()
    for x in range(height):
        n = note.Note(notes_page[x][y], quarterLength = duration_page[x][y])
        n.volume.velocity = volume_page[x][y]
        s.insert(y*2, n)
    full_audio.append(s)

# Export file
full_audio.write('mid', 'piano.mid')