import serial
import base64
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time
import pygame
from math import *
import numpy as np



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
    def angle1(self):
        return atan2(self.acceleration_y,self.acceleration_z)


    def angle2(self):
        return atan2(self.acceleration_x, self.acceleration_z)






WINDOW_SIZE = 800
ROTATE_SPEED = 0.02
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()



cube_points = [n for n in range(8)]
cube_points[0] = [[-1], [-1], [0.1]]
cube_points[1] = [[1], [-1], [0.1]]
cube_points[2] = [[1], [1], [0.1]]
cube_points[3] = [[-1], [1], [0.1]]
cube_points[4] = [[-1], [-1], [-0.1]]
cube_points[5] = [[1], [-1], [-0.1]]
cube_points[6] = [[1], [1], [-0.1]]
cube_points[7] = [[-1], [1], [-0.1]]

cube_points=np.array(cube_points).reshape(8,3)


class Rotation():
    def __init__(self):
        pass

    def rotation_x(self,points,angle_x):
        rotation_x_matrix = np.array([[1, 0, 0],
                                      [0, cos(angle_x), -sin(angle_x)],
                                      [0, sin(angle_x), cos(angle_x)]])
        return np.matmul(points, rotation_x_matrix)



    def rotation_y(self,points,angle_y):
        rotation_y_matrix = np.array([[cos(angle_y), 0, sin(angle_y)],
                                      [0, 1, 0],
                                      [-sin(angle_y), 0, cos(angle_y)]])
        return np.matmul(points,rotation_y_matrix)



    def rotation_z(self,points,angle_z):
        rotation_z_matrix = np.array([[cos(angle_z), -sin(angle_z), 0],
                                      [sin(angle_z), cos(angle_z), 0],
                                      [0, 0, 1]])
        return np.matmul(points,rotation_z_matrix)

    def projection(self,points):
        projection_matrix = np.array([[1, 0],
                                      [0, 1],
                                      [0, 0]])
        return np.matmul(points, projection_matrix)






def connect_points(i, j, points):

    pygame.draw.line(window, (255, 255, 255), points[i], points[j])


# Main Loop
scale = 100
angle_x = angle_y = angle_z = 0
rot = Rotation()
IMU=IMU_Data()
IMU.get_IMU_data_form_COM()



while True:
    IMU.get_IMU_data_form_COM()
    angle_xnew=angle_x
    angle_ynew=angle_y+IMU.angle2()
    angle_znew=angle_z+IMU.angle1()
    #streck =streck+ np.array([0,0,1])*np.random.rand(1)*0.01
    clock.tick(60)
    window.fill((0, 0, 0))
    shapea , shapeb=cube_points.shape
    cube_points_mod=cube_points# + streck
    rotate_x1 = rot.rotation_x(cube_points_mod ,angle_xnew)
    rotate_y1 = rot.rotation_y(rotate_x1 ,angle_ynew)
    rotate_z1 = rot.rotation_z(rotate_y1 ,angle_znew)
    point_2d1 = rot.projection(rotate_z1)
    point_2d1 = point_2d1*100+400
    x = (point_2d1[0][0] * scale) + WINDOW_SIZE / 2
    y = (point_2d1[1][0] * scale) + WINDOW_SIZE / 2



    for point2d in point_2d1:
        pygame.draw.circle(window, (255, 0, 0), point2d, 5)

    connect_points(0, 1, point_2d1)
    connect_points(0, 3, point_2d1)
    connect_points(0, 4, point_2d1)
    connect_points(1, 2, point_2d1)
    connect_points(1, 5, point_2d1)
    connect_points(2, 6, point_2d1)
    connect_points(2, 3, point_2d1)
    connect_points(3, 7, point_2d1)
    connect_points(4, 5, point_2d1)
    connect_points(4, 7, point_2d1)
    connect_points(6, 5, point_2d1)
    connect_points(6, 7, point_2d1)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            angle_y = angle_x = angle_z = 0
        if keys[pygame.K_a]:
            angle_y += ROTATE_SPEED
        if keys[pygame.K_d]:
            angle_y -= ROTATE_SPEED
        if keys[pygame.K_w]:
            angle_x += ROTATE_SPEED
        if keys[pygame.K_s]:
            angle_x -= ROTATE_SPEED
        if keys[pygame.K_q]:
            angle_z -= ROTATE_SPEED
        if keys[pygame.K_e]:
            angle_z += ROTATE_SPEED

    pygame.display.update()

