import serial
import time


ser = serial.Serial('/dev/ttyUSB0',115200)

time.sleep(1)

print(ser.readline())

print("Init serial ",ser.name)

ser.write(b"R10L10\r\n")

time.sleep(0.1)

print(ser.readline())

ser.close
