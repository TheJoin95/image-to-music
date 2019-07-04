import pygame, argparse
from PIL import Image
from midiutil.MidiFile import MIDIFile
from itertools import groupby
import math
import numpy as np

A0_NOTE = 1
C8_NOTE = 127


frequency_mapping = [
    (69, 220.000000000000), (70, 224.974515832279), (71, 230.061512608947), (72, 235.263533685635), (73, 240.583179926894),
    (74, 246.023111006560), (75, 251.586046737508), (76, 257.274768431491), (77, 263.092120289711), (78, 269.041010824843),
    (79, 275.124414315209), (80, 281.345372291834), (81, 287.706995059126), (82, 294.212463249940), (83, 300.865029415806),
    (84, 307.668019653116), (85, 314.624835266072), (86, 321.738954467250), (87, 329.013934116606), (88, 336.453411499804),
    (89, 344.061106146758), (90, 351.840821691297), (91, 359.796447772867), (92, 367.931961981248), (93, 376.251431845236),
    (94, 384.759016866289), (95, 393.458970598169), (96, 402.355642773591), (97, 411.453481478973), (98, 420.757035378352),
    (99, 430.270955987590), (100, 440.000000000000)]

def RGB2wav(r,g,b):

  if g == 0.0 and b == 1.0:
    wavelength = r*(350.-440.)+440.
  elif r == 0.0 and b == 1.0:
    wavelength = g*(490.-440.)+440.
  elif r == 0.0 and g == 1.0:
    wavelength = b*(490.-510.)+510.
  elif b == 0.0 and g == 1.0:
    wavelength = r*(580. - 510.)+510.
    print (r,g,b,wavelength)
  elif b == 0.0 and r == 1.0:
    wavelength = g*(580.-645.)+645
  elif b == 0.0 and r == 1.0 and g == 0.0:
    wavelength = 645
  elif b == 0.0 and g == 1.0 :
    wavelength = r*(580. - 510.)+510.
  else:
    wavelength = 340

  return wavelength

def lerp(min, max, note):
  # return int(min + note * (max - min))
  if note > max:
    return max
  elif note < min:
    return min
  else:
    return note


def convert_rgb_to_note(r, g, b):
  return [lerp(A0_NOTE, C8_NOTE, int(r)), lerp(A0_NOTE, C8_NOTE, int(g)), lerp(A0_NOTE, C8_NOTE, int(b))]
  return lerp(A0_NOTE, C8_NOTE, int((r+g+b)/6.0))


def add_note(song, track, pitch, time, duration, channel=0):
  song.addNote(track, channel, pitch, time, duration, 100)


def create_midi(tempo, data, r, g, b, drums):
  print ('Converting to MIDI.')
  song = MIDIFile(5)
  song.addTempo(0, 0, tempo)

  song.addProgramChange(0, 0, 0, 0)

  song.addProgramChange(0, 2, 0, 26)  # r
  song.addProgramChange(0, 3, 0, 41)  # g
  song.addProgramChange(0, 4, 0, 40)  # b

  song.addProgramChange(0, 10, 0, 35)

  grouped = [(note, sum(1 for i in g)) for note, g in groupby(data)]
  time = 0
  for note, duration in grouped:
    if type(note) is not int:
      for chord in note:
        add_note(song, 0, chord, time, duration)
    else:
      add_note(song, 0, note, time, duration)
    time += duration

  grouped = [(note, sum(1 for i in j)) for note, j in groupby(r)]
  time = 0
  for note, duration in grouped:
    if type(note) is not int:
      for chord in note:
        add_note(song, 0, chord, time, duration)
    else:
      add_note(song, 0, note, time, duration, channel=2)
    time += duration

  grouped = [(note, sum(1 for i in j)) for note, j in groupby(g)]
  time = 0
  for note, duration in grouped:
    if type(note) is not int:
      for chord in note:
        add_note(song, 0, chord, time, duration)
    else:
      add_note(song, 0, note, time, duration, channel=3)
    time += duration

  grouped = [(note, sum(1 for i in j)) for note, j in groupby(b)]
  time = 0
  for note, duration in grouped:
    if type(note) is not int:
      for chord in note:
        add_note(song, 0, chord, time, duration)
    else:
      add_note(song, 0, note, time, duration, channel=4)
    time += duration

  grouped = [(note, sum(1 for i in j)) for note, j in groupby(drums)]
  time = 0
  for note, duration in grouped:
    if type(note) is not int:
      for chord in note:
        add_note(song, 0, chord, time, duration, channel=10)
    else:
      add_note(song, 0, note, time, duration, channel=10)
    time += duration

  return song


def play_midi(music_file):
  clock = pygame.time.Clock()
  try:
    pygame.mixer.music.load(music_file)
    print ("Music file %s loaded. Press Ctrl + C to stop playback." % music_file)
  except Exception as e:
    print ("Error loading file: %s - %s" % (music_file, e))
    return
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    clock.tick(30)

def convert_to_bw(image):
  return image.convert('L')

def get_image_channel(img):
  red, green, blue = img.split()
  return {
    "red": red,
    "green": green,
    "blue": blue
  }

