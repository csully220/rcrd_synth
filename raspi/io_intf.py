import serial
import time
import threading
import logging

class IoIntfThread(threading.Thread):

#define NONE   0x00
#define ISO_CHNL 0x02
#define NEWSONG 0x03
#define POWEROFF 0xFE

    sw_names = ['sw_right', 'sw_left', 'sw_78', 'sw_33', 'sw_start', 'sw_auto', 'sw_7', 'sw_12']
    knob_names = ['knob0', 'knob1', 'knob2', 'knob3', 'knob4']

    def __init__(self, q_io, io_ctrls):
        super(IoIntfThread, self).__init__()
        self.name = 'IoIntf'
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.modes = {b'\x00':'DEFAULT', b'\x01':'ISOL_CH'}
        self.commands = {b'\xC0':'NONE', b'\xC1':'PWROFF', b'\xC2':'NEWSONG'}
        self.stoprequest = threading.Event()
        self.q_io = q_io
        self.io_ctrls = io_ctrls

    def get_readline(self):
        return self.ser.readline()

    def join(self, timeout=None):
        logging.debug('IO joining ..')
        self.stoprequest.set()
        super(IoIntfThread, self).join(timeout)

    def unpack_serial(self):
        try:
            tmp = self.ser.readline().strip()
            if(ord(tmp[0]) == 255):
                self.io_ctrls['knob4'] = ord(tmp[1])/10
                self.io_ctrls['knob3'] = ord(tmp[2])/10
                self.io_ctrls['knob2'] = ord(tmp[3])/10
                self.io_ctrls['knob1'] = ord(tmp[4])/10
                self.io_ctrls['knob0'] = ord(tmp[5])/10
                sw = ord(tmp[6])
                for r in range(8):
                    if(sw & (int('00000001') << r)):
                        self.io_ctrls[sw_names[r]] = True
                    else:
                        self.io_ctrls[sw_names[r]] = False
                #self.msg_byte = ord(tmp[7])
                if(ord(tmp[7]) >= b'\xC0'):
                    self.io_ctrls['command'] = self.commands[ord(tmp[7])]
                if(ord(tmp[7]) < b'\xC0'):
                    self.io_ctrls['synthmode'] = self.modes[ord(tmp[7])]
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
        prev_sw = [0 for i in range(9)]
        prev_mode = 'DEFAULT'
        io_ctrl_val_chg = False
        logging.debug('Running IO thread...')
        while(not self.stoprequest.isSet()):
            logging.debug('Getting new inputs...')
            if(self.unpack_serial()):
                logging.debug('Getting new inputs...')
                '''
                for i in range(5):
                    if(self.io_ctrls[knob_names[i]] != prev_knob[i]):
                        prev_knob[i] = self.io_ctrls[knob_names[i]]
                        io_ctrl_val_chg = True

                for i in range(9):
                    if(self.io_ctrls[sw_names[i]] != prev_sw[i]):
                        prev_sw[i] = self.io_ctrls[sw_names[i]]
                        io_ctrl_val_chg = True


                if(prev_mode != self.io_ctrls['command']):
                    prev_mode = self.io_ctrls['command']
                    io_ctrl_val_chg = True

                if(prev_mode != self.io_ctrls['synthmode']):
                    prev_mode = self.io_ctrls['synthmode']
                    io_ctrl_val_chg = True

                self.io_ctrls['ctrl_val_chg'] = io_ctrl_val_chg 
                '''
