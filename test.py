from music21 import note, stream
from random import random

n1 = note.Note(38, quarterLength = 2)
n2 = note.Note(35, quarterLength = 2)
n3 = note.Note(35, quarterLength = 2)
n4 = note.Note(42, quarterLength = 2)

s = stream.Part()
r = round(random(), 1)
print(r)

s.insert(0+r, n1)
r = random()
s.insert(0+r, n2)
r = random()
s.insert(0+r, n3)
r = random()
s.insert(0+r, n4)

s.write('mid', 'test.mid')