import mido
import threading
import re
import random
import logging
import Queue
from mido import MidiFile

class PlayerThread(threading.Thread):
   
    def __init__(self, s_env, _songfile, _io_ctrls):
        super(PlayerThread, self).__init__()
        self.name = 'Player'
        self.stoprequest = threading.Event()
        self.songfile = _songfile
        self.io_ctrls = _io_ctrls
        self.channels_in_use = []
       
        self.knob0 = self.io_ctrls['knob0']
        self.knob1 = self.io_ctrls['knob1']
        self.knob2 = self.io_ctrls['knob2']
        self.knob3 = self.io_ctrls['knob3']
        self.knob4 = self.io_ctrls['knob4']

        self.sw_12 = self.io_ctrls['sw_12']
        self.sw_7 = self.io_ctrls['sw_7']
        self.sw_auto = self.io_ctrls['sw_auto']
        self.sw_start = self.io_ctrls['sw_start']
        self.sw_33 = self.io_ctrls['sw_33']
        self.sw_78 = self.io_ctrls['sw_78']
        self.sw_left = self.io_ctrls['sw_left']
        self.sw_right = self.io_ctrls['sw_right']
        self.synthmode = self.io_ctrls['synthmode']
        self.playing = self.io_ctrls['playing']
        
 
        #get the portname (system specific)
        if(s_env == 'record_synth'):
            names = str(mido.get_output_names())
            #logging.debug(names)
            ports = names.split(',')
            #logging.debug(ports)
            sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
            #logging.debug(sobj)
            portname = sobj.group()
        if(s_env == 'colinsullivan.me'):
            portname = 'Midi Through:Midi Through Port-0 14:0'
        self.outport = mido.open_output(portname, autoreset=True)

    def join(self, timeout=None):
        logging.debug('joining ..')
        self.outport.reset()
        self.stoprequest.set()
        super(PlayerThread, self).join(timeout)

    def play(self):
        self.io_ctrls['playing'] == True

    def stop(self):
        self.io_ctrls['playing'] == False

    def change_song(self, filepath):
        self.stop()
        self.songfile = filepath

    def run(self):
        while(not self.stoprequest.isSet()):
            while(self.io_ctrls['playing'] == True):
                was_playing = True
                for msg in MidiFile(self.songfile).play():
                    if(self.io_ctrls['playing'] and not self.stoprequest.isSet()):
                        if(msg.type == 'program_change' and not msg.channel in self.channels_in_use):
                            self.channels_in_use.append(msg.channel)
                            logging.debug('saved channel:  ' + str(self.channels_in_use[-1])) 
#   --------    ------  MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        #if(val_chg == True):
                        #if(True):
                            #if(msg.type == 'note_on'):
                                #if(sw_33 and msg.channel == knob1):
                                #    msg.note += 7
                                #if(synthmode == 'ISO_CH'):
                                #    if(msg.channel != knob0):
                                #        msg.velocity = 0
                                #if(sw_12):
                                    #if(msg.channel == 9):
                                        #msg.velocity = 0
                                #if(sw_7):
                                #    if(msg.channel == 9):
                                #        msg.velocity = 127
 ###########    ## SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                         #logging.debug('notes')
                    else:
                        if(was_playing == True):
                            self.outport.reset()
                            was_playing = False
                        break
