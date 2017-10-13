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


global io_ctrls
io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'synthmode':'DEFAULT', 'playing':False, 'ctrl_val_chg':False}

################################################### INITIALIZE ############################

env = socket.gethostname()

q_plyr = Queue.Queue()
thr_player = PlayerThread(env, default_songfile, io_ctrls)
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
            playing = io_ctrls['playing']
            q_plyr.put(pair)

        except Queue.Empty:
            pass

    thr_player.join()
    thr_rtgui.join()

main()
