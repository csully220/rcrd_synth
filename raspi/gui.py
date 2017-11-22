import wolftones
import threading
import logging  
import curses

class GuiThread(threading.Thread):

    _msg_mode_hlp = 'gui or io'
    _ctrl_src = 'gui'
    _valid_sw_names = ['right', 'left', '78', '33', 'start', 'auto', '7', '12']
    _valid_knob_names = ['knob0', 'knob1', 'knob2', 'knob3', 'knob4']

    def __init__(self, _gui_ctrls):  #2nd arg was q_gui
        super(GuiThread, self).__init__()
        self.name = 'Gui'
        self.stoprequest = threading.Event()
        #self.out_q = q_gui
        self.gui_ctrls = _gui_ctrls
        self._is_ctrl_src = True
        self.mon_mode = False

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
        logging.debug('GUI joining...')
        self.stoprequest.set()
        super(GuiThread, self).join(timeout)

    def run(self):
   #     try:
            _val_chg = False
            screen = curses.initscr()
            while(not self.stoprequest.isSet()):

                self.refresh_screen(screen)
    
                screen.addstr(14, 4, 'RcrdSynth#  ')
                curses.echo()

                s_raw = screen.getstr(14, 15)
    
                toks = list(str.split(s_raw))
                #commands with no argument
                if(len(toks) == 1):
                    tok0 = toks[0]
                    if(tok0 == 'quit' or tok0 == 'q'):
                        self.gui_ctrls['cmd'] = 'POWEROFF'
                        _val_chg = True       
                        self.stoprequest.set()
                    if(tok0 == 'play' or tok0 == 'p'):
                        self.gui_ctrls['play'] = not self.gui_ctrls['play']
                        #logging.debug('val_chg play: ' + str(self.gui_ctrls['play']))
                        _val_chg = True
                    if(tok0 == 'newsong'):
                        self.gui_ctrls['cmd'] = 'NEWSONG'
                        _val_chg = True
                    #override the switches
                    if(tok0 in self._valid_sw_names):
                        self.gui_ctrls['sw_' + tok0] = not self.gui_ctrls['sw_' + tok0]
                        _val_chg = True
                    # this needs to be rethought
                    if(tok0 == 'm'):
                         self.mon_mode = True
                         curses.noecho() 
                         curses.halfdelay(2)
                         
                         while(self.mon_mode):
                             char = screen.getch()        # This blocks (waits) until the time has elapsed,
                             #TODO hook up ctrl_chgd to detect hardware control changes
                             #     so screen isn't constantly refreshing
                             ctrl_chgd = True
                             if(ctrl_chgd):
                                 self.refresh_screen(screen)                  # or there is input to be handled
                             if(char != curses.ERR):    # This is true if the user pressed something
                                 if(char == ord('m')):
                                     curses.nocbreak()
                                     self.mon_mode = False

                if(len(toks) == 2): 
                    tok0 = toks[0]
                    tok1 = toks[1]
                    if(tok0 in self._valid_knob_names and int(tok1) >= 0 and int(tok1) <= 127):
                        self.gui_ctrls[tok0] = int(tok1)
                        _val_chg = True
                    if(tok0 == 'load'):
                        self.gui_ctrls['cmd'] = 'LOADSONG'
                        self.gui_ctrls['songfile'] = tok1            
                        _val_chg = True
                if(_val_chg == True):
                    self.gui_ctrls['val_chg'] = True
                    _val_chg = False
                 #   lock.acquire()
                 #   try:
                 #       self.gui_ctrls['val_chg'] = True
                 #   finally:
                 #       lock.release()

        #except:
            curses.echo()
            curses.endwin()

    def refresh_screen(self, screen):
        screen.clear()
        screen.addstr(1, 1, '*RECORD PLAYER SYNTH CONTROLS*')
        screen.addstr(3, 2, 'Playing: ' + str(self.gui_ctrls['play']))
        screen.addstr(4, 2, '12     ' + str(self.gui_ctrls['sw_12']))
        screen.addstr(5, 2, '7      ' + str(self.gui_ctrls['sw_7']))
        screen.addstr(6, 2, 'AUTO   ' + str(self.gui_ctrls['sw_auto']))
        screen.addstr(7, 2, 'START  ' + str(self.gui_ctrls['sw_start']))
        screen.addstr(8, 2, '33     ' + str(self.gui_ctrls['sw_33']))
        screen.addstr(9, 2, '78     ' + str(self.gui_ctrls['sw_78']))
        screen.addstr(10, 2,'LEFT   ' + str(self.gui_ctrls['sw_left']))
        screen.addstr(11, 2,'RIGHT  ' + str(self.gui_ctrls['sw_right']))
        screen.addstr(4, 18,'KNOB0  ' + str(self.gui_ctrls['knob0']))
        screen.addstr(5, 18,'KNOB1  ' + str(self.gui_ctrls['knob1']))
        screen.addstr(6, 18,'KNOB2  ' + str(self.gui_ctrls['knob2']))
        screen.addstr(7, 18,'KNOB3  ' + str(self.gui_ctrls['knob3']))
        screen.addstr(8, 18,'KNOB4  ' + str(self.gui_ctrls['knob4']))
        screen.addstr(9, 18,'MODE   ' + str(self.gui_ctrls['mode']))
        screen.addstr(10,18,'monitor mode (m)  ' + str(self.mon_mode))
