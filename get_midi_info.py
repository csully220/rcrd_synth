#!/usr/bin/env python
from mido import MidiFile
import sys
import mido

filename = sys.argv[1]
mid = MidiFile(filename)

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    #for msg in track:
    #    print(msg)


