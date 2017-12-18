#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SerLCD.h>
#include "types.h"

/// one-based number of menu items
#define TOP_NUM_ITEMS 4
#define SWITCHES_NUM_ITEMS 10
#define PWROFF_NUM_ITEMS 2
#define NEWSONG_NUM_ITEMS 2

class Menus
{

public:
    Menus(SerLCD&, LiquidCrystal_I2C&);
    bool has_msg;
    
    void initRed();
    void initBlue();
    void dispKnobVals(byte*);
    void nextItem();
    void prevItem();
    void select();
    void dispTopMenu();
    void dispSwitchesMenu();
    void dispInt(int);
    byte getMsgByte();
    
private:
    SerLCD red_lcd;
    LiquidCrystal_I2C blue_lcd;
    int index;
    int last_wheel_val;
    char* sw_names[SWITCHES_NUM_ITEMS] = {"12", "7", "AUTO", "START", "33","78", "LEFT", "RIGHT", "ROT ENC", "PROGRAM"};
    char* knob_names[5] = {"KNOB1", "KNOB2", "KNOB3", "KNOB4", "KNOB5"};
    char* menu_items_top[TOP_NUM_ITEMS] = {"Switches", "Isolate Channel", "New Song", "Poweroff"};
    char* menu_items_pwroff[PWROFF_NUM_ITEMS] = {"Confirm poweroff", "Cancel"};
    char* menu_items_dlsong[NEWSONG_NUM_ITEMS] = {"Confirm new song", "Cancel"};
    e_menu_titles current_menu;

    int checkBounds(int);
    void changeItem(int);
    void changeMenu(e_menu_titles);
    byte msg_byte; 
};
