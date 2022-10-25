import numpy as np
import math

#
### Kalman filtering of IMU data
### Reference
### http://tom.pycke.be/mav/71/kalman-filtering-of-imu-data/
#

##### INIT #####
# Generic
dt = 0.02                           # 20ms timesteps
CF_GainGyro = 0.95                  # complementary filter gain of gyroscope
CF_GainAcc = 1 - CF_GainGyro        # complementary filter gain of gyroscope
A_GAIN = 0.0573                     # [deg/LSB]
G_GAIN = 0.070                      # [deg/s/LSB]

# IMU Input Section
Gyr_data_raw = np.array([0,0,0])
Gyr_bias = np.array([0,0,0])
Acc_data_raw = np.array([0,0,0])
u_k = Gyr_data_raw   # initial state vector

# State space model
x_k = np.concatenate(([0,0,0], Gyr_bias))
A = np.array([[1,0,0,-dt,0,0],[0,1,0,0,-dt,0],[0,0,1,0,0,-dt],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]])
B = np.array([[dt,0,0],[0,dt,0],[0,0,dt],[0,0,0],[0,0,0],[0,0,0]])   # Input matrix
C = np.array([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])
# Prediction
x_k1 = A @ x_k + B @ u_k

# Convert accelerometer output to angle
acc_angle_x = (math.atan2(Acc_data_raw(1), Acc_data_raw(2)) + np.pi) * np.pi/180
acc_angle_y = (math.atan2(Acc_data_raw(2), Acc_data_raw(0)) + np.pi) * np.pi/180
acc_angle_z = (math.atan2(Acc_data_raw(0), Acc_data_raw(1)) + np.pi) * np.pi/180

acc_angle_x = acc_angle_x - 180.0
if acc_angle_y > 90.0:
    acc_angle_y = acc_angle_y - 270.0
else:
    acc_angle_y = acc_angle_y + 90.0
y = [acc_angle_x,acc_angle_y,acc_angle_z]

# Innovation (Difference between the second value and the value predicted by our model)
Inn = y - np.matmul(C,x_k1)

# Covariance
s = C @ P @ C.T + Sz

# Kalman Gain
K = A @ P @ C.T @ np.linalg.inv(s)

# Correction (Correct state prediction)
x_next = x_k1 + K @ Inn

# Covariance calculation
P = A @ P @ A.T - K @  C @ P @ A.T + Sw









# Apply Complementary filter
CF_angle = CF_GainGyro * (CF_angle_x + [x * dt for x in gyr] * dt) + [x * CF_GainAcc for x in acc_angle]
