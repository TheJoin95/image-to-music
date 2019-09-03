# Music-generator-midi

Demo here: https://thejoin95.github.io/image-to-music/index.html

This little experiment is made in Python and Three.js.
The three.js base was made by a girl, but I could not find the link to the her repo anymore. I'm sorry.

## Generate Midi music from image
The img2mid script take in input some images and produce a midi file.

The music is made by a combination of colors: given a portion (pixel) of the image it's calculated the avg color and assigned to a midi note.
The duration of a not is given by the brightness of the pixel portion. More bright, the duration is up to 4s and the min is around 0.25s.

The drum's notes are given by the darkest colors (grey, dark brown and black).


I also tried to map the various colors to the light spectrum and then converted them into notes, but without success.

Sometimes the "songs" are shorter than other or sometimes they are "cringe".. it is almost a random sequence of notes.

All the midi files will be converted into a mp3 file, for web compability.

## Art Gallery
The Art Gallery idea came up since some images are paintings.
I used a premade box from a girl then I customized everything with some colors, pattern and audio.

If someone find her repo, please, contact me so I can give her the reference.

