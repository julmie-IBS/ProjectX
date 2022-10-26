import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Get angles from Kalman IMU and convert into cartesian coordinates
#
#
#
#
#

n = 100 # length of input vector
ax = plt.axes(projection='3d')

# defining all 3 axes
z = np.linspace(0, 1, n)
x = z * np.sin(25 * z)
y = z * np.cos(25 * z)

# plotting
ax.plot3D(x, y, z, 'red')
plt.show()

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- Kalman section -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# IMU input section
# Generic
dt = 0.02                           # 20ms timesteps
CF_GainGyro = 0.95                  # complementary filter gain of gyroscope
CF_GainAcc = 1 - CF_GainGyro        # complementary filter gain of gyroscope
A_GAIN = 0.0573                     # [deg/LSB]
G_GAIN = 0.070                      # [deg/s/LSB]
var = 0.2 #tbd


# IMU Input Section
Gyr_data_raw = np.array([0,0,0])
Gyr_bias = np.array([0,0,0])
Acc_data_raw = np.array([0,0,0])
u_k = Gyr_data_raw   # initial state vector

# Init
A = np.array([
              [1, 0, 0, -dt, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, -dt, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, -dt, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, dt, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, dt, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, dt],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
              ])

B = np.array([
            [dt, 0, 0],
            [0, dt, 0],
            [0, 0, dt],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
            ])

u_k_prev = Gyr_data_raw

x_k_prev = np.concatenate(([0,0,0], Gyr_bias,[0,0,0],[0,0,0]))
P_k_prev = np.eye(12) * var

# Prediction
x_k = A @ x_k_prev + B @ u_k_prev
P_k = A @ P_k_prev @ A.T

# Correction







