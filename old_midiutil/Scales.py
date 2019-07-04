"""
Music Scales

Source: http://en.wikipedia.org/wiki/List_of_musical_scales_and_modes

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

ACOUSTIC_SCALE = [0, 2, 4, 6, 7, 9, 10]
ADONAI_MALAKH = [0, 2, 4, 5, 7, 8, 10]
AEOLIAN_MODE = [0, 2, 3, 5, 7, 8, 10]
ALGERIAN_SCALE = [0, 2, 3, 6, 7, 8, 11]
ALTERED_SCALE = [0, 1, 3, 4, 6, 8, 10]
AUGMENTED_SCALE = [0, 3, 4, 7, 8, 11]
BEBOP_DOMINANT = [0, 2, 4, 5, 7, 9, 10, 11]
BLUES_SCALE = [0, 3, 5, 6, 7, 10]
DORIAN_MODE = [0, 2, 3, 5, 7, 9, 10]
DOUBLE_HARMONIC_SCALE = [0, 1, 4, 5, 7, 8, 11]
ENIGMATIC_SCALE = [0, 1, 4, 6, 8, 10, 11]
FLAMENCO_MODE = [0, 1, 4, 5, 7, 8, 11]
GYPSY_SCALE = [0, 2, 3, 6, 7, 8, 10]
HALF_DIMINISHED_SCALE = [0, 2, 3, 5, 6, 8, 10]
HARMONIC_MAJOR_SCALE = [0, 2, 4, 5, 7, 8, 11]
HARMONIC_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11]
HIRAJOSHI_SCALE = [0, 4, 6, 7, 11]
HUNGARIAN_GYPSY_SCALE = [0, 2, 3, 6, 7, 8, 11]
INSEN_SCALE = [0, 1, 5, 7, 10]
IONIAN_MODE = [0, 2, 4, 5, 7, 9, 11]
IWATO_SCALE = [0, 1, 5, 6, 11]
LOCRIAN_MODE = [0, 1, 3, 5, 6, 8, 10]
LYDIAN_AUGMENTED_SCALE = [0, 2, 4, 6, 8, 9, 11]
LYDIAN_MODE = [0, 2, 4, 6, 7, 9, 11]
MAJOR_LOCRIAN = [0, 2, 4, 5, 6, 8, 10]
MELODIC_MINOR_SCALE = [0, 2, 3, 5, 7, 9, 11]
MIXOLYDIAN_MODE = [0, 2, 4, 5, 7, 9, 10]
NEAPOLITAN_MAJOR_SCALE = [0, 1, 3, 5, 7, 9, 11]
NEAPOLITAN_MINOR_SCALE = [0, 1, 3, 5, 7, 8, 11]
PERSIAN_SCALE = [0, 1, 4, 5, 6, 8, 11]
PHRYGIAN_MODE = [0, 1, 3, 5, 7, 8, 10]
PROMETHEUS_SCALE = [0, 2, 4, 6, 9, 10]
TRITONE_SCALE = [0, 1, 4, 6, 7, 10]
UKRAINIAN_DORIAN_SCALE = [0, 2, 3, 6, 7, 9, 10]
WHOLE_TONE_SCALE = [0, 2, 4, 6, 8, 10]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]


"""
Build a scale given an array s

Example: to build a scale between 0 and 128 using the notes C, D, E

buildScale([0,2,4],0,128)
"""


def buildScale(s, min_note=0, max_note=128):
    return [x + (12 * j)
        for j in range(12)
        for x in s
        if x + (12 * j) >= min_note and x + (12 * j) <= max_note]
