#!/usr/bin/env python
import os
import datetime
import time
import threading
from threading import Lock
import logging

import io_intf 
from io_intf import IoIntfThread 

import player
from player import PlayerThread

import gui
from gui import GuiThread
from os import listdir
from os.path import isfile, join
from os import system 

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')

song_save_path = '/home/pi/rcrd_synth/raspi/songs/'
song_temp_path = '/home/pi/rcrd_synth/raspi/songs/temp/'

#default_songfile = song_save_path + 'warriorcatssong.mid'
default_songfile = 'tmp_song-12-18-03:07.mid'

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

    env = 'record_synth'
    
# intialization
    
    thr_plyr = PlayerThread(song_temp_path, default_songfile, plyr_ctrls)
    thr_plyr.setDaemon(True)
    thr_plyr.start()
    
    thr_gui = GuiThread(gui_ctrls, io_ctrls)
    thr_gui.setDaemon(True)
    thr_gui.start()
    
    if(env == 'record_synth'):
        thr_iointf = IoIntfThread(io_ctrls)
        thr_iointf.setDaemon(True)
        thr_iointf.start()
    
    #thr_plyr.load_song(default_songfile)

    while(thr_gui.isAlive() and thr_plyr.isAlive() and thr_iointf.isAlive()):
# copy / translate the inputs for use
        tmp_cmd = 'NONE'
        if(gui_ctrls['val_chg'] or io_ctrls['val_chg']):
            if(gui_ctrls['cmd'] != 'NONE'):
                tmp_cmd = gui_ctrls['cmd']
                gui_ctrls['cmd'] = 'NONE'

            if(io_ctrls['cmd'] != 'NONE'):
                tmp_cmd = io_ctrls['cmd']
                io_ctrls['cmd'] = 'NONE'

            plyr_ctrls['val_chg'] = main_ctrls['val_chg'] or io_ctrls['val_chg']

            for key in main_ctrls:
                main_ctrls[key] = (gui_ctrls[key] or io_ctrls[key])
            
            plyr_ctrls['play'] = (main_ctrls['play'] or io_ctrls['sw_right'])

# velocity control for tracks 
            if(main_ctrls['sw_start']):
                #logging.debug('dynamic volume')
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
                #logging.debug('fixed volume')
                plyr_ctrls['perc']    = 64
                plyr_ctrls['generic'] = 64 
                plyr_ctrls['poly']    = 64
                plyr_ctrls['upr_ld']  = 64
                plyr_ctrls['lwr_ld']  = 64
                plyr_ctrls['mov_ld']  = 64
                plyr_ctrls['str_ld']  = 64
                plyr_ctrls['chords']  = 64
                plyr_ctrls['bass']    = 64

# fills and riffs 
            plyr_ctrls['drum_fill'] = main_ctrls['sw_33']
            plyr_ctrls['lead_fill'] = main_ctrls['sw_12']
# command messages
            if(tmp_cmd == 'NEWSONG'):
                tmp_cmd = 'NONE'
                thr_plyr.new_song()

            if(tmp_cmd == 'LOADSONG'):
                tmp_cmd = 'NONE'
                songfiles = [f for f in listdir(song_temp_path) if isfile(join(song_temp_path, f))]
                songfiles = [f for f in listdir(song_temp_path) if isfile(join(song_temp_path, f))]
                if(gui_ctrls['songfile'] in songfiles):
                    thr_plyr.load_song(gui_ctrls['songfile'])
                    logging.debug('loading saved song ' + gui_ctrls['songfile'])
                else:
                    logging.debug('songfile not in saved')
            if(tmp_cmd == 'POWEROFF'):
                logging.debug('powering off... ')
                #os.system('sudo poweroff') 

# finish up
            io_ctrls['val_chg']   = False
            gui_ctrls['val_chg']  = False
            plyr_ctrls['val_chg'] = False

        time.sleep(0.01)

    if(thr_plyr.isAlive()):
        thr_plyr.stoprequest.set()
    if(thr_gui.isAlive()):
        thr_gui.stoprequest.set()
    if(thr_iointf.isAlive()):
        thr_iointf.stoprequest.set()
    quit()

main()
