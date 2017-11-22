#!/usr/bin/env python
import os
import datetime
import time
import threading
from threading import Lock
import logging
import socket
import Queue
from wolftones import WolfTones
from io_intf import IoIntfThread 
import player
from player import PlayerThread
from gui import GuiThread
import copy
from os import listdir
from os.path import isfile, join

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')

song_save_path = '/home/pi/rcrd_synth/raspi/songs/save/'
song_temp_path = '/home/pi/rcrd_synth/raspi/songs/temp/'

default_songfile = song_save_path + 'warriorcatssong.mid'

valid_cmd_names = ['NONE', 'ISO_CHNL', 'NEWSONG', 'POWEROFF']

global io_ctrls
io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

global gui_ctrls
gui_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

global plyr_ctrls
plyr_ctrls = {'chords':0,'lead':0,'bass':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

################################################### INITIALIZE ############################

env = socket.gethostname()

thr_plyr = PlayerThread(env, default_songfile, plyr_ctrls)
thr_plyr.setDaemon(True)
thr_plyr.start()

thr_gui = GuiThread(gui_ctrls, io_ctrls)
thr_gui.setDaemon(True)
thr_gui.start()

if(env == 'record_synth'):
    thr_iointf = IoIntfThread(io_ctrls)
    thr_iointf.setDaemon(True)
    thr_iointf.start()

wt = WolfTones()
################################################# END INITIALIZE ############################

#------------------------------------------------MAIN LOOP-----------------------------------

def main():
    #lock = Lock()
    wt.add_track_info(default_songfile)
    thr_plyr.load_song(default_songfile)
    while(thr_gui.isAlive() and thr_plyr.isAlive() and thr_iointf.isAlive()):
        if(gui_ctrls['val_chg'] == True):
            thr_plyr.plyr_ctrls = thr_gui.gui_ctrls 
            if(gui_ctrls['cmd'] == 'NEWSONG'):
                gui_ctrls['cmd'] = 'NONE'
                #try:
                filename = wt.get_by_genre()
                #logging.debug('MIDI file requested from ' + wt.nkm_encoded_url())
                logging.debug('Retrieved new song ' + filename)
                logging.debug('AFTER RETREIVAL ********** NKM-G-' + wt._nkm_encoded_id())
                thr_plyr.load_song(filename)
                #except:
                #    thr_plyr.load_song(default_songfile)
                #    logging.debug('Retrieval failed')

            if(gui_ctrls['cmd'] == 'LOADSONG'):
                gui_ctrls['cmd'] = 'NONE'
                logging.debug('loading saved song ' + gui_ctrls['songfile'])
                songfiles = [f for f in listdir(song_save_path) if isfile(join(song_save_path, f))]
                #for s in songfiles:
                #    logging.debug(str(s))
                #    logging.debug(str(gui_ctrls['songfile'] in songfiles))
                if(gui_ctrls['songfile'] in songfiles):
                    tmp = song_save_path + gui_ctrls['songfile']
                    logging.debug(tmp)
                    thr_plyr.load_song(tmp)
                else:
                    logging.debug('songfile not in saved')

            #lock.acquire()
            #try:
                #thr_plyr.ctrls.values() = thr_gui.ctrls.values() 

            gui_ctrls['val_chg'] == False
            #finally:
                #lock.release()
        time.sleep(0.05)

    if(thr_plyr.isAlive()):
        thr_plyr.stoprequest.set()
    if(thr_gui.isAlive()):
        thr_gui.stoprequest.set()
    #if(env == 'record_synth' and thr_iointf.isAlive()):
    if(thr_iointf.isAlive()):
        thr_iointf.stoprequest.set()
    quit()

main()
