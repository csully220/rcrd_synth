import serial

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
