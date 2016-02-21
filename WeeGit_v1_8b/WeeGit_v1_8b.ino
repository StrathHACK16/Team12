/*
 
  This example code is in the public domain.
 
  ---------------------------------------------------------------------
 
  This program demonstrates button detection, LCD text/number printing,
  and LCD backlight control on the Freetronics LCD & Keypad Shield, connected to an Arduino board.
 
 
  Pins used by LCD & Keypad Shield:
 
    A0: Buttons, analog input from voltage ladder
    D4: LCD bit 4
    D5: LCD bit 5
    D6: LCD bit 6
    D7: LCD bit 7
    D8: LCD RS
    D9: LCD E
    D10: LCD Backlight (high = on, also has pullup high so default is on)
 
  ADC voltages for the 5 buttons on analog input pin A0:
 
    RIGHT:  0.00V :   0 @ 8bit ;   0 @ 10 bit
    UP:     0.71V :  36 @ 8bit ; 145 @ 10 bit
    DOWN:   1.61V :  82 @ 8bit ; 329 @ 10 bit
    LEFT:   2.47V : 126 @ 8bit ; 505 @ 10 bit
    SELECT: 3.62V : 185 @ 8bit ; 741 @ 10 bit
*/
/*--------------------------------------------------------------------------------------
  Includes
--------------------------------------------------------------------------------------*/
#include <LiquidCrystal.h>   // include LCD library
/*--------------------------------------------------------------------------------------
  Defines
--------------------------------------------------------------------------------------*/
#define NAME "WeeGit v1.0"
#define TRUE '1'
#define GREEN 11
#define AMBER 12
#define RED 13
#define DELIMITER '|'
// Pins in use
#define BUTTON_ADC_PIN           A0  // A0 is the button ADC input
#define LCD_BACKLIGHT_PIN         10  // D10 controls LCD backlight
// ADC readings expected for the 5 buttons on the ADC input
#define RIGHT_10BIT_ADC           0  // right
#define UP_10BIT_ADC            145  // up
#define DOWN_10BIT_ADC          329  // down
#define LEFT_10BIT_ADC          505  // left
#define SELECT_10BIT_ADC        741  // right
#define BUTTONHYSTERESIS         10  // hysteresis for valid button sensing window
//return values for ReadButtons()
#define BUTTON_NONE               0  // 
#define BUTTON_RIGHT              1  // 
#define BUTTON_UP                 2  // 
#define BUTTON_DOWN               3  // 
#define BUTTON_LEFT               4  // 
#define BUTTON_SELECT             5  // 
//some example macros with friendly labels for LCD backlight/pin control, tested and can be swapped into the example code as you like
#define LCD_BACKLIGHT_OFF()     digitalWrite( LCD_BACKLIGHT_PIN, LOW )
#define LCD_BACKLIGHT_ON()      digitalWrite( LCD_BACKLIGHT_PIN, HIGH )
#define LCD_BACKLIGHT(state)    { if( state ){digitalWrite( LCD_BACKLIGHT_PIN, HIGH );}else{digitalWrite( LCD_BACKLIGHT_PIN, LOW );} }
/*--------------------------------------------------------------------------------------
  Variables
--------------------------------------------------------------------------------------*/
byte buttonJustPressed  = false;         //this will be true after a ReadButtons() call if triggered
byte buttonJustReleased = false;         //this will be true after a ReadButtons() call if triggered
byte buttonWas          = BUTTON_NONE;   //used by ReadButtons() for detection of button events
/*--------------------------------------------------------------------------------------
  Init the LCD library with the LCD pins to be used
--------------------------------------------------------------------------------------*/
LiquidCrystal lcd( 8, 9, 4, 5, 6, 7 );   //Pins for the freetronics 16x2 LCD shield. LCD: ( RS, E, LCD-D4, LCD-D5, LCD-D6, LCD-D7 )
/*--------------------------------------------------------------------------------------
  setup()
  Called by the Arduino framework once, before the main loop begins
--------------------------------------------------------------------------------------*/

String topLine = NAME;
String bottomLine = "";
boolean ledControl[3] = {false, false, false};
int cycles = 0;

