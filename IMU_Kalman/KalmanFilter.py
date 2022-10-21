import numpy as np
import math

##### INIT #####
# Generic
dt = 0.01                           # 10ms timesteps
CF_GainGyro = 0.95                  # complementary filter gain of gyroscope
CF_GainAcc = 1 - CF_GainGyro        # complementary filter gain of gyroscope
A_GAIN = 0.0573                     # [deg/LSB]
G_GAIN = 0.070                      # [deg/s/LSB]

# Kalman Filter
Q_angle  =  0.01
Q_gyro   =  0.0003
R_angle  =  0.01
x_bias = 0
y_bias = 0
XP_00 = 0
XP_01 = 0
XP_10 = 0
XP_11 = 0
YP_00 = 0
YP_01 = 0
YP_10 = 0
YP_11 = 0
CF_angle_x = 0.0
CF_angle_y = 0.0
CF_angle_z = 0.0
KF_angle_x = 0.0
KF_angle_y = 0.0
KF_angle_z = 0.0
gyro_angle_x = 0.0
gyro_angle_y = 0.0
gyro_angle_z = 0.0
acc_angle_x = 0.0
acc_angle_y = 0.0

# Acc und Gyro Input section
gyr_raw = [0,0,0]
acc_raw = [0,0,0]

# ---------------------------------
# Init
gyr_cal_angle_x = 0.0
gyr_cal_angle_y = 0.0
gyr_cal_angle_z = 0.0

# Convert raw gyro data to angular frequency
gyr_x = gyr_raw[0] * G_GAIN
gyr_y = gyr_raw[1] * G_GAIN
gyr_z = gyr_raw[2] * G_GAIN

# Calculate gyroscope angles
gyr_angle_x = gyr_cal_angle_x + gyr_x * dt
gyr_angle_y = gyr_cal_angle_y + gyr_y * dt
gyr_angle_z = gyr_cal_angle_z + gyr_z * dt

acc_angle_x = (math.atan2(acc_raw(1), acc_raw(2)) + np.pi) * np.pi/180
acc_angle_y = (math.atan2(acc_raw(2), acc_raw(0)) + np.pi) * np.pi/180
acc_angle_z = (math.atan2(acc_raw(0), acc_raw(1)) + np.pi) * np.pi/180

acc_angle_x = acc_angle_x - 180.0
if acc_angle_y > 90.0:
    acc_angle_y = acc_angle_y - 270.0
else:
    acc_angle_y = acc_angle_y + 90.0
    

# Apply Complementary filter
CF_angle_x = CF_GainGyro * (CF_angle_x + gyr_x * dt) + CF_GainAcc * acc_angle_x;
CF_angle_y = CF_GainGyro * (CF_angle_y + gyr_y * dt) + CF_GainAcc * acc_angle_y;
CF_angle_x = CF_GainGyro * (CF_angle_z + gyr_z * dt) + CF_GainAcc * acc_angle_z;
