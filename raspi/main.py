#!/usr/bin/env python
import os
import datetime
import time
import threading
from threading import Lock
import logging
import socket

import wolftones
from wolftones import WolfTonesSong

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
default_songfile = song_save_path + 'default.mid'


valid_cmd_names = ['NONE', 'ISO_CHNL', 'NEWSONG', 'POWEROFF']

io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

gui_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

main_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'songfile':'warriorcatssong.mid', 'mode':'DEFAULT', 'cmd':'NONE', 'play':False, 'val_chg':False}

plyr_ctrls = {'play':False,
              'val_chg':False, 
              #channel velocities 
              'perc':80, 
              'generic':80,
              'poly':80, 
              'upr_ld':80, 
              'lwr_ld':80, 
              'mov_ld':80, 
              'str_ld':80, 
              'chords':80, 
              'bass':80,
              #key and scale
              'key':60,
              'scale':[0],
              'drum_fill':False, 
              'songfile':'default.mid'}

################################################### INITIALIZE ############################

################################################# END INITIALIZE ############################

def main():

    global io_ctrls
    global gui_ctrls
    global plyr_ctrls

    #intialization
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
    
    wt = WolfTonesSong(song_save_path, song_temp_path)
    wt.load_file(default_songfile)
    thr_plyr.load_song(default_songfile)

    #filename = wt.get_by_genre()
    #thr_plyr.load_song(filename)

    plyr_ctrls['key'] = wt.key
    plyr_ctrls['scale'] = wt.scale

    while(thr_gui.isAlive() and thr_plyr.isAlive() and thr_iointf.isAlive()):
        if(gui_ctrls['val_chg'] or io_ctrls['val_chg']):

            plyr_ctrls['val_chg'] = main_ctrls['val_chg'] or io_ctrls['val_chg'] 

            for key in main_ctrls:
                main_ctrls[key] = gui_ctrls[key] or io_ctrls[key]
            
            plyr_ctrls['play']    = main_ctrls['play'] or io_ctrls['sw_right'] 
 
            if(main_ctrls['sw_start']):
                plyr_ctrls['perc']    = io_ctrls['knob0']
                plyr_ctrls['generic'] = io_ctrls['knob1'] 
                plyr_ctrls['poly']    = io_ctrls['knob1'] 
                plyr_ctrls['upr_ld']  = io_ctrls['knob2']
                plyr_ctrls['lwr_ld']  = io_ctrls['knob2']
                plyr_ctrls['mov_ld']  = io_ctrls['knob2']
                plyr_ctrls['str_ld']  = io_ctrls['knob2']
                plyr_ctrls['chords']  = io_ctrls['knob3']
                plyr_ctrls['bass']    = io_ctrls['knob4']
                vel_src_custom = True
                        
            elif( not (main_ctrls['sw_start'] or main_ctrls['sw_auto']) ):
                plyr_ctrls['perc']    = 64
                plyr_ctrls['generic'] = 64 
                plyr_ctrls['poly']    = 64
                plyr_ctrls['upr_ld']  = 64
                plyr_ctrls['lwr_ld']  = 64
                plyr_ctrls['mov_ld']  = 64
                plyr_ctrls['str_ld']  = 64
                plyr_ctrls['chords']  = 64
                plyr_ctrls['bass']    = 64
            

            plyr_ctrls['drum_fill'] = io_ctrls['sw_33']

            io_ctrls['val_chg']   = False
            gui_ctrls['val_chg']  = False
            plyr_ctrls['val_chg'] = False

            if(gui_ctrls['cmd'] == 'NEWSONG'):
                gui_ctrls['cmd'] = 'NONE'
                filename = wt.get_by_genre()
                logging.debug('New song: ' + filename)
                #logging.debug('AFTER RETREIVAL ********** NKM-G-' + wt._nkm_encoded_id())
                plyr_ctrls['key'] = wt.key
                plyr_ctrls['scale'] = wt.scale
                thr_plyr.load_song(filename)

            if(gui_ctrls['cmd'] == 'LOADSONG'):
                gui_ctrls['cmd'] = 'NONE'
                logging.debug('loading saved song ' + gui_ctrls['songfile'])
                songfiles = [f for f in listdir(song_save_path) if isfile(join(song_save_path, f))]
                if(gui_ctrls['songfile'] in songfiles):
                    wt.load_file(default_songfile)
                    #plyr_ctrls['key'] = wt.key
                    #plyr_ctrls['scale'] = wt.scale
                    tmp = song_save_path + gui_ctrls['songfile']
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
