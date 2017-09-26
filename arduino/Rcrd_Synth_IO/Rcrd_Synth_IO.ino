
#include "PinDefs.h"
#include "Comms.h"
#include "Menus.h"

int rcbl = 100; //rotary encoder bank limit
int rot_enc_ctr = 0;
int rot_enc_ctr_last = 0;
int sw_val_last;

void initInput();
bool updateInput();
void rotEncMovedLt();
void rotEncMovedRt();

SerLCD red_lcd(Serial1,16,2);    //RED ON BLACK LCD
LiquidCrystal_I2C blue_lcd(0x27,20,4); //BLUE ON WHITLE LCD
Menus menus(red_lcd, blue_lcd);

void setup()
{
  analogReference(EXTERNAL);
  attachInterrupt(0, rotEncMovedLt, RISING);
  attachInterrupt(1, rotEncMovedRt, RISING);
  
  Serial.begin(9600);
  Serial1.begin(9600);

  menus.init_red();
  menus.init_blue();
  initInput();
 }
/*********************************************************/
void loop() {
  
  if(updateInput()){
  
      menus.disp_knob_vals(knob_values);
      menus.disp_switch(rot_enc_ctr, sw_values);
      //delay(10);
      packKnobData();
      packSwData();
  
      //for(int i=0; i<=7; i++){
      //    Serial.write(output_buf[i]);
      //}
      //Serial.print("\n");
  }  
    
  if(rot_enc_ctr != rot_enc_ctr_last){
      if(rot_enc_ctr < 0)  rot_enc_ctr = rcbl;
      if(rot_enc_ctr > rcbl) rot_enc_ctr = 0;
      //menus.disp_wheel(rot_enc_ctr);
      menus.disp_switch(rot_enc_ctr, sw_values);
      //menus.disp_top(rot_enc_ctr);
      rot_enc_ctr_last = rot_enc_ctr;
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
