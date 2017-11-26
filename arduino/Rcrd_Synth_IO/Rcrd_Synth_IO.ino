
#include "Input.h"
#include "Comms.h"
#include "Menus.h"

int rcbl = 999; //rotary encoder bank limit
int rot_enc_ctr = 0;
int rot_enc_ctr_last = 0;
int sw_val_last;
bool msg_ready = false;
bool rot_enc_was_pressed;

void initInput();
bool updateInput();
void rotEncMovedLt();
void rotEncMovedRt();

SerLCD red_lcd(Serial1,16,2);          //RED ON BLACK LCD
LiquidCrystal_I2C blue_lcd(0x27,20,4); //BLUE ON WHITLE LCD
Menus menus(red_lcd, blue_lcd);

void setup()
{
  analogReference(EXTERNAL);
  attachInterrupt(0, rotEncMovedLt, RISING);
  attachInterrupt(1, rotEncMovedRt, RISING);
  
  Serial.begin(9600);
  Serial1.begin(9600);

  menus.initRed();
  menus.initBlue();
  initInput();
}
/*********************************************************/
void loop() {
  
  if(updateInput() || msg_ready == true){
  
      menus.dispKnobVals(knob_values);
      
      packKnobData();
      packSwData();
      packMsgByte(); 
      msg_ready = false;
      
      for(int i=0; i<=7; i++){
          Serial.write(output_buf[i]);
      }
      Serial.print("\n");
      
      if(sw_values[6])
          menus.dispTopMenu();
  }  

  if(sw_values[8] && rot_enc_was_pressed == false){
      rot_enc_was_pressed = true;
      menus.select();
      delay(400);
  } else {
      rot_enc_was_pressed = false;
  }
          
  if(rot_enc_ctr < rot_enc_ctr_last){
      if(rot_enc_ctr < 0)  rot_enc_ctr = rcbl;
      rot_enc_ctr_last = rot_enc_ctr;
      menus.prevItem();
  }

  if(rot_enc_ctr > rot_enc_ctr_last){
      if(rot_enc_ctr > rcbl)  rot_enc_ctr = 0;
      rot_enc_ctr_last = rot_enc_ctr;
      menus.nextItem();
  }
  
  if(menus.has_msg){
      packMsgByte(menus.getMsgByte());
      msg_ready = true;
  }
}

//Interrupt functions for the rotary encoder
void rotEncMovedLt(){
  cli(); //stop interrupts happening before we read pin values
  reading = PINE & 0x30; // read all eight pin values then strip away all but pinA and pinB's values
  if(reading == B00110000 && aFlag) { //check that we have both pins at detent (HIGH) and that we are expecting detent on this pin's rising edge
    rot_enc_ctr --; //decrement the encoder's position count
    bFlag = 0; //reset flags for the next turn
    aFlag = 0; //reset flags for the next turn
  }
  else if (reading == B00010000) bFlag = 1; //signal that we're expecting pinB to signal the transition to detent from free rotation
  sei(); //restart interrupts
}

void rotEncMovedRt(){
  cli();
  reading = PINE & 0x30; //read all eight pin values then strip away all but pinA and pinB's values
  if (reading == B00110000 && bFlag) { //check that we have both pins at detent (HIGH) and that we are expecting detent on this pin's rising edge
    rot_enc_ctr ++; //increment the encoder's position count
    bFlag = 0; //reset flags for the next turn
    aFlag = 0; //reset flags for the next turn
  }
  else if (reading == B00100000) aFlag = 1; //signal that we're expecting pinA to signal the transition to detent from free rotation
  sei();
}
/************************************************************/
