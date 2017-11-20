import mido
import threading
import re
import random
import logging
import Queue
from mido import MidiFile
import wolftones_validate




class PlayerThread(threading.Thread):

    def __init__(self, s_env, _songfile, _plyr_ctrls):
        super(PlayerThread, self).__init__()
        self.name = 'Player'
        self.stoprequest = threading.Event()
        self.songfile = _songfile
        self.plyr_ctrls = _plyr_ctrls
        self.channels_in_use = []
        self.midifile = MidiFile(_songfile)

        #get the portname (system specific)
        if(s_env == 'record_synth'):
            names = str(mido.get_output_names())
            ports = names.split(',')
            sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
            portname = sobj.group()
        if(s_env == 'colinsullivan.me'):
            portname = 'Midi Through:Midi Through Port-0 14:0'
        self.outport = mido.open_output(portname, autoreset=True)

    def join(self, timeout=None):
        logging.debug('Player joining..')
        self.outport.reset()
        self.stoprequest.set()
        super(PlayerThread, self).join(timeout)

    def play(self):
        self.plyr_ctrls['play'] = True

    def stop(self):
        self.plyr_ctrls['play'] = False

    def load_song(self, filepath):
            self.stop()
        #try: 
            self.midifile = MidiFile(filepath)
            self.plyr_ctrls['songfile'] = filepath
            logging.debug(str(self.midifile.tracks))
            self.songfile = filepath

    def run(self):
        while(not self.stoprequest.isSet()):
            #while(self.io_ctrls['playing'] == True):
            while(self.plyr_ctrls['play'] == True and not self.stoprequest.isSet()):
                was_playing = True
                for msg in self.midifile.play():
                    #if(self.io_ctrls['playing'] and not self.stoprequest.isSet()):
                    if(self.plyr_ctrls['play'] == True and not self.stoprequest.isSet()):
#-------------- MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        # Here do things that only happen once when a value changes
                        #if(self.plyr_ctrls['val_chg'] == True):
                        #    pass
                        #if(True):
                            #if(msg.type == 'note_on'):
                                #if(sw_33 and msg.channel == knob1):
                                #    msg.note += 7
                                #if(self.plyr_ctrls['mode'] == 'ISO_CH'):
                                #    if(msg.channel != knob0):
                                #        msg.velocity = 0
                                #if(sw_12):
                                    #if(msg.channel == 9):
                                        #msg.velocity = 0
                                #if(sw_7):
                                #    if(msg.channel == 9):
                                #        msg.velocity = 127
 ############# SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                    else:
                        if(was_playing == True):
                            self.outport.reset()
                            was_playing = False
                        break
