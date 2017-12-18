import mido
import threading
import re
import random
import logging
from mido import MidiFile
from mido import Message
import wolftones
from wolftones import WolfTonesSong
import socket

class PlayerThread(threading.Thread):

    global plyr_ctrls

    def __init__(self, _save_path, songfile, _plyr_ctrls):
        super(PlayerThread, self).__init__()
        self.name = 'Player'
        self.stoprequest = threading.Event()
        self.plyr_ctrls = _plyr_ctrls
        self.chan_roles = [0 for i in range(10)]
        self.plyr_ctrls['songfile'] = songfile
        self.midifile = MidiFile(_save_path + songfile)
        # 0 - drum fill
        self.counter = [0 for i in range(4)]
        self.wt = WolfTonesSong()
        self.save_path = _save_path
        self.load_song(songfile)
        self.alt_meas = []

        #get the portname (system specific)
        env = socket.gethostname()
        if(env == 'record_synth'):
            names = str(mido.get_output_names())
            ports = names.split(',')
            sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
            portname = sobj.group()
        if(env == 'colinsullivan.me'):
            #dummy port for testing on a headless server with no audio
            portname = 'Midi Through:Midi Through Port-0 14:0'
        self.outport = mido.open_output(portname, autoreset=True)

    def join(self, timeout=None):
        logging.debug('Player joining..')
        self.outport.reset()
        self.stoprequest.set()
        super(PlayerThread, self).join(timeout)

    def set_save_path(self, path, temp = False):
        if(path):
            self.save_path = path
        if(temp):
            self.save_path = path + 'temp' 

    def stop(self):
        self.plyr_ctrls['play'] = False

    def load_song(self, filename):
            self.stop() 
            tmp = filename.split('.')
            # if you forget or are too lazy to type the filetype extenstion
            if(len(tmp) > 1 and tmp[-1] != 'mid'):
                filename += '.mid'
            songfile = self.save_path + filename
            self.wt.load_file(songfile)
            self.midifile = MidiFile(songfile)
            self.plyr_ctrls['songfile'] = filename
            #logging.debug(str(self.midifile.tracks))
            # length of a quarter note
            self.ticks_per_beat = self.midifile.ticks_per_beat
            #self.chan_roles = [0 for i in range(10)]
            for trk in self.midifile.tracks:
                s = trk.name.split(':')
                chan = s[0]
                role = s[1] 
                #logging.debug('read  ' + chan + ' as ' + role)
                self.chan_roles[int(chan)] = role
                if(role[-3:] == '_ld'):
                    logging.debug('making riff')
                    self.make_riff(trk)
                logging.debug('Channel ' + str(chan) + ' is ' + role)
               
    def new_song(self):
            # save path here should be /songs/temp
            path = self.save_path
            fn = self.wt.get_by_genre(save_path=path)

            songfile = fn 
            self.midifile = MidiFile(songfile)
            self.plyr_ctrls['songfile'] = songfile
            #logging.debug(str(self.midifile.tracks))
            # length of a quarter note
            self.ticks_per_beat = self.midifile.ticks_per_beat
            #self.chan_roles = [0 for i in range(10)]
            for trk in self.midifile.tracks:
                s = trk.name.split(':')
                chan = s[0]
                role = s[1]
                #logging.debug('read  ' + chan + ' as ' + role)
                self.chan_roles[int(chan)] = role
                ld_role = len(re.match('ld', role)) > 0
                if(ld_role):
                    logging.debug('making riff')
                    self.make_riff(trk)
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
                                    df_msg.time = int(self.ticks_per_beat/16)
                                    df_msg.note = random.choice([35,36])
                                    df_msg.velocity = self.get_scaled_velocity(msg.velocity, 110)
                                    self.outport.send(df_msg)
                            if(self.plyr_ctrls['lead_fill']):
                                continue
                                role = ch_roles[msg.channel]
                                #if(len(self.alt_meas) > 1 and role[-3:] == '_ld'):
                                if(role[-3:] == '_ld'):
                                    logging.debug(len(self.alt_meas))
                                    lf_msg = msg.copy()
                                    lf_msg = self.alt_meas[self.counter[1]]
                                    self.counter[1] += 1
                                    if(self.counter[1] >= len(self.alt_meas)):
                                        self.counter[1] = 0
                                    self.outport.send(lf_msg)
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

    def make_riff(self, track):
        ticks_sum = 0
        msgs = []
        self.alt_meas = []
        if( not self.wt.scale):
            tmp_scale = [0,2,1,2,2,2,2,1]
        else:
            tmp_scale = self.wt.scale
        for i in range(36):
            rand_note = random.randint(0,len(tmp_scale)-1)
            steps = sum(tmp_scale[rand_note:-1])
            logging.debug('steps ' + str(steps))
            note = int(self.wt.key) + steps + random.randint(0,2)*12 
            len_note = [1,2,4,8,16]
            divisor = random.choice(len_note)
        
            time = int(self.ticks_per_beat/divisor)
            #logging.debug('note ' + str(self.wt.key))
            #logging.debug('time ' + str(time))
            #logging.debug('rand_note ' + str(rand_note))
        
            msg = Message('note_on', note=60, time=100)
            #msgs.append(msg.copy())
            #msgs.append(msg.copy(time = msg.time*2))
