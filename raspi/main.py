#!/usr/bin/env python
import os
import datetime
import time
import threading
import logging
import socket
from wolftones import WolfTones
from io_intf import IoIntfThread 
import player
from player import PlayerThread
from rt_gui import RtGuiThread

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')
default_songfile = 'songs/warriorcatssong.mid'

knobs = {'knob1':0, 'knob2':0,'knob3':0,'knob4':0,'knob5':0}
switches = {'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0}

################################################### INITIALIZE ############################
gi_knob0=0
gi_knob1=0
gi_knob2=0
gi_knob3=0
gi_knob4=0
gi_sw_12=0
gi_sw_7=0
gi_sw_auto=0
gi_sw_start=0
gi_sw_33=0
gi_sw_78=0
gi_sw_left=0
gi_sw_right=0
#gi_sw_rotenc=0
#gi_sw_prog=0
gi_synthmode='DEFAULT'
gi_playing=False     
gi_ctrl_val_chg = False

io_knob0=0
io_knob1=0
io_knob2=0
io_knob3=0
io_knob4=0
io_sw_12=0
io_sw_7=0
io_sw_auto=0
io_sw_start=0
io_sw_33=0
io_sw_78=0
io_sw_left=0
io_sw_right=0
#io_sw_rotenc=0
#io_sw_prog=0
io_synthmode='DEFAULT'
io_playing=False     
io_ctrl_val_chg = False


env = socket.gethostname()

thr_player = PlayerThread(env, default_songfile)
thr_player.setDaemon(True)
thr_player.start()

thr_rtgui = RtGuiThread()
thr_rtgui.setDaemon(True)
thr_rtgui.start()

if(env == 'record_synth'):
    thr_iointf = IoIntfThread()
    thr_iointf.setDaemon(True)
    thr_iointf.start()

x = None
wt = WolfTones()
synthmode = 'DEFAULT'
playing = False
################################################# END INITIALIZE ############################




#------------------------------------------------MAIN LOOP-----------------------------------

while(thr_rtgui.isAlive()): #and thr_iointf.isAlive()):
    if(io_ctrl_val_chg):
        pl_knob0 = io_knob0
        pl_knob1 = io_knob1
        pl_knob2 = io_knob2
        pl_knob3 = io_knob3
        pl_knob4 = io_knob4
        pl_sw_12 = io_sw_12
        pl_sw_7 = io_sw_7
        pl_sw_auto = io_sw_auto
        pl_sw_start = io_sw_start
        pl_sw_33 = io_sw_33
        pl_sw_78 = io_sw_78
        pl_sw_left = io_sw_left
        pl_sw_right = io_sw_right
        pl_synthmode = io_synthmode
        io_ctrl_val_chg = False

    if(gi_ctrl_val_chg):
        pl_knob0 = gi_knob0
        pl_knob1 = gi_knob1
        pl_knob2 = gi_knob2
        pl_knob3 = gi_knob3
        pl_knob4 = gi_knob4
        pl_sw_12 = gi_sw_12
        pl_sw_7 = gi_sw_7
        pl_sw_auto = gi_sw_auto
        pl_sw_start = gi_sw_start
        pl_sw_33 = gi_sw_33
        pl_sw_78 = gi_sw_78
        pl_sw_left = gi_sw_left
        pl_sw_right = gi_sw_right    
        pl_synthmode = gi_synthmode
        gi_ctrl_val_chg = False


