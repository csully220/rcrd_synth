

//initialize the serial output buffer and set the start byte. No other byte can be 0xFF

//output_buf[0]   START BYTE
//output_buf[1-5] KNOBS
//output_buf[6]   SWITCHES
//output_buf[7]   MESSAGE BYTE

byte output_buf[8] = {0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0};



void packKnobData(){
  for(int i = 0; i <= 4; i++){
    output_buf[i+1] = byte(knob_values[i]);
  }
}

void packSwData(){
  output_buf[6] = 0;
  //pack the switch position data
  for(int i=0; i<=6; i++) {
    if(sw_values[i] > 0)
      output_buf[6] |= 1;
    output_buf[6] <<= 1;
  }
  if(sw_values[7] > 0)
    output_buf[6] |= 1;
    output_buf[6] = byte(output_buf[6]);
}

void packMsgByte(byte msg){
  output_buf[7] = msg;
}

void packMsgByte(){
  //output_buf[7] = msg;
  output_buf[7] = byte(0xC0);
}
//"12", "7", "AUTO", "START", "33","78", "LEFT", "RIGHT", "ROT ENC", "PROGRAM"
// MSB  254    128      64     32   16     8        4         2         LSB
//    0    80    40       20     10    8     4        2                     




