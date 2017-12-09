import mido
import threading
import re
import random
import logging
from mido import MidiFile

class PlayerThread(threading.Thread):

    global plyr_ctrls

    def __init__(self, s_env, _songfile, _plyr_ctrls):
        super(PlayerThread, self).__init__()
        self.name = 'Player'
        self.stoprequest = threading.Event()
        self.songfile = _songfile
        self.plyr_ctrls = _plyr_ctrls
        self.chan_roles = [0 for i in range(16)] 
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

    def load_song(self, filepath):
            #self.stop()
            self.midifile = MidiFile(filepath)
            self.plyr_ctrls['songfile'] = filepath
            logging.debug(str(self.midifile.tracks))
            self.songfile = filepath
            for trk in self.midifile.tracks:
                s = trk.name.split(':')
                chan = s[0]
                role = s[1] 
                #logging.debug('read  ' + chan + ' as ' + role)
                self.chan_roles[int(chan)] = role
                logging.debug('Channel ' + str(chan) + ' is ' + role)
                
    def run(self):
        while(not self.stoprequest.isSet()):
            while(self.plyr_ctrls['play'] == True and not self.stoprequest.isSet()):
                #logging.debug('perc ' + str(self.plyr_ctrls['perc']))
                #logging.debug('bass ' + str(self.plyr_ctrls['bass']))
                was_playing = True
                ch_ro = self.chan_roles
                for msg in self.midifile.play():
                    if(self.plyr_ctrls['play'] == True and not self.stoprequest.isSet()):
#-------------- MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        # Here do things that only happen once when a value changes
                        #if(self.plyr_ctrls['val_chg'] == True):
                        #    pass
                        #if(True):
                        if(msg.type == 'note_on'):
                            msg.velocity = self.plyr_ctrls[ch_ro[msg.channel]]
############# SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                    else:
                        if(was_playing == True):
                            self.outport.reset()
                            was_playing = False
                        break
