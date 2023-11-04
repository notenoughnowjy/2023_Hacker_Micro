#define trig  8
#define echo  9
void setup() {
  Serial.begin(115200);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
}
unsigned long prev = 0;
unsigned long prev2 = 0;
void loop() {

  long duration, distance;

  if (millis() - prev > 1000) {
    prev = millis();
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);  // Trig 핀을 HIGH로 설정
    delayMicroseconds(10);
    digitalWrite(trig, LOW);  // Trig 핀을 LOW로 설정

    duration = pulseIn(echo, HIGH);  // 펄스의 지속 시간을 측정
    distance = ((float)(340 * duration / 10000) / 2);
  }
  if (millis() - prev2 > 100){
      prev2 = millis();
      Serial.println(distance);
  }
}
