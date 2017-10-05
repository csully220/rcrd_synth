#!/usr/bin/env python
import os
import datetime
import random
import threading
import time
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
default_song_file = 'songs/warriorcatssong.mid'

#io = IOInterface()
            
def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input

#------------------------------------------------------------------------------- INPUTS THREAD --------------------------------------
def update_control_inputs():

    global knob0
    global knob1
    global knob2
    global knob3
    global knob4
    global sw_12
    global sw_7
    global sw_auto
    global sw_start
    global sw_33
    global sw_78
    global sw_left
    global sw_right
    global sw_rotenc
    global sw_prog
    global ctrl_val_chg
    global playing
    global synthmode   

    while(1):
        if(io.unpack_serial()):
            logging.debug('Getting new inputs...')

            knob4 = io.get_knob(4)/10
            knob3 = io.get_knob(3)/10 
            knob2 = io.get_knob(2)/10 
            knob1 = io.get_knob(1)/10
            knob0 = io.get_knob(0)/10

            sw_12 = io.get_switch(7)
            sw_7  = io.get_switch(6) 
            sw_auto = io.get_switch(5)
            sw_start = io.get_switch(4)
            sw_33 = io.get_switch(3)
            sw_78 = io.get_switch(2)
            sw_left = io.get_switch(1)
            sw_right = io.get_switch(0)

            tmp_mode = io.get_mode()
            if(synthmode != tmp_mode):
                synthmode = tmp_mode

            #if(synthmode == 'PWROFF'):
            #    os.system('sudo poweroff')

            ctrl_val_chg = True

            #if(sw_right):
                #playing = True
            #else:
                #playing = False

            #logging.debug(str(knob4))
            #logging.debug(str(knob3))
            #logging.debug(str(knob2))
            #logging.debug(str(knob1))
            #logging.debug(str(knob0))
            #logging.debug('12     ' + str(sw_12))
            #logging.debug('7      ' + str(sw_7))
            #logging.debug('auto   ' + str(sw_auto))
            #logging.debug('start  ' + str(sw_start))
            #logging.debug('33     ' + str(sw_33))
            #logging.debug('78     ' + str(sw_78))
            #logging.debug('left   ' + str(sw_left))
            #logging.debug('right  ' + str(sw_right))
        else: 
            #sleep briefly so we don't eat up processor
            time.sleep(0.03)
############################################################################### END INPUTS THREAD ###################################

################################################### INITIALIZE ############################
# flag for starting/stopping MIDI file playback
#playing = False

# threads
thr_plyr = threading.Thread(name='PLAYER', target=play_midi)
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
