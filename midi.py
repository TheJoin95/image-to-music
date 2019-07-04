#!/usr/bin/python
import sys
from PIL import Image

from old_midiutil.MidiGenerator import MidiGenerator
from old_midiutil.TrackGen import LoopingArray

filename = sys.argv[1]
midifilename = filename[0:filename.find('.')]+'.midi'

#load the image and get it's dimensions
im = Image.open(filename)
pix = im.load()
width, height = im.size

#one list for each color channel rgb
red = []
green = []
blue = []

last_g = 50

#go over the image pixel by pixel
for y in range(0, height):
    for x in range(0, width):
        r, g, b = pix[x, y]
        red.append([r, g, b]) #get the notes
        green.append(((g+16)/255.0, last_g/255.0)) #get the duration of each note
        last_g = b+16
        blue.append(b) #velocities


duration = 3000
from_note = int(len(red)/2-duration)
to_note = from_note+duration
le_red = red[from_note:to_note]
le_green = green[from_note:to_note]
le_blue = blue[from_note:to_note]

#create the midi file
midiGenerator = MidiGenerator(filename=midifilename, tempo=150)

notes = LoopingArray(le_red)
beats = LoopingArray(le_green)
velocities = LoopingArray(le_blue)

#print(notes.arr)
#raise

#use the midigenerator to create the track with the image's pixel data
midiGenerator.add_track(0, 0, beat=beats, notes=notes, velocities=velocities, length=duration)
midiGenerator.write()