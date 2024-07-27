// Global variables
const int redPin = 5; // D1
const int yellowPin = 4; // D2
const int topYellowPin = 12; // D6
const int greenPin = 14; // D5
bool flash = false;
bool topFlash = false;
int flashPhase = true;
int flashTimerStart = 0;
const int flashOnTime = 660; // milliseconds
const int flashOffTime = 340; // milliseconds
int lastCommandTime = 0; // milliseconds
const int autoTimeout = 300; // seconds, before auto if no PC commands
int autoState = 0;
int lastAutoChangeTime = 0; // milliseconds
const int autoDwell = 5; // seconds

// function to reset all outputs and flashing bit
void resetOutputs() {
  digitalWrite(redPin, false);
  digitalWrite(yellowPin, false);
  digitalWrite(topYellowPin, false);
  digitalWrite(greenPin, false);
  flash = false;
}

// function to start flashing with correct phase
void startFlashing() {
  flash = true;
  flashPhase = true;
  flashTimerStart = millis();
}

// function to toggle the flashing aspects
void toggleFlash() {
  digitalWrite(yellowPin, !digitalRead(yellowPin));
  if (topFlash) {
    digitalWrite(topYellowPin, !digitalRead(topYellowPin));
  }
  flashPhase = !flashPhase;
  flashTimerStart = millis();
}

// function to show all outputs working when started
void testOutputs() {
  Serial.println("Testing outputs...");
  digitalWrite(redPin, true);
  delay(1000);
  digitalWrite(yellowPin, true);
  delay(1000);
  digitalWrite(topYellowPin, true);
  delay(1000);
  digitalWrite(greenPin, true);
  delay(2000);
  resetOutputs();
}

void changeState(int state) {
  // decode the state
  switch (state) {
    
    //red
    case 0:
      resetOutputs();
      digitalWrite(redPin, true);
      break;

    //yellow
    case 1:
      resetOutputs();
      digitalWrite(yellowPin, true);
      break;

    //double yellow
    case 2:
      resetOutputs();
      digitalWrite(yellowPin, true);
      digitalWrite(topYellowPin, true);
      break;

    //green
    case 3:
      resetOutputs();
      digitalWrite(greenPin, true);
      break;

    //flashing yellow
    case 4:
      resetOutputs();
      digitalWrite(yellowPin, true);
      startFlashing();
      topFlash = false;
      break;

    //flashing double yellow
    case 5:
      resetOutputs();
      digitalWrite(yellowPin, true);
      digitalWrite(topYellowPin, true);
      startFlashing();
      topFlash = true;
      break;
  }
}

void parseSerial() {
  // if there's any serial available, read it:
  while (Serial.available() > 0) {
    
    // look for the next valid integer in the incoming serial stream:
    int state = Serial.parseInt();
    
    // look for the newline. That's the end of your sentence:
    if (Serial.read() == '\n') {

      // Stop auto mode
      lastCommandTime = millis();
      autoState = 0;
      Serial.println("Decoding received state: " + String(state));
      changeState(state);
       
    }
  }
}

void flashUpdate() {
  // handle flashing
  if (flash) {
    if (flashPhase) {
      if (millis() - flashTimerStart >= flashOnTime) {
        toggleFlash();
      }
    } else {
      if (millis() - flashTimerStart >= flashOffTime) {
        toggleFlash();
      }
    }
  }
}

void autoMode() {
  
  // handle auto mode if no recent commands (PC stopped)
  if (millis() - lastCommandTime >= autoTimeout * 1000) {
    if (millis() - lastAutoChangeTime >= autoDwell * 1000) {
      Serial.println("Entering autostate: " + String(autoState));
      changeState(autoState);
      autoState = autoState+1;
      if (autoState >= 4) {
        autoState = 0;
      }
      lastAutoChangeTime = millis();
    }
  }
}

void setup() {
  // put your setup code here, to run once:

  //Initialise USB serial port at 9600 baud:
  Serial.begin(9600);
  Serial.println("DRC TVSC Signal Demo v1");
  Serial.println("Laurence Stant March 2023");

  //Initialise output pins:
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(topYellowPin, OUTPUT);
  pinMode(greenPin, OUTPUT);

  // Cycle outputs to show they work
  testOutputs();
}

void loop() {
  // put your main code here, to run repeatedly:

  // check for new commands from the PC:
  parseSerial();

  // Update flashing aspects if necessary:
  flashUpdate();

  // Auto sequence if the PC has stopped sending commands:
  autoMode();
}
