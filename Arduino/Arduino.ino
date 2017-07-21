/*
 * IRremote: IRrecvDump - dump details of IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 * JVC and Panasonic protocol added by Kristian Lauszus (Thanks to zenwheel and other people at the original blog post)
 * LG added by Darryl Smith (based on the JVC protocol)
 */

#include <IRremote.h>
#include <lgWhisen.h>


#define NTC A0
#define REFRESISTOR 10000

#define BCOEFFICIENT 3950
#define TEMPERATURENOMIAL 25
#define TERMISTORNOMIAL 10000

/* 
*  Default is Arduino pin D11. 
*  You can change this to another available Arduino Pin.
*  Your IR receiver should be connected to the pin defined here
*/
int RECV_PIN = 11; 

IRrecv irrecv(RECV_PIN);
IRsend irsend;
decode_results results;
lgWhisen lgWhisen(1, 0);


float getTemp()
{
  float Value;
  Value = analogRead(NTC);
  Value = REFRESISTOR / (1023 / Value - 1);
  /*Serial.print("NTC resist value : ");
  Serial.print(Value, 3);
  Serial.print("\t");*/

  float temperature;
  temperature = Value / TERMISTORNOMIAL;
  temperature = log(temperature);
  temperature /= BCOEFFICIENT;
  temperature += 1.0 / (TEMPERATURENOMIAL + 273.15);
  temperature = 1.0 / temperature;
  temperature -= 273.15;
  return temperature;
}
void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}
void dump(decode_results *results); 
void loop() {
  // send data only when you receive data:
  String str;
  

    if(Serial.available() > 0)
    {
        str = Serial.readStringUntil('\n');
        Serial.print("I/Received: ");
        Serial.println(str);
        if(str.length() > 2){
           if(str[0] == 'C' && str[2] == '0'){ // ON
             Serial.println("I/0/Turn ON");
              lgWhisen.activate(18, 1);
              delay(1000); 
              lgWhisen.activate(18, 1);
              delay(1000); 
           }        
           else if(str[0] == 'C' && str[2] == '1'){ // OFF
             Serial.println("I/1/Turn OFF");
              lgWhisen.power_down();
              delay(1000); 
              lgWhisen.power_down();
              delay(1000); 
           }     
           else if(str[0] == 'C' && str[2] == '2'){ // Degree
             Serial.print("I/2/");
             Serial.println(getTemp());
           }
        }
        
    }
  
   
/*  
  Serial.println("OK");
  lgWhisen.activate(18, 1);
  delay(1000); 
*/


  /*
  Serial.println("OK");
  int khz = 38; // 38kHz carrier frequency for the NEC protocol
  unsigned int poweron [] = {500, 1600, 450, 550, 500, 550, 450, 600, 450, 1600, 500, 550, 450, 550, 500, 550, 450, 550, 550, 500, 500, 550, 450, 550, 500, 550, 500, 550, 450, 550, 500, 550, 500, 550, 500, 550, 500, 1550, 500, 1600, 450, 550, 500, 1550, 500, 550, 450, 600, 500, 500, 550, 1550, 500, 1600, 450, 1600, 450};
  unsigned int cool    [] = {500, 1600, 450, 550, 500, 550, 500, 550, 450, 1600, 500, 550, 500, 550, 450, 550, 500, 550, 500, 550, 450, 550, 500, 550, 500, 1600, 450, 550, 500, 550, 450, 550, 500, 550, 500, 550, 450, 1600, 500, 1600, 450, 550, 500, 1600, 450, 550, 500, 550, 500, 1550, 500, 1600, 450, 1600, 500, 1600, 450};
  unsigned int poweroff[] = {500, 1600, 450, 600, 450, 550, 500, 550, 500, 1550, 500, 550, 500, 550, 450, 550, 500, 1600, 450, 1600, 500, 550, 450, 550, 500, 600, 450, 550, 500, 550, 450, 600, 450, 550, 500, 550, 450, 550, 500, 550, 450, 600, 450, 1600, 500, 550, 450, 1600, 500, 550, 500, 550, 450, 550, 500, 1600, 450}; 
  //AnalysIR Batch Export (IRremote) - RAW
  irsend.sendRaw(cool, sizeof(cool) / sizeof(cool[0]), khz); //Note the approach used to automatically calculate the size of the array.
  delay(1000);
  //irsend.sendRaw(cool, sizeof(cool) / sizeof(cool[0]), khz); //Note the approach used to automatically calculate the size of the array.
  //delay(5000);
  */
  


  /*
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    dump(&results);
    //Serial.println(results.bits);
    //lgWhisen.decode(&results);
    irrecv.resume(); // Receive the next value
  }
  */
  
}

void dump(decode_results *results) {
  // Dumps out the decode_results structure.
  // Call this after IRrecv::decode()
  int count = results->rawlen;
  if (results->decode_type == UNKNOWN) {
    Serial.print("Unknown encoding: ");
  }
  else if (results->decode_type == NEC) {
    Serial.print("Decoded NEC: ");

  }
  else if (results->decode_type == SONY) {
    Serial.print("Decoded SONY: ");
  }
  else if (results->decode_type == RC5) {
    Serial.print("Decoded RC5: ");
  }
  else if (results->decode_type == RC6) {
    Serial.print("Decoded RC6: ");
  }
  else if (results->decode_type == PANASONIC) {
    Serial.print("Decoded PANASONIC - Address: ");
    Serial.print(results->address, HEX);
    Serial.print(" Value: ");
  }
  else if (results->decode_type == LG) {
    Serial.print("Decoded LG: ");
  }
  else if (results->decode_type == JVC) {
    Serial.print("Decoded JVC: ");
  }
  else if (results->decode_type == AIWA_RC_T501) {
    Serial.print("Decoded AIWA RC T501: ");
  }
  else if (results->decode_type == WHYNTER) {
    Serial.print("Decoded Whynter: ");
  }
  Serial.print(results->value, HEX);
  Serial.print(" (");
  Serial.print(results->bits, DEC);
  Serial.println(" bits)");
  Serial.print("Raw (");
  Serial.print(count, DEC);
  Serial.print("): ");

  for (int i = 1; i < count; i++) {
    if (i & 1) {
      Serial.print(results->rawbuf[i]*USECPERTICK, DEC);
    }
    else {
      Serial.write('-');
      Serial.print((unsigned long) results->rawbuf[i]*USECPERTICK, DEC);
    }
    Serial.print(" ");
  }
  Serial.println();
}
