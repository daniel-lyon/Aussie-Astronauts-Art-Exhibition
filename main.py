# Import functions
import numpy as np
import matplotlib.pylab as plt
from music21 import note, stream
import time
from skimage.transform import resize
from random import random

# Read in the image
image = plt.imread('test_image.jpg')
# image = plt.imread('composite.png')
# image = plt.imread('170x170.jpg')
image = image/255
image = resize(image, (200, 200))
height = image.shape[0]
width = image.shape[1]

# List of notes to use
note_names = ['C2','D2','E2','G2','A2',
             'C3','D3','E3','G3','A3',
             'C4','D4','E4','G4','A4',
             'C5','D5','E5','G5','A5']
note_values = [round(i * 1/len(note_names)+0.05, 3) for i in range(len(note_names))]

# Volume settings
volume_values = [i+1 for i in range(16, 80)]
volume_norm = [i/128 for i in volume_values]

start_time = time.process_time()
print('start')

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
print('duration done')

# Setting the notes to be played
notes_page = np.empty((height, width), dtype = list)
for y in range(width):
    for x in range(height):
    
        value = image[x][y][1] # page 1 = green

        for index, notes in enumerate(note_names):
            if value <= note_values[index]:
                notes_page[x][y] = notes
                break
print('notes done')

# Setting the volume of each note
volume_page = np.empty((height, width), dtype = int)
for y in range(width):
    for x in range(height):

        value = image[x][y][2] # page 2 = blue

        for index, volume in enumerate(volume_values):
            if value <= volume_norm[index]:
                volume_page[x][y] = volume
                break
print('volume done')

# Combine notes with duration and volume
full_audio = stream.Stream()
for y in range(width):
    s = stream.Part()
    r = round(random(), 1)
    for x in range(height):
        n = note.Note(notes_page[x][y], quarterLength = duration_page[x][y])
        n.volume.velocity = volume_page[x][y]
        s.insert(y+r, n)
    full_audio.append(s)
print('audio done')

# Export file
full_audio.write('mid', 'piano.mid')

# Time to execute program
end_time = time.process_time()
print(f'Finished in {end_time - start_time} seconds')