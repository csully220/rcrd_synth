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

main_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

global plyr_ctrls
plyr_ctrls = {'play':False, 'vel_perc':0, 'vel_chords':0,'vel_lead':0,'vel_bass':0, 'ch_chords':0,'ch_lead':0,'ch_bass':0, 'songfile':'warriorcatssong.mid'}

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
    thr_plyr.load_song(default_songfile, chan_roles = {})
    while(thr_gui.isAlive() and thr_plyr.isAlive() and thr_iointf.isAlive()):
        if(gui_ctrls['val_chg'] or io_ctrls['val_chg']):
            gui_ctrls['val_chg'] = False
            io_ctrls['val_chg'] = False
            i = 0
            for key in main_ctrls:
                main_ctrls[key] = gui_ctrls[key] or io_ctrls[key]
            
            plyr_ctrls['play'] = main_ctrls['play'] 
            plyr_ctrls['vel_perc'] = io_ctrls['knob0'] 
            plyr_ctrls['vel_generic'] = io_ctrls['knob1'] 
            plyr_ctrls['vel_poly'] = io_ctrls['knob1'] 
            plyr_ctrls['vel_upr_ld'] = io_ctrls['knob2']
            plyr_ctrls['vel_lwr_ld'] = io_ctrls['knob2']
            plyr_ctrls['vel_mov_ld'] = io_ctrls['knob2']
            plyr_ctrls['vel_str_ld'] = io_ctrls['knob2']
            plyr_ctrls['vel_chords'] = io_ctrls['knob3']
            plyr_ctrls['vel_bass'] = io_ctrls['knob4']
            #plyr_ctrls['perc'] = main_ctrls['knob5']
            #plyr_ctrls['perc'] = 
            #plyr_ctrls['perc'] = 
            #plyr_ctrls['perc'] = 
            
            if(gui_ctrls['cmd'] == 'NEWSONG'):
                gui_ctrls['cmd'] = 'NONE'
                #try:
                filename = wt.get_by_genre()
                #logging.debug('MIDI file requested from ' + wt.nkm_encoded_url())
                logging.debug('Retrieved new song ' + filename)
                logging.debug('AFTER RETREIVAL ********** NKM-G-' + wt._nkm_encoded_id())
                thr_plyr.load_song(filename, wt.chan_roles)
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
                    thr_plyr.load_song(tmp,  wt.chan_roles)
                else:
                    logging.debug('songfile not in saved')

            #lock.acquire()
            #try:
                #thr_plyr.ctrls.values() = thr_gui.ctrls.values() 

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
