#include <SerLCD.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

class Menus
{

public:
    Menus(SerLCD&, LiquidCrystal_I2C&);
    void init_red();
    void init_blue();

    void disp_knob_vals(byte*);
    void disp_switch(int, byte*);
    
    void get_wheel(int);
    void disp_wheel(int);
    void select();
    
private:
    SerLCD red_lcd;
    LiquidCrystal_I2C blue_lcd;
    int index;
    int last_wheel_val;
    char* sw_names[10] = {"12", "7", "AUTO", "START", "33","78", "LEFT", "RIGHT", "ROT ENC", "PROGRAM"};
    char* knob_names[5] = {"KNOB1", "KNOB2", "KNOB3", "KNOB4", "KNOB5"};
    char* top_options[3] = {"Switches", "Isolate Channel", "Poweroff"};

    enum menu_title {TOP, SWITCHES, POWEROFF};
    menu_title current_menu;

    void disp_top(int);    
    int get_safe_index(menu_title);

};

