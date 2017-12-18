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
    commands = ['NONE', 'POWEROFF', 'NEWSONG']

    def __init__(self, _io_ctrls):
        super(IoIntfThread, self).__init__()
        self.name = 'IoIntf'
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.stoprequest = threading.Event()
        self.io_ctrls = _io_ctrls
        self.tmp_ctrls = {}
        self.tmp_ctrls['cmd'] = 'NONE'
        self.last_cmd = 'NONE'

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
                self.tmp_ctrls['knob4'] = ord(tmp[1])
                self.tmp_ctrls['knob3'] = ord(tmp[2])
                self.tmp_ctrls['knob2'] = ord(tmp[3])
                self.tmp_ctrls['knob1'] = ord(tmp[4])
                self.tmp_ctrls['knob0'] = ord(tmp[5])
                #logging.debug('getting knob input')
                sw = ord(tmp[6])
                #logging.debug(str(sw))
                for r in range(8):
                    #logging.debug(str(self.sw_names[r]))
                    if(sw & (int('00000001') << r)):
                        self.tmp_ctrls[self.sw_names[r]] = True
                        #logging.debug(self.sw_names[r] + str(self.tmp_ctrls[self.sw_names[r]]))
                    else:
                        self.tmp_ctrls[self.sw_names[r]] = False
                mb = ord(tmp[7])
                #logging.debug(str(mb))
   
                self.tmp_ctrls['cmd'] = self.commands[mb]

                #logging.debug('msg byte: ' + str(mb))
                return True
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
        prev_cmd = 'NONE'

        logging.debug('Running IO thread...')
        while(not self.stoprequest.isSet()):
            if(self.unpack_serial()):
                #logging.debug('unpack serial')
                #chgd = False
                self.io_ctrls['val_chg'] = True
                
                for i in range(5):
                    if(self.tmp_ctrls[self.knob_names[i]] != prev_knob[i]):
                        self.io_ctrls[self.knob_names[i]] = self.tmp_ctrls[self.knob_names[i]]
                        prev_knob[i] = self.io_ctrls[self.knob_names[i]]
                        #chgd = True

                for i in range(8):
                    if(self.tmp_ctrls[self.sw_names[i]] != prev_sw[i]):
                        self.io_ctrls[self.sw_names[i]] = self.tmp_ctrls[self.sw_names[i]]
                        prev_sw[i] = self.io_ctrls[self.sw_names[i]]
                        #chgd = True

                if(self.tmp_ctrls['cmd'] != prev_cmd):
                    self.io_ctrls['cmd'] = self.tmp_ctrls['cmd']
                    prev_cmd = self.tmp_ctrls['cmd']
                    #chgd = True

                #logging.debug(self.io_ctrls['cmd'])
                #self.io_ctrls['val_chg'] = chgd

            time.sleep(0.01)