void setup()
{
   //button adc input
   pinMode(BUTTON_ADC_PIN, INPUT );         //ensure A0 is an input
   pinMode(GREEN, OUTPUT);
   pinMode(AMBER, OUTPUT);
   pinMode(RED, OUTPUT);
   digitalWrite( BUTTON_ADC_PIN, LOW );      //ensure pullup is off on A0
   //lcd backlight control
   digitalWrite( LCD_BACKLIGHT_PIN, HIGH );  //backlight control pin D3 is high (on)
   pinMode( LCD_BACKLIGHT_PIN, OUTPUT );     //D3 is an output
   //set up the LCD number of columns and rows: 
   lcd.begin( 16, 2 );
   //Print some initial text to the LCD.
   printStrings();   
   Serial.begin(9600);
}
/*--------------------------------------------------------------------------------------
  loop()
  Arduino main loop
--------------------------------------------------------------------------------------*/
void loop()
{
   byte button;
   byte timestamp;
   
   if(readSerial()){
     printStrings();
     setLeds();
     timestamp = millis();
     cycles = 0;
   }
   else if (topLine.length() > 16 && ((millis() - timestamp) % 750 < 100)){
     cycles++;
     lcd.setCursor(0,0);
     if (topLine.length() - cycles - 5 < 1)
       cycles = 0;
     lcd.print((topLine + "               ").substring(cycles, cycles + 16));
     timestamp = millis();
    
  }
     
   
   
   //get the latest button pressed, also the buttonJustPressed, buttonJustReleased flags
   button = ReadButtons();

   //blank the demo text line if a new button is pressed or released, ready for a new label to be written
   if( buttonJustPressed)
   {
     if(button != BUTTON_NONE){
     writeSerial(button);
     }
   }

   if( buttonJustPressed )
      buttonJustPressed = false;
   if( buttonJustReleased )
      buttonJustReleased = false;
      
   delay(100);      
}

boolean readSerial() {
  char c = Serial.read();
  if (c == -1) return false;
  unsigned long timestamp = millis();
  topLine = "";
  while(c != DELIMITER && millis() <= timestamp + 1000 ) {
    if (c != -1)
      topLine += c;
    c = Serial.read();
  }
  bottomLine = "";
  c = -1;
  while(c != DELIMITER && millis() <= timestamp + 1000) {
    if (c != -1)
      bottomLine += c;
    c = Serial.read();
  }
  String ledTemp = "";
  c = -1;
  while(c != DELIMITER && millis() <= timestamp + 1000) {
    if (c != -1)
      ledTemp += c;
    c = Serial.read();
  }
  ledControl[0] = ledTemp.charAt(0) == TRUE;
  ledControl[1] = ledTemp.charAt(1) == TRUE;
  ledControl[2] = ledTemp.charAt(2) == TRUE;
  
  return true;
}

void writeSerial(int data){
  Serial.println(data);
}

void printStrings() {
  int timestamp = millis();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(topLine);
  lcd.setCursor(0,1);
  lcd.print(bottomLine);
}

void setLeds(){
  if(ledControl[0])
    digitalWrite(GREEN, HIGH);
  else
    digitalWrite(GREEN, LOW);
  
  if(ledControl[1])
    digitalWrite(AMBER, HIGH);
  else
    digitalWrite(AMBER, LOW);
  
  if(ledControl[2])
    digitalWrite(RED, HIGH);
  else
    digitalWrite(RED, LOW);
}

/*--------------------------------------------------------------------------------------
  ReadButtons()
  Detect the button pressed and return the value
  Uses global values buttonWas, buttonJustPressed, buttonJustReleased.
--------------------------------------------------------------------------------------*/
byte ReadButtons()
{
   unsigned int buttonVoltage;
   byte button = BUTTON_NONE;   // return no button pressed if the below checks don't write to btn
 
   //read the button ADC pin voltage
   buttonVoltage = analogRead( BUTTON_ADC_PIN );
   //sense if the voltage falls within valid voltage windows
   if( buttonVoltage < ( RIGHT_10BIT_ADC + BUTTONHYSTERESIS ) )
   {
      button = BUTTON_RIGHT;
   }
   else if(   buttonVoltage >= ( UP_10BIT_ADC - BUTTONHYSTERESIS )
           && buttonVoltage <= ( UP_10BIT_ADC + BUTTONHYSTERESIS ) )
   {
      button = BUTTON_UP;
   }
   else if(   buttonVoltage >= ( DOWN_10BIT_ADC - BUTTONHYSTERESIS )
           && buttonVoltage <= ( DOWN_10BIT_ADC + BUTTONHYSTERESIS ) )
   {
      button = BUTTON_DOWN;
   }
   else if(   buttonVoltage >= ( LEFT_10BIT_ADC - BUTTONHYSTERESIS )
           && buttonVoltage <= ( LEFT_10BIT_ADC + BUTTONHYSTERESIS ) )
   {
      button = BUTTON_LEFT;
   }
   else if(   buttonVoltage >= ( SELECT_10BIT_ADC - BUTTONHYSTERESIS )
           && buttonVoltage <= ( SELECT_10BIT_ADC + BUTTONHYSTERESIS ) )
   {
      button = BUTTON_SELECT;
   }
   //handle button flags for just pressed and just released events
   if( ( buttonWas == BUTTON_NONE ) && ( button != BUTTON_NONE ) )
   {
      //the button was just pressed, set buttonJustPressed, this can optionally be used to trigger a once-off action for a button press event
      //it's the duty of the receiver to clear these flags if it wants to detect a new button change event
      buttonJustPressed  = true;
      buttonJustReleased = false;
   }
   if( ( buttonWas != BUTTON_NONE ) && ( button == BUTTON_NONE ) )
   {
      buttonJustPressed  = false;
      buttonJustReleased = true;
   }
 
   //save the latest button value, for change event detection next time round
   buttonWas = button;
 
   return( button );
}

