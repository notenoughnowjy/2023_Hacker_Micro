import serial
import cv2  # OpenCV 라이브러리를 사용하여 영상 출력
import pygame

pygame.mixer.init()
pygame.init()

ser = serial.Serial('/dev/cu.usbmodem142201', 9600)  # 포트 이름을 아두이노의 포트 이름으로 변경

while True:
    data = ser.readline().strip()
    waterlevel = int(data)  # 수위 데이터를 정수로 변환

    if waterlevel >= 50:
        print(f"데이터가 {waterlevel}% 이상입니다")

        sound = pygame.mixer.Sound("/Users/boojin/PycharmProjects/pythonProject/videos/sound_test.wav")
        sound.play()

        # 동영상 파일을 플레이하려면 VideoCapture를 사용합니다.
        video = cv2.VideoCapture('/Users/boojin/PycharmProjects/pythonProject/videos/test_04.mov')
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow("Water Level Alert", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()
