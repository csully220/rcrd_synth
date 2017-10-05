
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
