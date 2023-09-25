// Three buttons correspond to the three live data entry points 
// inside the python LEGO Super Mario program
// By KiriAnn Rodenburg




const int buttonPin = 2; // 
const int buttonPin2 = 7; // 
const int buttonPin3 = 12; // 

const int ledPin = 13;   // Replace with your actual LED pin


int buttonState = LOW;    // current state of the button
int lastButtonState = LOW; // previous state of the button

int buttonState2 = LOW;    // current state of the button
int lastButtonState2 = LOW; // previous state of the button

int buttonState3 = LOW;    // current state of the button
int lastButtonState3 = LOW; // previous state of the button

unsigned long lastDebounceTime = 0;  // last time the button state was changed
unsigned long debounceDelay = 50;    // debounce time in milliseconds

unsigned long lastDebounceTime2 = 0;  // last time the button state was changed
unsigned long debounceDelay2 = 50;    // debounce time in milliseconds

unsigned long lastDebounceTime3 = 0;  // last time the button state was changed
unsigned long debounceDelay3 = 50;    // debounce time in milliseconds

void setup() {
  pinMode(buttonPin, INPUT_PULLUP); // INPUT_PULLUP enables internal pull-up resistor
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  int reading = digitalRead(buttonPin);
 
  // check if the button state has changed
  if (reading != lastButtonState) {
    lastDebounceTime = millis(); // reset the debounce timer

    if (reading == HIGH) {
      // button was just pressed
      digitalWrite(ledPin, HIGH);
      Serial.write('1');
    }
  }

  // check for button release after debounce
  if ((millis() - lastDebounceTime) > debounceDelay && reading == LOW) {
    // button has been released after debounce
    digitalWrite(ledPin, LOW);
    
  }

  lastButtonState = reading;

//////////////////////////////////////////////////////////////////////////
  
  int reading2 = digitalRead(buttonPin2);

  // check if the button state has changed
  if (reading2 != lastButtonState2) {
    lastDebounceTime2 = millis(); // reset the debounce timer

    if (reading2 == HIGH) {
      // button was just pressed
      digitalWrite(ledPin, HIGH);
      Serial.write('2');
    }
  }

  // check for button release after debounce
  if ((millis() - lastDebounceTime2) > debounceDelay2 && reading2 == LOW) {
    // button has been released after debounce
    digitalWrite(ledPin, LOW);
    
  }
  
  lastButtonState2 = reading2;

 ////////////////////////////////////////////////////////////////////
  
  int reading3 = digitalRead(buttonPin3);

   // check if the button state has changed
  if (reading3 != lastButtonState3) {
    lastDebounceTime3 = millis(); // reset the debounce timer

    if (reading3 == HIGH) {
      // button was just pressed
      digitalWrite(ledPin, HIGH);
      Serial.write('3');
    }
  }

  // check for button release after debounce
  if ((millis() - lastDebounceTime3) > debounceDelay3 && reading3 == LOW) {
    // button has been released after debounce
    digitalWrite(ledPin, LOW);
    
  }

  lastButtonState3 = reading3;
  
}
