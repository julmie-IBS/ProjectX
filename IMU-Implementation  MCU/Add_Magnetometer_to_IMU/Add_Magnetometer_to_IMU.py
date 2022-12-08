import serial
import base64
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time


ser = serial.Serial('COM7', 500000, timeout=1,rtscts=1)
value=(ser.readline().decode("ascii"))


class IMU_Data:
    def __init__(self):
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_z = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0


    def get_IMU_data_form_COM(self,):
        serial_line = (ser.readline().decode("ascii"))
        if serial_line != b'':
            temp = serial_line.split(",")
        if len(temp)==6:
            self.acceleration_x = float(temp[0])
            self.acceleration_y = float(temp[1])
            self.acceleration_z = float(temp[2])
            self.gyro_x = float(temp[3])
            self.gyro_y = float(temp[4])
            self.gyro_z = float(temp[5][0:-2])  ## EOL Symbol
        else:
            return 1


IMU = IMU_Data()


for _ in range(10000):

        #t1=time.perf_counter()

        IMU.get_IMU_data_form_COM()
        plt.scatter(IMU.acceleration_z,0)
        plt.show(block=False)
        plt.pause(0.001)

        #print(IMU.gyro_x)
        #print(IMU.gyro_y)
        #print(IMU.gyro_z)

        #print(1/(time.perf_counter()-t1))

