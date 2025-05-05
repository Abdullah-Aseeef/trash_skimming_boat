import socket
import cv2
import numpy as np
import struct

CAMERA_IP = 'laptop_ip' 
CAMERA_PORT = 8000            
COMMAND_PORT = 9000           

# CSI Camera Setup - Can change resolution to improve latency
gst_str = ("nvarguscamerasrc ! "
           "video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! "
           "nvvidconv flip-method=0 ! "
           "video/x-raw, format=BGRx ! "
           "videoconvert ! "
           "video/x-raw, format=BGR ! appsink")
cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000)) 
server_socket.listen(1)
print(f"Waiting for connection from {CAMERA_IP}...")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} established!")

command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_socket.bind(('0.0.0.0', COMMAND_PORT))
command_socket.listen(1)
print(f"Waiting for control commands from {CAMERA_IP} on port {COMMAND_PORT}...")

control_socket, control_address = command_socket.accept()
print(f"Connection from control socket {control_address} established!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, frame_encoded = cv2.imencode('.jpg', frame, encode_param)
    data = frame_encoded.tobytes()

    size = len(data)
    client_socket.sendall(struct.pack(">L", size))  
    client_socket.sendall(data) 

    command = control_socket.recv(1024).decode('utf-8')
    if command:
        print(f"Received command: {command}")

        if command == "move forward":
            print("Moving boat forward...")
            # Will put logic for actual arduino to accept serial commands here
        elif command == "turn left":
            print("Turning boat left...")
            # Will put logic for actual arduino to accept serial commands here
        elif command == "turn right":
            print("Turning boat right...")
            # Will put logic for actual arduino to accept serial commands here
        else:
            print("Unknown command.")

    # may need sleep here too to ensure the boat actually moves before sending the next frame

cap.release()
client_socket.close()
command_socket.close()
server_socket.close()
