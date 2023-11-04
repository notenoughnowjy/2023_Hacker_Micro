import serial
import cv2
import threading
import queue

data_values = []
lock = threading.Lock()
result = 0
temp = 0
image_index_queue = queue.Queue()
stop_threads = False

def receive_data(ser):
    global result, temp, stop_threads
    i = 10
    while not stop_threads:
        data_str = ser.readline().decode().strip()
        print("data_str", data_str)
        if data_str.isdigit():
            data = int(data_str)
            with lock:
                data_values.append(data)
                if len(data_values) > 10:
                    data_values.pop(0)
                result = sum(data_values) / len(data_values)
                if result > temp and i >= 0:
                    i -= 1
                    temp = result
                elif result < temp and i <= 290:
                    i += 1
                    temp = result
                elif result == temp:
                    i = i
                    temp = result
                image_index_queue.put(i)
                print("i", i)

def load_and_display_image():
    global stop_threads
    while not stop_threads:
        if not image_index_queue.empty():
            i = image_index_queue.get()
            if i >= 0:
                try:
                    image = cv2.imread(fr'C:\pycharmdir\Hack_only_video\frame{i}.jpg')
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

port_number = 'COM13'
Serial_baud = 115200
ser = serial.Serial(port_number, Serial_baud, timeout=1)

data_thread = threading.Thread(target=receive_data, args=(ser,))
display_thread = threading.Thread(target=load_and_display_image)

data_thread.start()
display_thread.start()

data_thread.join()
display_thread.join()

cv2.destroyAllWindows()
