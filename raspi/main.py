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

default_songfile = 'songs/warriorcatssong.mid'

io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'synthmode':'DEFAULT', 'playing':False, 'ctrl_val_chg':False}

################################################### INITIALIZE ############################

pl_knob0=0
pl_knob1=0
pl_knob2=0
pl_knob3=0
pl_knob4=0
pl_sw_12=0
pl_sw_7=0
pl_sw_auto=0
pl_sw_start=0
pl_sw_33=0
pl_sw_78=0
pl_sw_left=0
pl_sw_right=0
pl_synthmode='DEFAULT'
pl_playing=False
pl_ctrl_val_chg=False

env = socket.gethostname()

q_plyr = Queue.Queue()
thr_player = PlayerThread(env, default_songfile, q_plyr, io_ctrls)
#thr_player.setDaemon(True)
thr_player.start()

q_gui = Queue.Queue()
thr_rtgui = RtGuiThread(q_gui)
#thr_rtgui.setDaemon(True)
thr_rtgui.start()

if(env == 'record_synth'):
    thr_iointf = IoIntfThread()
    thr_iointf.setDaemon(True)
    thr_iointf.start()

wt = WolfTones()
pl_synthmode = 'DEFAULT'
################################################# END INITIALIZE ############################

#------------------------------------------------MAIN LOOP-----------------------------------
def main():
    while(thr_rtgui.isAlive() and thr_player.isAlive()):
        try:
            pair = q_gui.get(True, 0.05)
            #logging.debug('gui queue not empty')
            io_ctrls[pair.keys()[0]] = pair.values()[0]
            logging.debug(pair.keys()[0] + ' : ' + str(pair.values()[0]))
            q_plyr.put(pair)

        except Queue.Empty:
            continue

#            pl_knob0 = io_ctrls['knob0']
#            pl_knob1 = io_ctrls['knob1']
#            pl_knob2 = io_ctrls['knob2']
#            pl_knob3 = io_ctrls['knob3']
#            pl_knob4 = io_ctrls['knob4']
#            pl_sw_12 = io_ctrls['sw_12']
#            pl_sw_7 = io_ctrls['sw_7']
#            pl_sw_auto = io_ctrls['sw_auto']
#            pl_sw_start = io_ctrls['sw_start']
#            pl_sw_33 = io_ctrls['sw_33']
#            pl_sw_78 = io_ctrls['sw_78']
#            pl_sw_left = io_ctrls['sw_left']
#            pl_sw_right = io_ctrls['sw_right']
#            pl_synthmode = io_ctrls['synthmode']
#            pl_playing = io_ctrls['playing']
 
    thr_rtgui.join()
    thr_player.join()

main()
