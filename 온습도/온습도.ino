int sensorPin = A0;  // 아날로그 핀에 수위 센서 연결
int sensorValue = 0;

void setup() {
  Serial.begin(9600);  // 시리얼 통신 속도 설정 (파이썬 코드와 일치해야 함)
}

void loop() {
  sensorValue = analogRead(sensorPin);                // 아날로그 핀에서 수위 값을 읽음
  int waterLevel = map(sensorValue, 0, 730, 0, 100);  // 센서 값 범위를 원하는 범위로 매핑

  if (waterLevel >= 100) {
    waterLevel = 100;  // 수위가 100% 이상인 경우 100%로 제한
  }
  // 아두이노에서 수위 데이터를 파이썬으로 전송

  Serial.println(waterLevel);


  delay(300);  // 300ms 대기
}
