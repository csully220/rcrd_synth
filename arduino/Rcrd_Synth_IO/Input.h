int rot_enc_a_chan = 2; //clk
int rot_enc_b_chan = 3; //dt
volatile byte aFlag = 0; // let's us know when we're expecting a rising edge on pinA to signal that the encoder has arrived at a detent
volatile byte bFlag = 0; // let's us know when we're expecting a rising edge on pinB to signal that the encoder has arrived at a detent (opposite direction to when aFlag is set)
volatile byte reading = 0; //somewhere to store the direct values we read from our interrupt pins before checking to see if we have moved a whole detent

//from Messages.h char* sw_names[] = {"12", "7", "AUTO", "START", "33","78", "LEFT", "RIGHT", "ROT ENC", "PROGRAM"};
byte sw_values[10] = {0,0,0,0,0,0,0,0,0,0};

//from Messages.h char* knob_names[] = {"KNOB1", "KNOB2", "KNOB3", "KNOB4", "KNOB5"};
byte knob_values[5] = {0,0,0,0,0};

static const int digital_pins[] = {42, 48, 46, 52, 44, 50, 4, 5};

int sw_rot_enc_chan = 13;
int sw_12_chan = 42;
int sw_33_chan = 44;
int sw_auto_chan = 46;
int sw_start_chan = 52;
int sw_78_chan = 50;
int sw_7_chan = 48;
int sw_program_chan = 40;
int sw_left_chan = 4;
int sw_right_chan = 5;

void initInput(){
	pinMode(rot_enc_a_chan, INPUT);
	pinMode(rot_enc_b_chan, INPUT);
	pinMode(sw_rot_enc_chan, INPUT);
	pinMode(sw_12_chan, INPUT_PULLUP);
	pinMode(sw_33_chan, INPUT_PULLUP);
	pinMode(sw_auto_chan, INPUT_PULLUP);
	pinMode(sw_start_chan, INPUT_PULLUP);
	pinMode(sw_78_chan, INPUT_PULLUP);
	pinMode(sw_7_chan, INPUT_PULLUP);
	pinMode(sw_program_chan, INPUT_PULLUP);
	pinMode(sw_left_chan, INPUT_PULLUP);
	pinMode(sw_right_chan, INPUT_PULLUP);
}

bool updateInput(){
  
  bool changed = false;
  byte temp;

  for(int i=0; i<=4; i++){
      temp = analogRead(i)/8.0;
      if(temp != knob_values[i]){
          knob_values[i] = temp;
          changed = true;
      }
  }
  
  for(int i=0; i<=7; i++){
      temp = !digitalRead(digital_pins[i]);
      if(temp != sw_values[i]){
          sw_values[i] = temp;
          changed = true;
      }
  }
  sw_values[8] = !digitalRead(sw_rot_enc_chan);
  return changed;
}
