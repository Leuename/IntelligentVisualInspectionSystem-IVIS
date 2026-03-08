// === Global flags ===
bool isRunning = false;
bool stopFlag = false;
bool resetPressed = false;
int stripIndex = 0;
int processStep = 0;  // NEW: Move step variable to global scope

// === Pin definitions ===
#define stepPinL 4  
#define dirPinL 5  
#define stepPinR 6  
#define dirPinR 7  
#define stepPinC 8  
#define dirPinC 9  
#define for_dc 2  
#define rev_dc 3  
#define rel_break 10  

#define lsL 48  
#define lsR 50  
#define lsPR 46  
#define lsPF 52  

#define button_stop 26  
#define button_reset 32

// === HOMING FUNCTION FOR STEPPERS ===
void HomeStepper(uint8_t pulse, uint8_t dir, uint8_t ls, int dec = 0) {
  delay(50);
  digitalWrite(dir, dec);
  while (digitalRead(ls) == 1) {
    if (checkForStop()) return; 
    digitalWrite(pulse, HIGH);
    delayMicroseconds(350);
    digitalWrite(pulse, LOW);
    delayMicroseconds(350);
  }
  digitalWrite(pulse, HIGH);
  delay(200);
  Serial.println("STOP");
}

// === HOMING FUNCTION FOR PUSHER ===
void HomePusher() {
  Serial.println("Homing pusher...");
  digitalWrite(for_dc, HIGH);  // stop forward
  digitalWrite(rev_dc, LOW);   // move reverse
  delay(50);

  unsigned long startT = millis();
  while (digitalRead(lsPR) == 1 && millis() - startT < 20000) { // 20s timeout
    if (checkForStop()) {
      digitalWrite(rev_dc, HIGH); // stop motor
      return;
    }
  }

  digitalWrite(rev_dc, HIGH); // stop motor
  Serial.println("Pusher homed at reverse limit");
}

// === SETUP ===
void setup() {
  Serial.begin(115200);
  Serial.println("=== SYSTEM BOOTED ===");

  pinMode(stepPinL, OUTPUT); 
  pinMode(stepPinR, OUTPUT);
  pinMode(stepPinC, OUTPUT);
  pinMode(dirPinL, OUTPUT); 
  pinMode(dirPinR, OUTPUT); 
  pinMode(dirPinC, OUTPUT);

  pinMode(for_dc, OUTPUT);
  pinMode(rev_dc, OUTPUT);
  pinMode(rel_break, OUTPUT);

  digitalWrite(for_dc, HIGH);
  digitalWrite(rev_dc, HIGH);
  digitalWrite(rel_break, HIGH);

  pinMode(lsL, INPUT_PULLUP);
  pinMode(lsR, INPUT_PULLUP);
  pinMode(lsPR, INPUT_PULLUP);
  pinMode(lsPF, INPUT_PULLUP);

  pinMode(button_stop, INPUT_PULLUP);
  pinMode(button_reset, INPUT_PULLUP);


  // Reset if PR switch triggered
  if (digitalRead(lsPR) == 1) {
    digitalWrite(rev_dc, LOW);
    delay(100);
    unsigned long startT = millis();
    while (digitalRead(lsPR) == 1 && millis() - startT < 5000) {
      if (checkForStop()) return;
    }
    digitalWrite(rev_dc, HIGH);
    delay(100);
  }

  // Homing
  HomeStepper(stepPinL, dirPinL, lsL);
  HomeStepper(stepPinR, dirPinR, lsR, 0);
}

// === LOOP ===
void loop() {
  // Process strips only if isRunning triggered by serial
  if (isRunning) processOneStrip();

  // Continuously check for serial input
  if (Serial.available()) handleSerial();

  // Check stop button
  checkStopButton();

   // Check reset button
  if (digitalRead(button_reset) == LOW) {
    delay(20); // debounce
    if (digitalRead(button_reset) == LOW && !resetPressed) {
      Serial.println("RESET BUTTON PRESSED");
      resetSystem();    // homes pusher first, then stepper motors
      resetPressed = true;
    }
  } else {
    // Button released, allow next press
    resetPressed = false;
  }
}

