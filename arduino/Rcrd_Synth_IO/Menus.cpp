#include "Menus.h"

    //commands
    #define MSG_NONE    0x00 // 192
    #define MSG_PWROFF  0x01 // 193
    #define MSG_NEWSONG 0x02 // 194

    Menus::Menus(SerLCD& ser_lcd, LiquidCrystal_I2C& i2c_lcd): red_lcd(ser_lcd), blue_lcd(i2c_lcd){
      current_menu = TOP;
      has_msg = false;
      msg_byte = MSG_NONE; 
    }
    
    void Menus::initRed(){
        red_lcd.begin();
        red_lcd.clear();
        red_lcd.print("Record Synth!");
    }

    void Menus::initBlue(){
        blue_lcd.init(); //initialize the lcd
        blue_lcd.backlight(); //turn on backlight
    }
   
    void Menus::dispKnobVals(byte* knob_values){
        blue_lcd.setCursor(0,0);
        blue_lcd.print(String(knob_values[4]));
        blue_lcd.print("    ");
        blue_lcd.setCursor(10,0);
        blue_lcd.print(String(knob_values[3]));
        blue_lcd.print("    ");
        blue_lcd.setCursor(0,1);
        blue_lcd.print(String(knob_values[2]));
        blue_lcd.print("    ");
        blue_lcd.setCursor(10,1);
        blue_lcd.print(String(knob_values[1]));
        blue_lcd.print("    ");
        blue_lcd.setCursor(0,2);
        blue_lcd.print(String(knob_values[0]));
        blue_lcd.print("    ");
    }

    /*void Menus::dispSwitch(int index, byte* sw_values){
        red_lcd.clear();
        red_lcd.setPosition(0,0);
        red_lcd.print(sw_names[index]);
        red_lcd.setPosition(2,0);
        red_lcd.print(sw_values[index]);
    }*/

    void Menus::nextItem(){
        index++;
        index = checkBounds(index);
        changeItem(index);
    }

    void Menus::prevItem(){
        index--;
        index = checkBounds(index);
        changeItem(index);
    }

    void Menus::changeItem(int idx){
        red_lcd.clear();
        red_lcd.setPosition(1,0);
        switch(current_menu){
          case TOP:
            red_lcd.print(menu_items_top[idx]);
          break;
          case SWITCHES:
            red_lcd.print(sw_names[idx]);
          break;
          case POWEROFF:
            red_lcd.print(menu_items_pwroff[idx]);
          break;
          case NEWSONG:
            red_lcd.print(menu_items_dlsong[idx]);
          break;
        }
    }

    int Menus::checkBounds(int idx){
        switch(current_menu){
          case TOP:
            if(idx > TOP_NUM_ITEMS-1)
              idx = 0;
            else if(idx < 0)
              idx = TOP_NUM_ITEMS-1;
          break;
          case SWITCHES:
            if(idx > SWITCHES_NUM_ITEMS-1)
              idx = 0;
            else if(idx < 0)
              idx = SWITCHES_NUM_ITEMS-1;
          break;
          case POWEROFF:
            if(idx > PWROFF_NUM_ITEMS-1)
              idx = 0;
            else if(idx < 0)
              idx = PWROFF_NUM_ITEMS-1;
          break;
          case NEWSONG:
            if(idx > NEWSONG_NUM_ITEMS-1)
              idx = 0;
            else if(idx < 0)
              idx = NEWSONG_NUM_ITEMS-1;
          break;
        }
        return idx;
    }
    
    void Menus::select(){
      switch(current_menu) {
        /************/
        case TOP:
          switch(index){
            case 0: //switches
              changeMenu(SWITCHES);
            break;
            case 1: //isolate channel
              //msg_byte = byte(MSG_ISO_CH);
              //has_msg = true;
            break;
            case 2: //new song
              changeMenu(NEWSONG);
              //msg_byte = byte(MSG_NEWSONG); 
              has_msg = true;
            break;
            case 3: //poweroff
              changeMenu(POWEROFF);
            break;
          }
        break;
        /************/
        case SWITCHES:
          changeMenu(TOP);
        break;
        /************/
        case POWEROFF:
          // confirm
          if(index == 0){
            msg_byte = byte(MSG_PWROFF);
            has_msg = true;
            changeMenu(TOP);
          }
          // cancel
          else if(index == 1){
            changeMenu(TOP);
          }
        break;
        /************/
        case NEWSONG:
          if(index == 0){ // confirm
            msg_byte = byte(MSG_NEWSONG);
            has_msg = true;
            changeMenu(TOP);
          }
          else if(index == 1){  // cancel
            changeMenu(TOP);
          }
        break;
      }
    }
    
    void Menus::changeMenu(e_menu_titles new_menu){
      current_menu = new_menu;
      index = 0;
      changeItem(0);
    }

    byte Menus::getMsgByte(){
      has_msg = false;
      byte rtn = msg_byte;
      msg_byte = MSG_NONE;
      return rtn;
    }

    void Menus::dispTopMenu(){
      if(current_menu != TOP)
        changeMenu(TOP);
    }
/*
    void Menus::dispSwitchesMenu(){
      if(current_menu != SWITCHES)
        changeMenu(SWITCHES);
    }
    void Menus::dispInt(int i){
        red_lcd.setPosition(2,0);
        red_lcd.print(i);
    }
*/
