import sys
import os
import cv2

def video_read(data):
    video_path = '/Users/junyeong/Downloads/해변가_영상만_30초.mp4'
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Camera open failed!')
        sys.exit()

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print("fps: ", video_fps)
x
    try:
        if not os.path.exists('Hack_only_video'):
            os.makedirs('Hack_only_video')
    except OSError:
        print('Error: Creating directory Hack_only_video')

    count = 0
    frame_count = 0
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            if frame_count % 6 == 0:  # 6프레임마다 이미지 저장
                cv2.imwrite('Hack_only_video/frame%d.jpg' % count, image)
                print('Saved frame number:', count)
                count += 1
            frame_count += 1
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

# 출력
data = 0
video_read(data)
