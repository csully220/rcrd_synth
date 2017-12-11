import mido
import threading
import re
import random
import logging
from mido import MidiFile
from mido import Message

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
            #fluidsynth backend running on pi. Note that the following change to the dbus /etc/system.conf file may be needed to run the audio backend headless. 
            #<policy user="pi">
            #    <allow own="org.freedesktop.ReserveDevice1.Audio0"/>
            #</policy>
            sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
            portname = sobj.group()
        if(s_env == 'colinsullivan.me'):
            #dummy port for testing on a headless server with no audio
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
            # length of a quarter note
            self.ticks_per_beat = self.midifile.ticks_per_beat
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
                ch_roles = self.chan_roles
                for msg in self.midifile.play():
                    if(self.plyr_ctrls['play'] == True and not self.stoprequest.isSet()):
     #-------------- MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        # Here do things that only happen once when a value changes
                        if(self.plyr_ctrls['val_chg'] == True):
                            self.plyr_ctrls['val_chg'] = False
                            pass
                        
                        if(msg.type == 'note_on' and msg.velocity):
                            ctrl_vel = self.plyr_ctrls[ch_roles[msg.channel]]
                            #logging.debug('ctrl_vel ' + str(ctrl_vel))
                            msg_vel = msg.velocity
                            msg.velocity = self.get_scaled_velocity(msg_vel, ctrl_vel) 
                            if(self.plyr_ctrls['drum_fill']):
                                if(ch_roles[msg.channel] == 'perc'):
                                    df_msg = msg.copy()
                                    df_msg.time = int(self.ticks_per_beat/8)
                                    df_msg.note = 35
                                    df_msg.velocity = self.get_scaled_velocity(msg.velocity, 100)
                                    self.outport.send(df_msg)
     ############ SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                    else:
                        if(was_playing == True):
                            self.outport.reset()
                            was_playing = False
                        break

    def get_scaled_velocity(self, msg_vel, ctrl_vel):
        ctrl_vel_ratio = float(ctrl_vel)/127
        #logging.debug('msg_vel ' +  str(msg_vel))
        #logging.debug('ratio ' +  str(ctrl_vel_ratio))
        if(ctrl_vel_ratio == 0.5):
             rtn_vel = msg_vel
        elif(ctrl_vel_ratio > 0.5):
             rtn_vel = msg_vel + ((127 - msg_vel)*((ctrl_vel/64)-1))
        elif(ctrl_vel_ratio < 0.5):
             rtn_vel = ctrl_vel_ratio * msg_vel * 2
        #logging.debug('rtn_vel ' +  str(rtn_vel))
        return int(rtn_vel)
