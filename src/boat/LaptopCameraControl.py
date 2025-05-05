import socket
import cv2
import numpy as np
import struct
import time
from ultralytics import YOLO
import torch

JETSON_IP = '192.168.1.26'  
JETSON_PORT = 8000            
COMMAND_PORT = 9000           
CONF_THRESH = 0.2 # Will change on actual deployment       

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = YOLO("best.pt").to(device)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((JETSON_IP, JETSON_PORT))
print(f"Connected to Jetson at {JETSON_IP}:{JETSON_PORT}")

command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.connect((JETSON_IP, COMMAND_PORT))
print(f"Connected to control port at {JETSON_IP}:{COMMAND_PORT}")

while True:
    data_len = struct.unpack(">L", client_socket.recv(4))[0]
    data = b""
    while len(data) < data_len:
        data += client_socket.recv(4096)

    frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    start_time = time.time()


    results = model(frame)  # Perform inference on the received frame

    end_time = time.time()
    print(f"Inference time: {(end_time - start_time) * 1000:.2f} ms")

    # --- Get Results ---
    boxes = results[0].boxes.xyxy.cpu().numpy()  
    confidences = results[0].boxes.conf.cpu().numpy()  
    class_ids = results[0].boxes.cls.cpu().numpy()  

    if len(boxes) > 0:

        filtered_boxes = [(box, conf) for box, conf in zip(boxes, confidences) if conf > CONF_THRESH]
        
        if filtered_boxes:

            largest_box, confidence = max(filtered_boxes, key=lambda x: x[1]) # may change this logic to find the largest bounding box to go to the closest object

            x1, y1, x2, y2 = largest_box[:4]

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            label = f"Class {int(class_ids[np.argmax(confidences)])}: {confidence:.2f}"

            cv2.putText(frame, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if x1 < frame.shape[1] / 3:
                command = "turn left"
            elif x2 > frame.shape[1] * 2 / 3:
                command = "turn right"
            else:
                command = "move forward"

            print(f"Sending command: {command}")
            command_socket.sendall(command.encode('utf-8'))
        else:
            print("No valid object detected, sending 'move forward'.")
            command_socket.sendall("move forward".encode('utf-8'))
    else:
        print("No object detected, sending 'move forward'.")
        command_socket.sendall("move forward".encode('utf-8'))

    cv2.imshow("Detected Frame", frame)
    # time.sleep(1) # sleep can be useful to make sure boat responds to an input properly

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
command_socket.close()
cv2.destroyAllWindows()
