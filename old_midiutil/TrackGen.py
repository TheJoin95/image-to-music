"""
Note generators

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


class StaticIterator:
    """
    A static value generator, returns the same value
    """

    def __init__(self, value=1, id=''):
        self.value = value
        self.id = id

    def __iter__(self):
        return self

    def next(self):
        return self.value


class LoopingArray:
    """
    A generator returning values from an array.


    [value1, value2, value3, value4, ..... valuex]
       ^
    loopindex

    on next(), the loopindex is moved. By default the value is incremented
    by 1, however this can be modified by adding values to the list
    functioniterator (see below).

    Example:
    x = LoopingArray([1,2,3])
    print x.next()
    > 1
    print x.next()
    > 2
    print x.next()
    > 3

    The parameter functioniterator can be used as a stepper function.
    functioniterator
    is a list of tuples (function,generator)

    Example:

    x = LoopingArray(
        [1,2,3,4,5,6],
        functioniterator=[('add', StaticIterator(value=2))]
    )

    This will loop through the array with a step of 2

    x = LoopingArray(
        [1,2,3,4,5,6],
        functioniterator=[('add', LoopingArray([1,2]))]
    )
    This will loop through the array with a step of 1 and then a step of 2

    The items in functioniterator list are evaluated in sequence
    For example:
    x = LoopingArray(
        [1,2,3,4,5,6],
        functioniterator=[
            ('add', StaticIterator(value=2)), ('dec', StaticIterator(value=1))
        ]
    )

    First the array index is incremented by 2 ('add', StaticIterator(value=2))
    and then the index is decremented by 1 ('dec', StaticIterator(value=1))]).
    Having a list of StaticIterator in functioniterator is useless however you
    can create complex patterns when adding other generators such as
    LoopingArray or LoopingIndexedArray.
    """

    def __init__(self, arr,
        functioniterator=[('add', StaticIterator(value=1))], id='',
        debug=False):

        self.arr = arr
        self.index = 0
        self.functioniterator = functioniterator
        self.id = id
        self.debug = debug

    def __iter__(self):
        return self

    def next(self):
        r = self.arr[int(self.index)]

        if self.debug:
            print('%s:%s' % (self.id, r))

        for op, fn in self.functioniterator:
            if op == 'add':
                val = fn.next()
                self.index = (self.index + val) % len(self.arr)
            elif op == 'mult':
                val = fn.next()
                self.index = (self.index * val) % len(self.arr)
            elif op == 'dec':
                val = fn.next()
                self.index = (self.index - val) % len(self.arr)
            elif op == 'div':
                val = fn.next()
                self.index = (self.index / val) % len(self.arr)

        return r


class LoopingIndexedArray:
    """
    A LoopingIndexedArray returns items from an array.

    values = [value1, value2, value3, value4, value5]

    indexes = [index1, index2, index3, index4, index5]
                  ^
              loopindex

    returns values[indexes[loopindex]]

    on next(), the loopindex is moved. By default the value is incremented
    by 1, however this can be modified by adding values to the list
    functioniterator (see below).

    Example:
    x = LoopingIndexedArray([1,2,3,4,5],[0,1,0,2,0,3])
    x.next()
    > 1
    x.next()
    > 2
    x.next()
    > 1
    x.next()
    3
    x.next()
    > 1

    if any of the values in indexes is an array, multiple notes are played
    from the arr index

    x = LoopingIndexedArray([[1],[2],[3],[4],[5]],[[0,1],1,0,2,0,3])
    print x.next()
    print x.next()
    print x.next()
    print x.next()
    print x.next()
    x.next()
    > [1, 2]
    x.next()
    > [2]
    x.next()
    > [1]
    x.next()
    > [3]
    x.next()
    > [1]


    Refer to functioniterator documentation at class LoopingArray
    """

    def __init__(self, arr, indexes,
        functioniterator=[('add', StaticIterator(value=1))], id='',
        debug=False):

        self.arr = arr
        self.indexes = indexes
        self.functioniterator = functioniterator
        self.id = id
        self.index = 0
        self.debug = debug

    def __iter__(self):
        return self

    def next(self):
        if isinstance(self.indexes[int(self.index) % len(self.indexes)], int):
            r = self.arr[
                self.indexes[
                    int(self.index) % len(self.indexes)
                ] % len(self.arr)
            ]
        else:
            r = []
            for x in self.indexes[int(self.index) % len(self.indexes)]:
                r = r + self.arr[x % len(self.arr)]

        if self.debug:
            print('%s:%s' % (self.id, r))

        for op, fn in self.functioniterator:
            if op == 'add':
                val = fn.next()
                self.index = (self.index + val) % len(self.indexes)
            elif op == 'mult':
                val = fn.next()
                self.index = (self.index * val) % len(self.indexes)
            elif op == 'dec':
                val = fn.next()
                self.index = (self.index - val) % len(self.indexes)
            elif op == 'div':
                val = fn.next()
                self.index = (self.index / val) % len(self.indexes)

        return r


class LoopingIncrementalIndexedArray:
    """
    A LoopingIncrementalIndexedArray returns items from an array.

    values = [value1, value2, value3, value4, value5]

    indexes = [index1, index2, index3, index4, index5]
                  ^
              loopindex

    noteindex=noteindex+indexes[loopindex]
    returns values[noteindex]

    on next(), the loopindex is moved. By default the value is incremented
    by 1, however this can be modified by adding values to the list
    functioniterator (see below).

    Example:
    x = LoopingIncrementalIndexedArray([1,2,3,4,5],[0,1,-1,2,0,3])
    x.next()
    > 1
    x.next()
    > 1
    x.next()
    > 2
    x.next()
    > 1
    x.next()
    > 3
    x.next()
    > 3
    x.next()
    > 1

    Note: negative values will move the loopindex to the right

    Refer to functioniterator documentation at class LoopingArray
    """

    def __init__(self, arr, indexes,
        functioniterator=[('add', StaticIterator(value=1))], id='',
        debug=False):

        self.arr = arr
        self.indexes = indexes
        self.index = 0
        self.incindex = 0
        self.functioniterator = functioniterator
        self.id = id
        self.debug = debug

    def __iter__(self):
        return self

    def next(self):
        r = self.arr[int(self.incindex) % len(self.arr)]

        if self.debug:
            print('%s:%s' % (self.id, r))

        self.incindex += self.indexes[self.index % len(self.indexes)]
        self.index += 1

        return r


def add_track(midi, tempo, track, channel, time, startbeat,
    beat=[], notes=[], velocities=[], length=0):
    """
    Adds a midi track. Please use MidiGenerator instead
    """

    midi.addTrackName(track, time, "Track %s" % track)
    midi.addTempo(track, time, tempo)

    beat_index = startbeat
    while beat_index - startbeat < length:
        beat_value, duration_value = beat.next()
        for note in notes.next():
            midi.addNote(
                track,
                channel,
                note,
                beat_index,
                duration_value,
                velocities.next()
            )

        beat_index += beat_value
