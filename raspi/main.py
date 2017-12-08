#!/usr/bin/env python
import os
import datetime
import time
import threading
from threading import Lock
import logging
import socket
import Queue

import wolftones
from wolftones import WolfTones

import io_intf 
from io_intf import IoIntfThread 

import player
from player import PlayerThread

import gui
from gui import GuiThread
from os import listdir
from os.path import isfile, join

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')

song_save_path = '/home/pi/rcrd_synth/raspi/songs/save/'
song_temp_path = '/home/pi/rcrd_synth/raspi/songs/temp/'

#default_songfile = song_save_path + 'warriorcatssong.mid'
default_songfile = song_temp_path + '25-31-149244754-1-16087-58-58-4-2709-51-0-5-102-36-502-54-203-0-0-5-122-0.mid'


valid_cmd_names = ['NONE', 'ISO_CHNL', 'NEWSONG', 'POWEROFF']

io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

gui_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

main_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

plyr_ctrls = {'play':False, 'perc':80, 'generic':80,'poly':80, 'upr_ld':80, 'lwr_ld':80, 'mov_ld':80, 'str_ld':80, 'chords':80, 'bass':80, 'val_chg':False, 'songfile':'warriorcatssong.mid'}

################################################### INITIALIZE ############################

################################################# END INITIALIZE ############################

def main():

    global io_ctrls
    global gui_ctrls
    global plyr_ctrls

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
    wt.load_file(default_songfile)
    thr_plyr.load_song(default_songfile)

    while(thr_gui.isAlive() and thr_plyr.isAlive() and thr_iointf.isAlive()):
        if(gui_ctrls['val_chg'] or io_ctrls['val_chg']):

            plyr_ctrls['val_chg'] = main_ctrls['val_chg'] or io_ctrls['val_chg'] 
            for key in main_ctrls:
                main_ctrls[key] = gui_ctrls[key] or io_ctrls[key]
            
            plyr_ctrls['play'] = main_ctrls['play'] or io_ctrls['sw_right'] 
            plyr_ctrls['generic'] = io_ctrls['knob0'] 
            #plyr_ctrls['poly'] = gui_ctrls['knob1'] 
            plyr_ctrls['poly'] = io_ctrls['knob0'] 
            #plyr_ctrls['upr_ld'] = gui_ctrls['knob1']
            plyr_ctrls['upr_ld'] = io_ctrls['knob1']
            #plyr_ctrls['lwr_ld'] = gui_ctrls['knob1']
            plyr_ctrls['lwr_ld'] = io_ctrls['knob1']
            #plyr_ctrls['mov_ld'] = gui_ctrls['knob1']
            plyr_ctrls['mov_ld'] = io_ctrls['knob1']
            #plyr_ctrls['str_ld'] = gui_ctrls['knob1']
            plyr_ctrls['str_ld'] = io_ctrls['knob2']
            #plyr_ctrls['chords'] = gui_ctrls['knob2']
            plyr_ctrls['chords'] = io_ctrls['knob2']
            #plyr_ctrls['bass'] = gui_ctrls['knob3']
            plyr_ctrls['bass'] = io_ctrls['knob3']
            #plyr_ctrls['perc'] = main_ctrls['knob4']
            plyr_ctrls['perc'] = io_ctrls['knob4']
            plyr_ctrls['perc'] = io_ctrls['knob4']
 
            gui_ctrls['val_chg'] = False
            io_ctrls['val_chg'] = False
            plyr_ctrls['val_chg'] = False

            if(gui_ctrls['cmd'] == 'NEWSONG'):
                gui_ctrls['cmd'] = 'NONE'
                filename = wt.get_by_genre()
                logging.debug('New song: ' + filename)
                #logging.debug('AFTER RETREIVAL ********** NKM-G-' + wt._nkm_encoded_id())
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

        time.sleep(0.05)

    if(thr_plyr.isAlive()):
        thr_plyr.stoprequest.set()
    if(thr_gui.isAlive()):
        thr_gui.stoprequest.set()
    if(thr_iointf.isAlive()):
        thr_iointf.stoprequest.set()
    quit()

main()
