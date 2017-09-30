#!/usr/bin/env python
import sys
import mido
import re
from mido import MidiFile

filename = sys.argv[1]
if len(sys.argv) == 3:
    portname = sys.argv[2]
else:
    portname = None

names = str(mido.get_output_names())
ports = names.split(',')
sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
portname = sobj.group()

#with mido.open_output(ports[0]) as output:
with mido.open_output(portname) as output:
    try:
        for msg in MidiFile(filename).play():
            print(msg)
            output.send(msg)

    except KeyboardInterrupt:
        print()
    output.reset()
