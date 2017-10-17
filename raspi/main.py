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

song_save_path = '/home/pi/rcrd_synth/raspi/songs/save/'
song_temp_path = '/home/pi/rcrd_synth/raspi/songs/temp/'

default_songfile = song_save_path + 'warriorcatssong.mid'

global io_ctrls
io_ctrls = {'knob0':0, 'knob1':0,'knob2':0,'knob3':0,'knob4':0, 'sw_12':0, 'sw_7':0,'sw_auto':0,'sw_start':0,'sw_33':0,'sw_78':0,'sw_left':0,'sw_right':0, 'synthmode':'DEFAULT', 'command':'NONE', 'playing':False, 'ctrl_val_chg':False}

################################################### INITIALIZE ############################

env = socket.gethostname()

q_plyr = Queue.Queue()
thr_player = PlayerThread(env, default_songfile, io_ctrls)
thr_player.setDaemon(True)
thr_player.start()

q_gui = Queue.Queue()
thr_gui = RtGuiThread(q_gui)
thr_gui.setDaemon(True)
thr_gui.start()

if(env == 'record_synth'):
    thr_iointf = IoIntfThread()
    thr_iointf.setDaemon(True)
#    thr_iointf.start()

wt = WolfTones()
################################################# END INITIALIZE ############################

#------------------------------------------------MAIN LOOP-----------------------------------
def main():
    while(thr_gui.isAlive() and thr_player.isAlive()):
        try:
            pair = q_gui.get(True, 0.1) #blocks until gets
            #logging.debug('gui queue not empty')
            io_ctrls[pair.keys()[0]] = pair.values()[0]
            #logging.debug(pair.keys()[0] + ' : ' + str(pair.values()[0]))
            playing = io_ctrls['playing']
            if(io_ctrls['command'] == 'NEWSONG'):
                io_ctrls['command'] = 'NONE'
                try:
                    response = wt.get_by_genre()
                    #logging.debug('MIDI file requested from ' + wt.nkm_encoded_url())
                    if(response.content):
                        logging.debug('Got a new song from Wolftones')
                        tmp = song_temp_path + 'dl_song-{:%m-%d-%H:%M}'.format(datetime.datetime.now()) + '.mid'
                        with open(tmp, 'w+') as f:
                            f.write(response.content)
                        thr_player.change_song(tmp)
                except:
                    song_file = default_songfile
                    logging.debug('Wolftones retrieval failed')

        except Queue.Empty:
            pass
    if(thr_player.isAlive()):
        thr_player.join()
    if(thr_gui.isAlive()):
        thr_gui.join()
    if(env == 'record_synth' and thr_iointf.isAlive()):
        thr_iointf.join()

main()
