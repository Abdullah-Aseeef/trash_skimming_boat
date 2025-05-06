import socket
import cv2
import numpy as np
import struct
import serial
import time

CAMERA_IP = '192.168.1.21' 
CAMERA_PORT = 8000            
COMMAND_PORT = 9000           

arduino_port = '/dev/ttyACM0'  # Adjust if necessary (check your system using `ls /dev/tty*`)
baud_rate = 9600

ser = serial.Serial(arduino_port, baud_rate)
print(f"Connected to Arduino Mega at {arduino_port}")

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
            ser.write('F'.encode('utf-8'))
        elif command == "turn left":
            print("Turning boat left...")
            ser.write('L'.encode('utf-8'))
        elif command == "turn right":
            print("Turning boat right...")
            ser.write('R'.encode('utf-8'))
        else:
            print("Unknown command.")
    time.sleep(1)
    # may need sleep here too to ensure the boat actually moves before sending the next frame

cap.release()
client_socket.close()
command_socket.close()
server_socket.close()
