import mido
import threading
import re
import random

class PlayerThread(threading.Thread):
    
    def __init__(self, s_env, s_filepath):
        super(PlayerThread, self).__init__()
        self.stoprequest = threading.Event()
        self.playing = False
        self.songfile = s_filepath
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
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)

    def start(self):
        self.playing == True

    def stop(self):
        self.playing == False

    def change_song(self, filepath):
        self.stop()
        sleep(0.3)
        self.songfile = filepath

    def run(self):

        global pl_knob0
        global pl_knob1
        global pl_knob2
        global pl_knob3
        global pl_knob4
        global pl_sw_12
        global pl_sw_7
        global pl_sw_auto
        global pl_sw_start
        global pl_sw_33
        global pl_sw_78
        global pl_sw_left
        global pl_sw_right
        #pl_sw_rotenc=0
        #pl_sw_prog=0
        global pl_synthmode
        global pl_playing
        global pl_ctrl_val_chg

        was_playing = False
        #channels_in_use = []
        try:
            while not self.stoprequest.isSet():
                while(self.playing == True or sw_right):
                    was_playing = True
                    for msg in MidiFile(self.songfile).play():
                        if(msg.type == 'prog'):
                            channels_in_use.append(msg.channel)
    #--------------------  MODIFY MIDI MESSAGES ON THE FLY  ------------------------
                        if(ctrl_val_chg == True):
                            if(msg.type == 'note_on'):
                                if(sw_33 and msg.channel == knob1):
                                    msg.note += 7
                                if(synthmode == 'ISO_CH'):
                                    if(msg.channel != knob0):
                                        msg.velocity = 0
                                if(sw_12):
                                    if(msg.channel == 9):
                                        msg.velocity = 0
                                if(sw_7):
                                    if(msg.channel == 9):
                                        msg.velocity = 127
        ##################### SEND MIDI MESSAGE #######################################
                        self.outport.send(msg)
                        if(playing == False):
                            break
                if(was_playing == True):
                    self.outport.reset()
                    was_playing = False
        except KeyboardInterrupt:
            print()
        self.outport.reset()
