import mido
import threading
import re
import random
import logging

class PlayerThread(threading.Thread):
    
    def __init__(self, s_env, s_filepath, q_plyr):
        super(PlayerThread, self).__init__()
        self.stoprequest = False
        self.playing = False
        self.songfile = s_filepath
        self.q_in = q_plyr
        #get the portname (system specific)
        if(s_env == 'record_synth'):
            names = str(mido.get_output_names())
            logging.debug(names)
            ports = names.split(',')
            #logging.debug(ports)
            sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
            #logging.debug(sobj)
            portname = sobj.group()
        if(s_env == 'colinsullivan.me'):
            portname = 'Midi Through:Midi Through Port-0 14:0'
        self.outport = mido.open_output(portname, autoreset=True)

    def join(self, timeout=None):
        self.stoprequest = True 
        super(WorkerThread, self).join(timeout)

    def start(self):
        self.playing == True

    def stop(self):
        self.playing == False

    def change_song(self, filepath):
        self.stop()
        self.songfile = filepath

    def run(self):

        global io_ctrls

        was_playing = False
        channels_in_use = []
        try:
            while not self.stoprequest == False:
                while(io_ctrls['playing']): # == True or sw_right):
                    was_playing = True
                    for msg in MidiFile(self.songfile).play():
                        if(msg.type == 'prog'):
                            channels_in_use.append(msg.channel)
    #--------------------  MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        #if(val_chg == True):
                        if(True):
                            if(msg.type == 'note_on'):
                                #if(sw_33 and msg.channel == knob1):
                                #    msg.note += 7
                                #if(synthmode == 'ISO_CH'):
                                #    if(msg.channel != knob0):
                                #        msg.velocity = 0
                                if(sw_12):
                                    if(msg.channel == 9):
                                        msg.velocity = 0
                                #if(sw_7):
                                #    if(msg.channel == 9):
                                #        msg.velocity = 127
        ##################### SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                        logging.debug('playing...')
                        if(playing == False):
                            break
                if(was_playing == True):
                    self.outport.reset()
                    was_playing = False
        except KeyboardInterrupt:
            print()
        self.outport.reset()
