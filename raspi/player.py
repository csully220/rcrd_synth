import mido

def play_midi():
# get the portname (system specific)
#names = str(mido.get_output_names())
#logging.debug(names)
#ports = names.split(',')
#logging.debug(ports)
#sobj = re.search(r'Synth input port \(\d*:0\)', ports[0], flags=0)
#sobj = re.search(r'Midi Through Port-0 \(\d*:0\)', names, flags=0)
#logging.debug(sobj)
#portname = sobj.group()

    portname = 'Midi Through:Midi Through Port-0 14:0'
    with mido.open_output(portname, autoreset=True) as output:
        was_playing = False
        channels_in_use = []
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