// === SERIAL COMMAND HANDLER ===
void handleSerial() {
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  cmd.toLowerCase();  // normalize to lowercase

  if (cmd == "play") {
    if (!isRunning) {
      isRunning = true;
      stopFlag = false;

      if (stripIndex == 0) {
        Serial.println("Playing — starting process...");
      } else {
        Serial.print("Playing — resuming process at strip ");
        Serial.println(stripIndex + 1);
      }
    } else if (stopFlag) {
      stopFlag = false;
      Serial.println("Playing — resuming process from last step...");
    }
    Serial.println("ACK_PLAY");
  }
  else if (cmd == "pause") {
    if (isRunning && !stopFlag) {
      stopFlag = true;
      Serial.println("Paused — process halted. Current step and state saved.");
    }
    Serial.println("ACK_PAUSE");
  }
     else if (cmd == "reset") {
    Serial.println("RESET COMMAND RECEIVED");
    resetSystem();             // Perform same reset as button
    Serial.println("ACK_RESET");
  }
}

// === EMERGENCY STOP ===
void stopAll() {
  digitalWrite(for_dc, HIGH);
  digitalWrite(rev_dc, HIGH);
  digitalWrite(rel_break, HIGH);
  isRunning = false;
  stopFlag = false;
  Serial.println("SYSTEM STOPPED SAFELY.");
}

// === STOP CHECK FUNCTION ===
bool checkForStop() {
  static unsigned long lastStopTime = 0;
  static bool stopState = false;

  int reading = digitalRead(button_stop);

  // debounce: require stable LOW for 50ms
  if (reading == LOW && !stopState && millis() - lastStopTime > 300) {
    delay(20); // small debounce delay
    if (digitalRead(button_stop) == LOW) {
      stopAll();
      stopState = true;
      lastStopTime = millis();
      return true;
    }
  }

  if (reading == HIGH) stopState = false;
  return false;
}

// Helper to continuously check physical stop button
void checkStopButton() {
  checkForStop();
}

// === RESET FUNCTION ===
void resetSystem() {
  Serial.println("SYSTEM RESET — initializing...");

  // 1. Stop all motors
  stopAll();

  // 2. Reset global variables
  stripIndex = 0;
  processStep = 0;  // FIXED: Reset the step counter
  isRunning = false;
  stopFlag = false;

  // 3. Perform homing sequence
  HomePusher();
  HomeStepper(stepPinL, dirPinL, lsL);
  HomeStepper(stepPinR, dirPinR, lsR, 0);

  Serial.println("HOMING COMPLETE — system ready for new operation.");
}

// === PROCESS FUNCTIONS ===
void forward() {
  Serial.println("PUSH FORWARD");
  if (digitalRead(lsPF) == 1) {
    digitalWrite(for_dc, LOW);  // Motor starts
    delay(100);
    unsigned long startT = millis();
    while (digitalRead(lsPF) == 1 && millis() - startT < 20000) {
      if (checkForStop()) {
        digitalWrite(for_dc, HIGH);  // ← STOP MOTOR FIRST! ✓
        return;
      }
    }
    digitalWrite(for_dc, HIGH);  // Normal stop
    delay(100);
  }

  delay(1000);
  Serial.println("MOVE CONVEYOR TO INSPECTION AREA");
  digitalWrite(rel_break, LOW);
  delay(100);
  digitalWrite(dirPinC, LOW);
  for (int x = 0; x < 420; x++) {
    if (checkForStop()) return;
    digitalWrite(stepPinC, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPinC, LOW);
    delayMicroseconds(1000);
  }
  for (int i = 1; i <= 10; i++) {
    digitalWrite(dirPinC, LOW);
    for (int x = 0; x < 42; x++) {
      if (checkForStop()) return;
      digitalWrite(stepPinC, HIGH);
      delayMicroseconds(1000);
      digitalWrite(stepPinC, LOW);
      delayMicroseconds(1000);
    }
    // interruptible wait
    unsigned long t0 = millis();
    while (millis() - t0 < 1000) {
      if (checkForStop()) return;
      delay(10);
    }
  }
  digitalWrite(rel_break, HIGH);
  Serial.println("Brake engaged — conveyor stopped.");
}

