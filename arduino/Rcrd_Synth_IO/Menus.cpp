#include "Menus.h"

    Menus::Menus(SerLCD& ser_lcd, LiquidCrystal_I2C& i2c_lcd): red_lcd(ser_lcd), blue_lcd(i2c_lcd){}
    
    void Menus::init_red(){
        red_lcd.begin();
        red_lcd.clear();
        red_lcd.print("Time to play!");
    }

    void Menus::init_blue(){
        blue_lcd.init(); //initialize the lcd
        blue_lcd.backlight(); //open the backlight
    }
   
    void Menus::disp_knob_vals(byte* knob_values){
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

    void Menus::disp_switch(int index, byte* sw_values){
        //index = get_safe_index(SWITCHES);
        red_lcd.clear();
        red_lcd.setPosition(0,0);
        red_lcd.print(sw_names[index]);
        red_lcd.setPosition(2,0);
        red_lcd.print(sw_values[index]);
    }

    void Menus::disp_top(int updn){
        //index = get_safe_index(TOP);
        red_lcd.clear();
        red_lcd.setPosition(0,0);
        red_lcd.print(top_options[index]);
    }

    void Menus::get_wheel(int val){
        return val;
    }
    
    void Menus::disp_wheel(int val){
        red_lcd.clear();
        red_lcd.setPosition(0,0);
        red_lcd.print(val);    
    }

