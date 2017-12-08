import serial
import time
import threading
import logging

class IoIntfThread(threading.Thread):

    #MODES
    #define MSG_DEFAULT 0x00 // 1
    #define MSG_ISO_CH  0x01 // 2

    #COMMANDS
    #define MSG_NONE    0xC0 // 192
    #define MSG_PWROFF  0xC1 // 193
    #define MSG_DLSONG  0xC2 // 194

    global io_ctrls

    sw_names = ['sw_right', 'sw_left', 'sw_78', 'sw_33', 'sw_start', 'sw_auto', 'sw_7', 'sw_12']
    knob_names = ['knob0', 'knob1', 'knob2', 'knob3', 'knob4']
    modes = ['DEFAULT', 'ISOL_CH']
    commands = ['NONE', 'PWROFF', 'NEWSONG']

    def __init__(self, _io_ctrls):
        super(IoIntfThread, self).__init__()
        self.name = 'IoIntf'
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.stoprequest = threading.Event()
        self.io_ctrls = _io_ctrls

    def get_readline(self):
        return bytearray(self.ser.readline())

    def join(self, timeout=None):
        logging.debug('Goodbye IO thread!')
        self.stoprequest.set()
        time.sleep(10)
        self.close_port()
        super(IoIntfThread, self).join(timeout)

    def unpack_serial(self):
        try:
            tmp = self.ser.readline().strip()
            if(ord(tmp[0]) == 255):
                rtn = True
                self.io_ctrls['knob4'] = ord(tmp[1])
                self.io_ctrls['knob3'] = ord(tmp[2])
                self.io_ctrls['knob2'] = ord(tmp[3])
                self.io_ctrls['knob1'] = ord(tmp[4])
                self.io_ctrls['knob0'] = ord(tmp[5])
                #logging.debug('getting knob input')
                sw = ord(tmp[6])
                #logging.debug(str(sw))
                for r in range(8):
                    #logging.debug(str(self.sw_names[r]))
                    if(sw & (int('00000001') << r)):
                        self.io_ctrls[self.sw_names[r]] = True
                    else:
                        self.io_ctrls[self.sw_names[r]] = False
                mb = ord(tmp[7])
                #logging.debug(str(mb))
                if(mb < 192):
                    #logging.debug('msg byte is something')
                    self.io_ctrls['mode'] = self.modes[mb]
   
                elif(mb >= 192):
                    self.io_ctrls['cmd'] = self.commands[mb - 192]
                logging.debug(str(mb))

                return rtn 
        except:
            self.ser.reset_input_buffer()
            return False

    def close_port(self):
        try:
            self.ser.close()
        except:
            pass

    def run(self):
        prev_knob = [0 for i in range(5)]
        prev_sw = [0 for i in range(8)]
        prev_mode = 'DEFAULT'
        logging.debug('Running IO thread...')
        while(not self.stoprequest.isSet()):
            if(self.unpack_serial()):
                self.io_ctrls['val_chg'] = True 
                
                for i in range(5):
                    if(self.io_ctrls[self.knob_names[i]] != prev_knob[i]):
                        prev_knob[i] = self.io_ctrls[self.knob_names[i]]

                for i in range(8):
                    if(self.io_ctrls[self.sw_names[i]] != prev_sw[i]):
                        prev_sw[i] = self.io_ctrls[self.sw_names[i]]

                if(prev_mode != self.io_ctrls['cmd']):
                    prev_mode = self.io_ctrls['cmd']

                if(prev_mode != self.io_ctrls['mode']):
                    prev_mode = self.io_ctrls['mode']

            time.sleep(0.01)
