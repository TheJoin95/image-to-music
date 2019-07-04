"""
MIDI note generator

Copyright (C) 2012  Alfred Farrugia

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from os import path
import sys
from old_midiutil.TrackGen import LoopingArray
from old_midiutil.MidiFileGenerator import MidiFileGenerator, MidiTrack


class MidiGenerator:
    def __init__(self, filename='', tempo=120):
        """
        If filename is empty, set the midi file to the __main__file_name.mid
        """
        if filename == '':
            self.filename = os.path.basename(
                path.abspath(sys.modules['__main__'].__file__)
                ).split('.')[0] + '.mid'
        else:
            self.filename = filename

        self.midi = MidiFileGenerator()
        self.tempo = tempo

    def add_track(self, track, time, trackname='',
        beat=[], notes=[], velocities=[], length=0):

        # append to existing track
        if track < len(self.midi.tracks):
            track = self.midi.tracks[track]
        else:
            track = MidiTrack(channel=track, tempo=self.tempo)
            self.midi.tracks.append(track)

        beat_index = time
        while beat_index - time < length:
            beat_value, duration_value = beat.next()
            for note in notes.next():
                track.add_note(
                    beat_index,
                    duration_value,
                    note, velocities.next()
                )

            beat_index += beat_value

    def add_arpeggio(self, track, time, chords_beat=[], notes_beat=[],
        chords=[], velocities=[], note_skip=LoopingArray([1, 2, 3]), length=0):

        track = MidiTrack(channel=track, tempo=self.tempo)

        beat_index = time
        bi = beat_index
        while beat_index - time < length:
            chordindex = 0
            beat_value, _ = chords_beat.next()
            chord = chords.next()
            while (bi < beat_index + beat_value) and (bi < length):
                chordindex = note_skip.next()
                note = chord[chordindex % len(chord)]
                notes_beat_value, notes_duration_value = notes_beat.next()
                track.add_note(
                    bi,
                    notes_duration_value,
                    note,
                    velocities.next())

                bi += notes_beat_value
            beat_index += beat_value

        self.midi.tracks.append(track)

    def write(self):
        self.midi.writeToFile(self.filename)
