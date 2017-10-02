#!/usr/bin/env python
import os
import datetime
import random
import threading
import time
import logging
import curses
import mido  
from mido import MidiFile
import re  
from wolftones import *
from intf import *

LOG_FILENAME = 'log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w', format='(%(threadName)-10s) %(message)s')

io = IOInterface()
knob0=0 
knob1=0
knob2=0 
knob3=0
sw_12=0
sw_7=0
sw_auto=0
sw_start=0
sw_33=0
sw_78=0
sw_left=0
sw_right=0
sw_rotenc=0
sw_prog=0  
ctrl_val_chg = False
synthmode = 'DEFAULT'

#------------------------------------------------------------------------------- PLAYER THREAD ----------------------------------
def play_midi():
    was_playing = False
    channels_in_use = []
    with mido.open_output(portname, autoreset=True) as output:
        try:
            while(1):
                while(playing == True or sw_right):
                    was_playing = True
                    for msg in MidiFile(song_file).play():
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
                        output.send(msg)
                        if(playing == False):
                            break    
                if(was_playing == True):
                    output.reset()
                    was_playing = False
        except KeyboardInterrupt:
            print()
    output.reset()
################################################################################# END PLAYER THREAD ##############################
            
def get_param(prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    input = screen.getstr(10, 10, 60)
    return input

#------------------------------------------------------------------------------- INPUTS THREAD --------------------------------------
def update_control_inputs():

    global knob0
    global knob1
    global knob2
    global knob3
    global knob4
    global sw_12
    global sw_7
    global sw_auto
    global sw_start
    global sw_33
    global sw_78
    global sw_left
    global sw_right
    global sw_rotenc
    global sw_prog
    global ctrl_val_chg
    global playing
    global synthmode   

    while(1):
        if(io.unpack_serial()):
            logging.debug('Getting new inputs...')

            knob4 = io.get_knob(4)/10
            knob3 = io.get_knob(3)/10 
            knob2 = io.get_knob(2)/10 
            knob1 = io.get_knob(1)/10
            knob0 = io.get_knob(0)/10

            sw_12 = io.get_switch(7)
            sw_7  = io.get_switch(6) 
            sw_auto = io.get_switch(5)
            sw_start = io.get_switch(4)
            sw_33 = io.get_switch(3)
            sw_78 = io.get_switch(2)
            sw_left = io.get_switch(1)
            sw_right = io.get_switch(0)

            tmp_mode = io.get_mode()
            if(synthmode != tmp_mode):
                synthmode = tmp_mode

            if(synthmode == 'PWROFF'):
                os.system('sudo poweroff')

            ctrl_val_chg = True

            #if(sw_right):
                #playing = True
            #else:
                #playing = False

            #logging.debug(str(knob4))
            #logging.debug(str(knob3))
            #logging.debug(str(knob2))
            #logging.debug(str(knob1))
            #logging.debug(str(knob0))
            #logging.debug('12     ' + str(sw_12))
            #logging.debug('7      ' + str(sw_7))
            #logging.debug('auto   ' + str(sw_auto))
            #logging.debug('start  ' + str(sw_start))
            #logging.debug('33     ' + str(sw_33))
            #logging.debug('78     ' + str(sw_78))
            #logging.debug('left   ' + str(sw_left))
            #logging.debug('right  ' + str(sw_right))
        else: 
            #sleep briefly so we don't eat up processor
            time.sleep(0.03)
############################################################################### END INPUTS THREAD ###################################

################################################### INITIALIZE ############################
# flag for starting/stopping MIDI file playback
playing = False

# get the portname (system specific)
names = str(mido.get_output_names())
ports = names.split(',')
sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
portname = sobj.group()

# threads
thr_plyr = threading.Thread(name='PLAYER', target=play_midi)
thr_plyr.setDaemon(True)
thr_inpts = threading.Thread(name='INPUTS', target=update_control_inputs)
thr_inpts.setDaemon(True)
thr_plyr.start()
thr_inpts.start()
################################################# END INITIALIZE ############################

#------------------------------------------------MAIN LOOP-----------------------------------
song_file = 'songs/warriorcatssong.mid'
x = 0
wt = WolfTones()


while x != ord('q'):

    try:
        screen = curses.initscr()
        screen.clear()
        screen.border(0)
        screen.addstr(2, 40, "Mode: " + str(synthmode))
        screen.addstr(3, 40, "Space to start/stop...")
        screen.addstr(7, 40, "Playing: " + str(playing))
        screen.addstr(8, 40, "e - Edit Params")
        screen.addstr(9, 40, "s - select song")
        screen.addstr(10, 40, "n - new song")
        screen.addstr(11, 40, "d - display WolfTones params")
        screen.addstr(12, 40, "c - display control inputs")
        screen.addstr(13, 40, "q - Quit")

        screen.refresh()
        curses.noecho()

        #handle special commands for synthmode
        #if(synthmode == 'DEFAULT'):
        x = screen.getch()

        if x == ord('d'):
            screen.addstr(2, 2, 'Wolfram Tones Parameters')
            screen.addstr(5, 2, '1. Genre:      ' + str(wt.params['genre']))
            screen.addstr(6, 2, '2. Rule Type:  ' + str(wt.params['rule_type']))
            screen.addstr(7, 2, '3. Rule:       ' + str(wt.params['rule']))
            screen.addstr(8, 2, '4. Boundaries: ' + str(wt.params['cyc_bdrs']))
            screen.addstr(9, 2, '5. Seed:       ' + str(wt.params["seed"]))
            screen.addstr(10, 2,'6. Duration    ' + str(wt.params["duration"]))
            screen.addstr(11, 2,'7. Tempo, BPM  ' + str(wt.params["bpm"]))
            screen.addstr(12, 2,'8. Scale       ' + str(wt.params["scale"]))
            screen.addstr(13, 2,'9. Pitch       ' + str(wt.params["pitch"]))
            screen.addstr(14, 2,'10. Inst 1      ' + str(wt.params["inst_1"]))
            screen.addstr(15, 2,'11. Role 1      ' + str(wt.params["role_1"]))
            screen.addstr(16, 2,'12. Inst 2      ' + str(wt.params["inst_2"]))
            screen.addstr(17, 2,'13. Role 2      ' + str(wt.params["role_2"]))
            screen.addstr(18, 2,'14. Inst 3      ' + str(wt.params["inst_3"]))
            screen.addstr(19, 2,'15. Role 3      ' + str(wt.params["role_3"]))
            screen.addstr(20, 2,'16. Inst 4      ' + str(wt.params["inst_4"]))
            screen.addstr(21, 2,'17. Role 4      ' + str(wt.params["role_4"]))
            screen.addstr(22, 2,'16. Inst 5      ' + str(wt.params["inst_5"]))
            screen.addstr(23, 2,'17. Role 5      ' + str(wt.params["role_5"]))
            screen.addstr(24, 2,'18. Percussion  ' + str(wt.params["perc"]))
            screen.move(25, 2)
            screen.refresh()
            curses.noecho()
            screen.getch()
    
        if x == ord('c'):
            screen.addstr(2, 2, 'Control Inputs')
            screen.addstr(5, 2, '12             ' + str(sw_12))
            screen.addstr(6, 2, '7              ' + str(sw_7))
            screen.addstr(7, 2, 'AUTO           ' + str(sw_auto))
            screen.addstr(8, 2, 'START          ' + str(sw_start))
            screen.addstr(9, 2, '33             ' + str(sw_33))
            screen.addstr(10, 2,'78             ' + str(sw_78))
            screen.addstr(11, 2,'LEFT           ' + str(sw_left))
            screen.addstr(12, 2,'RIGHT          ' + str(sw_right))
            screen.addstr(13, 2,'KNOB1          ' + str(knob0))
            screen.addstr(14, 2,'KNOB2           ' + str(knob1))
            screen.addstr(15, 2,'KNOB3           ' + str(knob2))
            screen.addstr(16, 2,'KNOB4           ' + str(knob3))
            screen.addstr(17, 2,'KNOB5           ' + str(knob4))
            screen.refresh()
            curses.noecho()
            screen.getch()
    
        if x == ord(' '):
            playing = not playing
    
        if x == ord('s'):
            curses.echo()
            song_file = 'songs/' + get_param("Choose MIDI file...") + '.mid'
    
        if x == ord('n') or synthmode == 'DLSONG':
            try:
                response = wt.send_url_request()
                logging.debug('MIDI file requested from ' + wt.nkm_encoded_url())
                if(response.content):
                    logging.debug('Got a new song from Wolftones')
                    curses.echo()
                    #tmp = 'songs/' + get_param("Enter song filename: ") + '.mid'
                    tmp = 'songs/song' + '{:%m-%d-%H:%M}'.format(datetime.datetime.now()) + '.mid'
                    with open(tmp, 'w+') as f:
                        f.write(response.content)
                    curses.noecho()
                    song_file = tmp
            except:
                song_file = 'songs/warriorcatssong.mid'
            synthmode = 'DEFAULT' 
        if x == ord('e'):
            screen.addstr(25, 2, 'Make selection ')
            curses.echo()
            x = screen.getstr(25,18)
    
            if x == str(1):
                tmp = get_param("Set genre: ")
                #wt.set_param(key='genre', value=tmp)
                wt.set_genre(genre=tmp)
            if x == str(2):
                tmp = get_param("Set rule type: ")
                wt.set_param(key='rule_type', value=tmp)
            if x == str(3):
                tmp = get_param("Set rule: ")
                wt.set_param(key='rule', value=tmp)
            if x == str(5):
                tmp = get_param("Set seed: ")
                wt.set_param(key='seed', value=tmp)
            if x == str(6):
                tmp = get_param("Set duration: ")
                wt.set_param(key='duration', value=tmp)
            if x == str(7):
                tmp = get_param("Set BPM: ")
                wt.set_param(key='bpm', value=tmp)
            if x == str(8):
                tmp = get_param("Set scale: ")
                wt.set_param(key='scale', value=tmp)
    except KeyboardInterrupt:
        curses.echo()
        curses.endwin()
        io.close_port()
    except:
        curses.echo()
        curses.endwin()
        io.close_port()
curses.endwin()
io.close_port()

################################################# MAIN LOOP ###################################
