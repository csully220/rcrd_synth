import wolftones
import threading
import logging  
import curses

class RtGuiThread(threading.Thread):

    _msg_mode_hlp = 'gui or io'
    _ctrl_src = 'gui'



    def __init__(self, q_gui):
        super(RtGuiThread, self).__init__()
        self.name = 'RtGui'
        self.stoprequest = threading.Event()
        self.out_q = q_gui
        self._is_ctrl_src = True

    def is_input_src():
        return self._is_ctrl_src

    def get_param(prompt_string):
        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, prompt_string)
        screen.refresh()
        input = screen.getstr(10, 10, 60)
        return input

    def join(self, timeout=None):
        self.stoprequest.set()
        super(RtGuiThread, self).join(timeout)

    def run(self):

        gi_knob0 = 0
        gi_knob1 = 0 
        gi_knob2 = 0 
        gi_knob3 = 0 
        gi_knob4 = 0 
        gi_sw_12 = False
        gi_sw_7 = False
        gi_sw_auto = False
        gi_sw_start = False
        gi_sw_33 = False
        gi_sw_78 = False
        gi_sw_left = False
        gi_sw_right = False
        gi_playing = False
        gi_synthmode = 'DEFAULT'

        try:
            screen = curses.initscr()
            while(not self.stoprequest.isSet()):
            #while(True):
                screen.addstr(1, 1, '*CONTROLS*')
                screen.addstr(3, 2, 'Playing: ' + str(gi_playing))
                screen.addstr(4, 2, '12     ' + str(gi_sw_12))
                screen.addstr(5, 2, '7      ' + str(gi_sw_7))
                screen.addstr(6, 2, 'AUTO   ' + str(gi_sw_auto))
                screen.addstr(7, 2, 'START  ' + str(gi_sw_start))
                screen.addstr(8, 2, '33     ' + str(gi_sw_33))
                screen.addstr(9, 2,'78     ' + str(gi_sw_78))
                screen.addstr(10, 2,'LEFT   ' + str(gi_sw_left))
                screen.addstr(11, 2,'RIGHT  ' + str(gi_sw_right))
                screen.addstr(4, 18,'KNOB0  ' + str(gi_knob0))
                screen.addstr(5, 18,'KNOB1  ' + str(gi_knob1))
                screen.addstr(6, 18,'KNOB2  ' + str(gi_knob2))
                screen.addstr(7, 18,'KNOB3  ' + str(gi_knob3))
                screen.addstr(8, 18,'KNOB4  ' + str(gi_knob4))
                screen.addstr(9, 18,'MODE  ' + str(gi_synthmode))
                screen.addstr(10, 18,'Input Src ' + str(self._ctrl_src))
    
                screen.addstr(14, 4, 'RcrdSynth#  ')
    
                curses.echo()

                s_raw = screen.getstr(14, 15)
                screen.clear()
    
                toks = list(str.split(s_raw))
                #commands with no argument
                if(len(toks) == 1):
                    tok0 = toks[0]
                    if(tok0 == 'quit' or tok0 == 'q'):
                        #self.stoprequest.set()
                        self.join()
                        logging.debug('quitting...')
                    if(tok0 == '12'):
                        gi_sw_12 = not gi_sw_12
                        self.out_q.put({'sw_12':gi_sw_12})
                    if(tok0 == '7'):
                        gi_sw_7 = not gi_sw_7
                        self.out_q.put({'sw_7':gi_sw_7})
                    if(tok0 == 'auto'):
                        gi_sw_auto = not gi_sw_auto
                        self.out_q.put({'sw_auto':gi_sw_auto})
                    if(tok0 == 'start'):
                        gi_sw_start = not gi_sw_start
                        self.out_q.put({'sw_start':gi_sw_start})
                    if(tok0 == '33'):
                        gi_sw_33 = not gi_sw_33
                        self.out_q.put({'sw_33':gi_sw_33})
                    if(tok0 == '78'):
                        gi_sw_78 = not gi_sw_78
                        self.out_q.put({'sw_78':gi_sw_78})
                    if(tok0 == 'left'):
                        gi_sw_left = not gi_sw_left
                        self.out_q.put({'sw_left':gi_sw_left})
                    if(tok0 == 'right'):
                        gi_sw_right = not gi_sw_right
                        self.out_q.put({'sw_right':gi_sw_right})

                    if(tok0 == 'p'):
                        gi_playing = not gi_playing
                        self.out_q.put({'playing':gi_playing})
                    if(tok0 == 'newsong'):
                        self.out_q.put({'command':tok0})

    
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
                                     self.out_q.put({'playing':gi_playing})
                             else:  
                                 screen.addstr(12, 4, "Playing: " + str(gi_playing))
    
                if(len(toks) == 2): 
                    tok0 = toks[0]
                    tok1 = toks[1] 
                    if(tok0 == 'knob0'):
                        gi_knob0 = int(tok1)
                        self.out_q.put({'knob0':gi_knob0})
                    if(tok0 == 'knob1'):
                        gi_knob1 = int(tok1)
                        self.out_q.put({'knob1':gi_knob1})
                    if(tok0 == 'knob2'):
                        gi_knob2 = int(tok1)
                        self.out_q.put({'knob2':gi_knob2})
                    if(tok0 == 'knob3'):
                        gi_knob3 = int(tok1)
                        self.out_q.put({'knob3':gi_knob3})
                    if(tok0 == 'knob4'):
                        gi_knob4 = int(tok1)
                        self.out_q.put({'knob4':gi_knob4})
                    if(tok0 == 'mode'):
                        if(tok1 == 'gui'):
                            self._is_ctrl_src = True
                            self._ctrl_src = tok1
                        if(tok1 == 'io'):
                            self._is_ctrl_src = False
                            self._ctrl_src = tok1
                        if(tok1 == '?'):
                            screen.addstr(15, 8, self._msg_mode_hlp)
        except:
            curses.echo()
            curses.endwin()
        curses.echo()
        curses.endwin()

