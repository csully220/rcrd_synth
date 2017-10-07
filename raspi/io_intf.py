import serial
import time

class IoIntfThread:

#define BM_NONE   0x00
#define BM_ISO_CH 0x02
#define BM_DLSONG 0x03
#define BM_PWROFF 0xFE

    def __init__(self):
        super(IoIntfThread, self).__init__()
        self.name = 'IoIntf'
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.switch = [0 for i in range(8)]
        self.knob = [0,0,0,0,0]
        self.msg_byte = b'0x00'
        self.modes = {b'\x00':'DEFAULT', b'\xFE':'PWROFF', b'\x02':'ISOL_CH', b'\x03':'DL_SONG'}
        self.stoprequest = threading.Event()

    def get_readline(self):
        return self.ser.readline()

    def unpack_serial(self):
        try:
            tmp = self.ser.readline().strip()
            if(ord(tmp[0]) == 255):
                self.knob[4] = ord(tmp[1])
                self.knob[3] = ord(tmp[2])
                self.knob[2] = ord(tmp[3])
                self.knob[1] = ord(tmp[4])
                self.knob[0] = ord(tmp[5])
                sw = ord(tmp[6])
                for r in range(8):
                    if(sw & (int('00000001') << r)):
                        self.switch[r] = 1 
                    else:
                        self.switch[r] = 0
                #self.msg_byte = ord(tmp[7])
                self.msg_byte = tmp[7]
                return True
        except:
            self.ser.reset_input_buffer()
            return False

    def get_switch(self, idx = 0):
        if idx >= 0 and idx <=7:
            return self.switch[idx]

    def get_knob(self, idx = 0):
        if idx >= 0 and idx <=4:
            return self.knob[idx]

    def get_mode(self):
        return self.modes[self.msg_byte]
        #return self.msg_byte

    def close_port(self):
        try:
            self.ser.close()
        except:
            pass


    def run():
        global io_knob0
        global io_knob1
        global io_knob2
        global io_knob3
        global io_knob4
        global io_sw_12
        global io_sw_7
        global io_sw_auto
        global io_sw_start
        global io_sw_33
        global io_sw_78
        global io_sw_left
        global io_sw_right
        #global io_sw_rotenc
        #global io_sw_prog
        global io_ctrl_val_chg
        global io_playing
        global io_synthmode
    
        while(not self.stoprequest.isSet()):
            if(self.unpack_serial()):
                logging.debug('Getting new inputs...')
    
                io_knob4 = self.get_knob(4)/10
                io_knob3 = self.get_knob(3)/10
                io_knob2 = self.get_knob(2)/10
                io_knob1 = self.get_knob(1)/10
                io_knob0 = self.get_knob(0)/10
    
                io_sw_12 = self.get_switch(7)
                io_sw_7  = self.get_switch(6)
                io_sw_auto = self.get_switch(5)
                io_sw_start = self.get_switch(4)
                io_sw_33 = self.get_switch(3)
                io_sw_78 = self.get_switch(2)
                io_sw_left = self.get_switch(1)
                io_sw_right = self.get_switch(0)
    
                tmp_mode = self.get_mode()
    
                if(io_synthmode != tmp_mode):
                    io_synthmode = tmp_mode
    
                #if(synthmode == 'PWROFF'):
                #    os.system('sudo poweroff')
                io_ctrl_val_chg = True
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
