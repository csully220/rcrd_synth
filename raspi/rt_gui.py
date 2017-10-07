import wolftones
import threading
import curses

class RtGuiThread(threading.Thread):

    def __init__(self):
        super(RtGuiThread, self).__init__()
        self.playing = False
        self.stoprequest = threading.Event()
        self.synthmode = None

    def get_param(prompt_string):
        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, prompt_string)
        screen.refresh()
        input = screen.getstr(10, 10, 60)
        return input

    def run(self):
        x = None
        screen = curses.initscr()
        while x != ord('q') and not self.stoprequest.isSet():
            try:
                screen.clear()
                screen.border(0)
                screen.addstr(2, 40, "Mode: " + str(self.synthmode))
                screen.addstr(3, 40, "Space to start/stop...")
                screen.addstr(7, 40, "Playing: " + str(self.playing))
                screen.addstr(8, 40, "e - Edit Params")
                screen.addstr(9, 40, "s - select song")
                screen.addstr(10, 40, "n - new song")
                screen.addstr(11, 40, "d - display WolfTones params")
                screen.addstr(12, 40, "c - display control inputs")
                screen.addstr(13, 40, "q - Quit")
        
                screen.refresh()
                curses.noecho()
        
                x = screen.getch()

                if x == ord(' '):
                    self.playing = not self.playing
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
        

    def join(self, timeout=None):
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
