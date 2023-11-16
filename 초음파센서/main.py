import serial
import cv2
import threading
import queue
import numpy as np
from filterpy.kalman import KalmanFilter

data_values = []
lock = threading.Lock()
result = 0
temp = 0
image_index_queue = queue.Queue()
stop_threads = False

def receive_data(ser):
    global result, temp, stop_threads
    i = 10

    # 칼만 필터 초기화
    kf = KalmanFilter(dim_x=2, dim_z=1)
    kf.x = np.array([[0.],  # state
                     [0.]]) # velocity
    kf.F = np.array([[1.,1.],
                     [0.,1.]]) # state transition matrix
    kf.H = np.array([[1.,0.]])  # measurement function
    kf.P *= 1000.  # covariance matrix
    kf.R = 5  # state uncertainty
    kf.Q = Q_discrete_white_noise(2, dt=1., var=0.1)  # process uncertainty

    while not stop_threads:
        data_str = ser.readline().decode().strip()
        print("data_str", data_str)
        if data_str.isdigit():
            data = int(data_str)
            with lock:
                data_values.append(data)
                if len(data_values) > 10:
                    result = sum(data_values) / len(data_values)
                    data_values = []

                    # 칼만 필터 적용
                    kf.predict()
                    kf.update(result)
                    result = kf.x[0]

                if result > temp and i >= 0:
                    i -= 1
                    temp = result
                if result < temp and i <= 290:
                    i += 1
                    temp = result
                elif result == temp:
                    i = i
                    temp = result
                image_index_queue.put(i)
                print("i", i)

# 나머지 코드는 그대로...


def load_and_display_image():
    global stop_threads
    while not stop_threads:
        if not image_index_queue.empty():
            i = image_index_queue.get()
            if i >= 0:
                try:
                    image = cv2.imread(fr'C:\Users\yhyi\PycharmProjects\pythonProject\Hack_only_video\frame{i}.jpg')
                    if image is None:
                        raise FileNotFoundError
                except FileNotFoundError:
                    print(f"Could not load image with index {i}, loading default image.")
                    image = cv2.imread(fr'C:\pycharmdir\Hack_only_video\default.jpg')
                if image is not None:
                    window_name = 'image'
                    cv2.imshow(window_name, image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                stop_threads = True
                break

port_number = 'COM15'
Serial_baud = 115200
ser = serial.Serial(port_number, Serial_baud)

data_thread = threading.Thread(target=receive_data, args=(ser,))
display_thread = threading.Thread(target=load_and_display_image)

data_thread.start()
display_thread.start()

data_thread.join()
display_thread.join()

cv2.destroyAllWindows()
