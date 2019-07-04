"""
Creates a MIDI multi-track and writes it to disk

Limitations: tempo is only written at start of track

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

import struct


class MidiEvent:
    def __init__(self, time=0, control=0, channel=0, param_a=0, param_b=0):
        self.time = time
        self.control = control
        self.channel = channel
        self.param_a = param_a
        self.param_b = param_b

    def __str__(self):
        return '%s%s%s' % (
            chr(self.control << 4 | self.channel),
            chr(self.param_a),
            chr(self.param_b))


class TempoEvent:
    def __init__(self, time=0, tempo=0):
        self.time = 0
        self.tempo = tempo
        self.control = 0xff

    def __str__(self):
        return '\xff\x51\x03%s' % (
            struct.pack('>L', int(60000000 / self.tempo))[1:4])


class MidiTrack:
    def __init__(self, channel=0, tempo=120):
        self.channel = channel
        self.midi_events = []
        self.tempo = tempo

    def add_midi_event(self, time, control, channel, param_a, param_b):
        self.midi_events.append(
            MidiEvent(
                time, control, channel, param_a, param_b
            )
        )

    def add_note(self, time, duration, note, velocity):
        self.midi_events.append(
            MidiEvent(
                time, 0x9, self.channel, note, velocity
            )
        )
        self.midi_events.append(
            MidiEvent(
                time + duration, 0x8, self.channel, note, velocity
            )
        )

    def __str__(self):
        s = ''

        # write tempo as start of track
        self.midi_events.append(TempoEvent(0, self.tempo))

        self.midi_events.sort(key=lambda x: (x.time * 100) + x.control)
        prev_time = 0
        for midi_event in self.midi_events:
            delta_time = 0
            if midi_event.time > prev_time:
                delta_time = midi_event.time - prev_time
                prev_time = midi_event.time

            s += writeVarLength(96 * delta_time)
            s += str(midi_event)

        s += '\x00\xFF\x2F\x00'

        return 'MTrk%s%s' % (struct.pack('>L', len(s)), s)


class MidiFileGenerator:
    def __init__(self):
        self.number_of_track_chunks = 16
        self.ticks_per_beat = 96
        self.tracks = []

    def getHeaderChunk(self):
        return 'MThd\x00\x00\x00\x06\x00\x01%s%s' % (
                               struct.pack('>h', self.number_of_track_chunks),
                               struct.pack('>h', self.ticks_per_beat))

    def writeToFile(self, filename):
        f = open(filename, 'wb')
        f.write(str(self).encode(encoding='UTF-8'))
        f.close()

        print ('Wrote %s track%s to %s' % (
                    len(self.tracks), '' if len(self.tracks) == 1 else 's',
                    filename
                ))

    def __str__(self):
        return '%s%s' % (
            self.getHeaderChunk(),
            ''.join(str(x) for x in self.tracks)
        )


def writeVarLength(value):
    newvalue = 0
    indx = 0
    s = ''
    while (int(value) >> 7 > 0):
        newvalue = (newvalue << 8) + (int(value) & 127)
        if indx > 0:
            newvalue += (1 << 7)
        value = int(value) >> 7
        s = chr(newvalue & 0xff) + s
        indx += 1
    if indx > 0:
        value = value + (1 << 7)
    s = chr(int(value)) + s
    return s

if __name__ == "__main__":
    m = MidiFileGenerator()
    for j in range(16):
        track1 = MidiTrack(channel=j)
        for i in range(20):
            track1.add_note(i, 0.5, 64 + j, 127)
        m.tracks.append(track1)
    m.writeToFile('test.mid')
