import wolftones
import threading
import logging  
import curses

class RtGuiThread(threading.Thread):

    def __init__(self):
        super(RtGuiThread, self).__init__()
        self.name = 'RtGui'
        self.stoprequest = False

    def get_param(prompt_string):
        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, prompt_string)
        screen.refresh()
        input = screen.getstr(10, 10, 60)
        return input

    def run(self):
        logging.debug('Running GuiThread')
        global gi_knob0
        global gi_knob1
        global gi_knob2
        global gi_knob3
        global gi_knob4
        global gi_sw_12
        global gi_sw_7
        global gi_sw_auto
        global gi_sw_start
        global gi_sw_33
        global gi_sw_78
        global gi_sw_left
        global gi_sw_right
        global gi_synthmode
        global gi_ctrl_val_chg

        gi_knob0 = 0
        gi_knob1 = 0 
        gi_knob2 = 0 
        gi_knob3 = 0 
        gi_knob4 = 0 
        gi_sw_12 = 0 
        gi_sw_7 = 0 
        gi_sw_auto = 0 
        gi_sw_start = 0 
        gi_sw_33 = 0 
        gi_sw_78 = 0 
        gi_sw_left = 0 
        gi_sw_right = 0 
        gi_synthmode = 0 
        gi_ctrl_val_chg = 0

        gi_sw_12 = 0
        gi_playing = False
        gi_synthmode = 'DEFAULT'
        #global gi_sw_rotenc
        #global gi_sw_prog

        screen = curses.initscr()
        while self.stoprequest == False:
            try:

                screen.addstr(2, 4, 'GUI Inputs')
                screen.addstr(5, 4, '12     ' + str(gi_sw_12))
                screen.addstr(6, 4, '7      ' + str(gi_sw_7))
                screen.addstr(7, 4, 'AUTO   ' + str(gi_sw_auto))
                screen.addstr(8, 4, 'START  ' + str(gi_sw_start))
                screen.addstr(9, 4, '33     ' + str(gi_sw_33))
                screen.addstr(10, 4,'78     ' + str(gi_sw_78))
                screen.addstr(11, 4,'LEFT   ' + str(gi_sw_left))
                screen.addstr(12, 4,'RIGHT  ' + str(gi_sw_right))
                screen.addstr(13, 4,'KNOB0  ' + str(gi_knob0))
                screen.addstr(14, 4,'KNOB1  ' + str(gi_knob1))
                screen.addstr(15, 4,'KNOB2  ' + str(gi_knob2))
                screen.addstr(16, 4,'KNOB3  ' + str(gi_knob3))
                screen.addstr(17, 4,'KNOB4  ' + str(gi_knob4))

                screen.addstr(25, 4, 'RcrdSynth: ')

                curses.echo()
                s_raw = screen.getstr(25,15)
                screen.clear()
                toks = list(str.split(s_raw))
                #commands with no argument
                if(len(toks) == 1):
                    tok0 = toks[0]
                    if(tok0 == 'quit' or tok0 == 'q'):
                        self.stoprequest = True
                        screen.addstr(19, 4, 'quitting...')
                    if(tok0 == '12'):
                        gi_sw_12 = not gi_sw_12
                        gi_ctrl_val_chg = True
                    if(tok0 == '7'):
                        gi_sw_7 = not gi_sw_7
                        gi_ctrl_val_chg = True
                    if(tok0 == 'auto'):
                        gi_sw_auto = not gi_sw_auto
                        gi_ctrl_val_chg = True
                    if(tok0 == 'start'):
                        gi_sw_start = not gi_sw_start
                        gi_ctrl_val_chg = True
                    if(tok0 == '33'):
                        gi_sw_33 = not gi_sw_33
                        gi_ctrl_val_chg = True
                    if(tok0 == '78'):
                        gi_sw_78 = not gi_sw_78
                        gi_ctrl_val_chg = True
                    if(tok0 == 'right'):
                        gi_sw_right = not gi_sw_right
                        gi_ctrl_val_chg = True
                    if(tok0 == 'left'):
                        gi_sw_left = not gi_sw_left
                        gi_ctrl_val_chg = True

                    elif(tok0 == 'rt'):
                         syncmode = True
                         curses.noecho() 
                         curses.halfdelay(2)
                         while(syncmode):
                             char = screen.getch()        # This blocks (waits) until the time has elapsed,
                             screen.clear()                          # or there is input to be handled
                             if(char != curses.ERR):    # This is true if the user pressed something
                                 if(char == ord('q')):
                                     curses.nocbreak()
                                     syncmode = False
                                 if(char == ord(' ')):
                                     gi_playing = not gi_playing
                                     gi_ctrl_val_chg = True
                             else:  
                                 screen.addstr(12, 4, "Playing: " + str(gi_playing))
                if(len(toks) == 3): 
                    tok0 = toks[0]
                    tok1 = toks[1] 
                    tok2 = toks[2] 
                    if(tok0 == 'knob'):
                        if(tok1 in ['0', '1', '2', '3', '4']):
                            if(tok1 == '0'):
                                gi_knob0 = int(tok2)
                                gi_ctrl_val_chg = True
                            if(tok1 == '1'):
                                gi_knob1 = int(tok2)
                                gi_ctrl_val_chg = True
                            if(tok1 == '2'):
                                gi_knob2 = int(tok2)
                                gi_ctrl_val_chg = True
                            if(tok1 == '3'):
                                gi_knob3 = int(tok2)
                                gi_ctrl_val_chg = True
                            if(tok1 == '4'):
                                gi_knob4 = int(tok2)
                                gi_ctrl_val_chg = True

                '''
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
                '''    
            except:
                curses.echo()
                curses.endwin()
        curses.echo()
        curses.endwin()
        

#    def join(self, timeout=None):
        #self.stoprequest.set()
        #super(RtGuiThread, self).join(timeout) 

        '''
 
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
    '''
