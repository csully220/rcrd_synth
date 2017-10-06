import serial
import time

knob0=0
knob1=0
knob2=0
knob3=0
sw_12=0
sw_7=0
sw_auto=0
sw_start=0
sw_33=0
sw_78=0
sw_left=0
sw_right=0
sw_rotenc=0
sw_prog=0
ctrl_val_chg = False
synthmode = 'DEFAULT'

class IOInterface:

#define BM_NONE   0x00
#define BM_ISO_CH 0x02
#define BM_DLSONG 0x03
#define BM_PWROFF 0xFE

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.switch = [0 for i in range(8)]
        self.knob = [0,0,0,0,0]
        self.msg_byte = b'0x00'
        self.modes = {b'\x00':'DEFAULT', b'\xFE':'PWROFF', b'\x02':'ISOL_CH', b'\x03':'DL_SONG'}
        self.io = IOInterface()

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

    def update_control_inputs():
    
        global knob0
        global knob1
        global knob2
        global knob3
        global knob4
        global sw_12
        global sw_7
        global sw_auto
        global sw_start
        global sw_33
        global sw_78
        global sw_left
        global sw_right
        global sw_rotenc
        global sw_prog
        global ctrl_val_chg
    
    #   global playing
        global synthmode
    
        while(1):
            if(io.unpack_serial()):
                logging.debug('Getting new inputs...')
    
                knob4 = self.get_knob(4)/10
                knob3 = self.get_knob(3)/10
                knob2 = self.get_knob(2)/10
                knob1 = self.get_knob(1)/10
                knob0 = self.get_knob(0)/10
    
                sw_12 = self.get_switch(7)
                sw_7  = self.get_switch(6)
                sw_auto = self.get_switch(5)
                sw_start = self.get_switch(4)
                sw_33 = self.get_switch(3)
                sw_78 = self.get_switch(2)
                sw_left = self.get_switch(1)
                sw_right = self.get_switch(0)
    
                tmp_mode = self.get_mode()
    
                if(synthmode != tmp_mode):
                    synthmode = tmp_mode
    
                #if(synthmode == 'PWROFF'):
                #    os.system('sudo poweroff')
                ctrl_val_chg = True
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
