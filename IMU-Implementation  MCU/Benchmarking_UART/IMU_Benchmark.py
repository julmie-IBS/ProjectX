import serial
import base64
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time

ser = serial.Serial('COM7', 1000000, timeout=0.000001)
value = (ser.readline().decode("ascii"))



for _ in range(10000):

    temp=str(int(np.random.rand()*10))
    temp="1"
    t1 = time.perf_counter()
    ser.write(temp.encode())
    """
    while True:
        if (ser.readline()).decode()=="a":
            print((time.perf_counter() - t1))
            print("gotit")
            break
    """

    while True:
        if ser.read(1) == "a".encode():
            print((time.perf_counter() - t1))
            print("gotit")
            break



    ser.readline()
    ser.readline()
    ser.readline()
    time.sleep(1)






