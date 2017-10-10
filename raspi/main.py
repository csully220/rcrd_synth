#!/usr/bin/env python
import os
import datetime
import time
import threading
import logging
import socket
import Queue
from wolftones import WolfTones
from io_intf import IoIntfThread 
import player
from player import PlayerThread
from rt_gui import RtGuiThread

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')
#obj_log = logging.getLogger('rcrd_synth')
default_songfile = 'songs/warriorcatssong.mid'

io_ctrls = {'knob1':0, 'knob2':0,'knob3':0,'knob4':0,'knob5':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'playing':False, 'ctrl_val_chg':False}
gi_ctrls = pl_ctrls = io_ctrls

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

#ev_gi_ctrl_upd = threading.Event()
q_plyr = Queue.Queue()
thr_player = PlayerThread(env, default_songfile, q_plyr)
thr_player.setDaemon(True)
thr_player.start()

q_gui = Queue.Queue()
thr_rtgui = RtGuiThread(q_gui)
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
    while(not q_gui.empty()):
        pair = q_gui.get()
        io_ctrls[pair.keys()[0]] = pair.values()[0]
        logging.debug(pair.keys()[0] + ' : ' + str(pair.values()[0]))
        #q_plyr.put(pair)
        #io_ctrls['ctrl_val_chg'] = True