void reverse() {
  Serial.println("PUSH REVERSE");
  if (digitalRead(lsPR) == 1) {
    digitalWrite(rev_dc, LOW);  // Motor starts
    delay(100);
    unsigned long startT = millis();
    while (digitalRead(lsPR) == 1 && millis() - startT < 20000) {
      if (checkForStop()) {
        digitalWrite(rev_dc, HIGH);  // ← STOP MOTOR FIRST! ✓
        return;
      }
    }
    digitalWrite(rev_dc, HIGH);  // Normal stop
    delay(100);
  }
}

void leftlevel() {
  Serial.println("Left Level");
  for (int i = 0; i < 4; i++) {
    digitalWrite(dirPinL, HIGH);
    for (int x = 0; x < 2000; x++) {
      if (checkForStop()) return;
      digitalWrite(stepPinL, HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPinL, LOW);
      delayMicroseconds(50);
    }
    delay(50);
  }
}

void rightlevel() {
  Serial.println("Right Level");
  for (int i = 0; i < 4; i++) {
    digitalWrite(dirPinR, HIGH);
    for (int x = 0; x < 2000; x++) {
      if (checkForStop()) return;
      digitalWrite(stepPinR, HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPinR, LOW);
      delayMicroseconds(50);
    }
    delay(50);
  }
}

// Conveyor movements to Magazine 2 (LOADING)
void conveyorFast() {
  Serial.println("Conveyor fast movement...");
  digitalWrite(rel_break, LOW);
  digitalWrite(dirPinC, LOW);
  for (int x = 0; x < 900; x++) {
    if (checkForStop()) return;
    digitalWrite(stepPinC, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPinC, LOW);
    delayMicroseconds(1000);
  }
  digitalWrite(rel_break, HIGH);
  Serial.println("Conveyor fast movement done");
}

void conveyorMicrostep() {
  Serial.println("Conveyor microstep movement...");

  digitalWrite(rel_break, LOW);
  delay(300);               // release brake and wait
  digitalWrite(dirPinC, LOW); // set forward direction

  // Perform 5 small microstep cycles
  for (int i = 1; i <= 5; i++) {
    digitalWrite(dirPinC, LOW);

    // 42 pulses per cycle
    for (int x = 0; x < 42; x++) {
      if (checkForStop()) return;   // allow emergency stop
      digitalWrite(stepPinC, HIGH);
      delayMicroseconds(2000);
      digitalWrite(stepPinC, LOW);
      delayMicroseconds(2000);
    }

    // interruptible wait between cycles
    unsigned long t0 = millis();
    while (millis() - t0 < 150) {   // 150 ms pause
      if (checkForStop()) return;
      delay(10);
    }
  }

  digitalWrite(rel_break, HIGH);   // engage brake
  Serial.println("Conveyor microstep movement complete.");
}

// === PROCESS CONTROLLER ===
void processOneStrip() {
  static unsigned long lastAction = 0;

  if (stopFlag) return;

  // FIXED: Use global processStep instead of local static step
  switch (processStep) {
    case 0:
      Serial.print("PROCESS STRIP ");
      Serial.println(stripIndex + 1);
      forward();
      lastAction = millis();
      processStep++;
      break;
    case 1:
      if (millis() - lastAction > 750) { reverse(); lastAction = millis(); processStep++; }
      break;
    case 2:
      if (millis() - lastAction > 750) { leftlevel(); lastAction = millis(); processStep++; }
      break;
    case 3:
      if (millis() - lastAction > 750) { conveyorFast(); lastAction = millis(); processStep++; }
      break;
    case 4:
      if (millis() - lastAction > 750) { conveyorMicrostep(); lastAction = millis(); processStep++; }
      break;
    case 5:
      if (millis() - lastAction > 750) { rightlevel(); lastAction = millis(); processStep++; }
      break;
    case 6:
      Serial.println("STRIP COMPLETED\n------------------");
      stripIndex++;

      // FIX: reset step + timing properly for next strip
      processStep = 0;
      lastAction = millis();

      if (stripIndex >= 20) {
        isRunning = false;
        Serial.println("ALL 20 STRIPS PROCESSED");
      } else {
        Serial.print("Preparing next strip... #");
        Serial.println(stripIndex + 1);
      }
      break;
  }
}