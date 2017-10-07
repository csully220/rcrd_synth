#!/usr/bin/env python
import os
import datetime
import random
import threading
import logging
import curses
import mido  
from mido import MidiFile
import re  
from wolftones import *
#from io_intf import *
from player import *
from rt_gui import *

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')
default_songfile = 'songs/warriorcatssong.mid'

#io = IOInterface()
obj_player = Player('server', default_songfile)
obj_rtgui = RtGui()
################################################### INITIALIZE ############################
# flag for starting/stopping MIDI file playback
# threads
thr_plyr = threading.Thread(name='PLAYER', target=obj_player.play_midi_loop)
#thr_io_intf = threading.Thread(name='INPUTS', target=update_control_inputs)
thr_rt_gui = threading.Thread(name='RT_GUI', target=rt_gui_update)

thr_plyr.setDaemon(True)
#thr_io_intf.setDaemon(True)
thr_rt_gui.setDaemon(True)

thr_plyr.start()
#thr_io_intf.start()
thr_rt_gui.start()
################################################# END INITIALIZE ############################

#------------------------------------------------MAIN LOOP-----------------------------------
song_file = default_song_file              
x = 0
while(1):
    pass


################################################# MAIN LOOP ###################################