def get_image_portion(img, w, h, firstMethod=False):
  # if w > 1000 or h > 1000:
  #   w = 800
  #   h = 800
  #   img.thumbnail((w, h), Image.ANTIALIAS)

  if firstMethod == False:
    w, h = img.size

    xPixels = int(math.pow(w, 1/8))
    yPixels = int(math.pow(h, 1/3))

    portions = []
    pixelArray = np.array(img)

    xArrayIterator = 0
    tempArray = []
    while xArrayIterator < len(pixelArray):
      sumArray = pixelArray[xArrayIterator]
      # arrays = pixelArray[xArrayIterator:xPixels]
      # for array in arrays:
      #   tempArray.append(np.mean(array, axis = 0))
      # xArrayIterator = xArrayIterator + xPixels

      for i in range(xArrayIterator+1, xPixels):
        sumArray = sumArray + pixelArray[i]
      
      xArrayIterator = xArrayIterator + xPixels
      #tempArray.append(sumArray / xPixels)
      tempArray.append(np.mean(sumArray, axis = 0))

    #### a questo punto io ho tante striscie, già con il colore medio calcolato
    #### dovrei splittare in verticale, così da avere più striscie, anche in orizzontale, no?
    portions = []
    for array in tempArray:
      yIterator = 0
      while yIterator < len(array):
        splitArray = []
        for i in range(yIterator, yPixels):
          splitArray.append(array)

        if splitArray != []:
          portions.append(np.mean(splitArray, axis = 0))
        yIterator = yIterator + yPixels

        # splitArray = array[yIterator:yPixels]
        # print(splitArray)
        # portions.append(np.mean(splitArray, axis = 0))
        # yIterator = yIterator + yPixels
  else:
    wLimit = int(math.pow(w, 1/2))
    hLimit = int(math.pow(h, 1/2))

    portions = []
    x = 0
    y = 0

    for x, y in [(0, 0), (int(w * 0.8), 0), (int(w * 0.45), 0), (0, int(w * 0.8)), (0, int(w * 0.45))]:
      while x < w and y < h:
        portion = []

        for yPortion in range(hLimit):
          for xPortion in range(wLimit):
            print("xPortion: %d, yPortion: %d" % (x+xPortion, y+yPortion))
            try:
              pixelValue = img.getpixel((x+xPortion, y+yPortion))
              portion.append(pixelValue)
            except Exception as e:
              print(e)
              pass

        y = y + 1
        x = x + 1
        print("X: %d, Y: %d" % (x, y))
        portions.append(portion)

    portions = get_portion_rgb_mean(portions)

  return portions

def get_portion_rgb_mean(portions):
  portionColorMean = []
  for i in range(len(portions)):
    meanCounter = 0
    rTotal = gTotal = bTotal = 0
    for j in range(len(portions[i])):
      r, g, b = portions[i][j]
      print("r: %d, g: %d, b: %d" % (r, g, b))
      rTotal = rTotal + r
      gTotal = gTotal + g
      bTotal = bTotal + b
      meanCounter = meanCounter + 1

    portionColorMean.append([int(rTotal/meanCounter), int(gTotal/meanCounter), int(bTotal/meanCounter)])

  return portionColorMean

def get_song_data(filename):
  try:
    im = Image.open(filename).convert('RGB')
  except Exception as e:
    print ("Error loading image: %s" % e)
    raise SystemExit
  print ("Img %s loaded." % filename)
  w, h = im.size

  # im = convert_to_bw(im)
  # print(im.getpixel((100, 100))) # brightness 0 - 255
  # raise
  medianRGBs = get_image_portion(im, w, h, False)
  #medianRGBs = get_portion_rgb_mean(portions)

  # channels = get_image_channel(im)

  # red = get_image_portion(channels['red'], w, h)
  # red = get_image_portion(im, w, h)
  # print(red)
  # raise

  print(medianRGBs)

  notes = redNotes = greenNotes = blueNotes = []
  drumNotes = []
  for rgb in medianRGBs:
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])

    print("r: %d, g: %d, b: %d" % (r, g, b))

    if r < 80 and g < 80 and b < 80:
      if r > 30 and g > 30 and b > 30:
        drumNotes.append(convert_rgb_to_note(r, g, b))
    else:
      # drumNotes.append(0)
      notes.append(convert_rgb_to_note(r, g, b))
      redNotes.append(min(int(r*0.7), 110))
      greenNotes.append(min(int(g*0.7), 110))
      blueNotes.append(min(int(b*0.7), 110))

  drumNotes = drumNotes[0:len(notes)]
  print("notes: %d, drumNotes: %d" % (len(notes), len(drumNotes)))

  return (notes, redNotes, greenNotes, blueNotes, drumNotes)
  return [convert_rgb_to_note(r, g, b) for r, g, b in medianRGBs]


def convert(img_file, midi_file, play):
  pygame.init()
  data, red, green, blue, drums = get_song_data(img_file)
  song = create_midi(240, data, red, green, blue, drums)
  with open(midi_file, 'wb') as f:
    song.writeFile(f)

  if play:
    try:
      play_midi(midi_file)
    except KeyboardInterrupt:
      pygame.mixer.music.fadeout(1000)
      pygame.mixer.music.stop()
      raise SystemExit


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert image file to midi.')
  parser.add_argument('input', nargs=1, help='Path to input image file')
  parser.add_argument('output', nargs=1, help='Path to output midi file')
  parser.add_argument('--play', action='store_true', default=False, help='Play file after conversion')
  args = vars(parser.parse_args())

  convert(args['input'][0], args['output'][0], args['play'])