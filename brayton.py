import numpy as np
import matplotlib.pyplot as plt
import math as math


# Constants
GAMMA = 1.4
R = 0.08205746   # L atm / K mol
A = 1   # m^2
h = 1   #m
DELTA_P = 1

# Initial Conditions
T0 = 273.15 + 10        # KELVIN
P0 = 1  # atm
V0 = 1   # L
N = P0 * V0 / (R * T0)

# Constraints
P_RATIO_MAX = 20        # P1/P2
T_max = 273.15 + 1000   # KELVIN

# Stage 1 (given)
p1 = P0
t1 = T0
v1 = N * R * t1 / p1

# stage 2
p2 = p1 * P_RATIO_MAX
v2 = v1 * (p1/p2)**(1/GAMMA)
t2 = t1 * (v1/v2)**(GAMMA - 1)

# stage 3
p3 = p2
v3 = N * R * T_max / p3
t3 = t2 * v3 / v2

# stage 4
p4 = p1
v4 = v3 * (p3/p4)**(1/GAMMA)
t4 = t3 * (v3/v4)**(GAMMA-1)

pressure_1_2 = [i * DELTA_P for i in range(p1, p2)]
data_size = len(pressure_1_2)
volume_1_2 = np.ones(data_size)


# initilize volume array
volume_1_2[0] = v1
count = 1
while count < data_size:
    volume_1_2[count] = volume_1_2[count-1] * (pressure_1_2[count-1]/pressure_1_2[count])**(1/GAMMA)
    count += 1

v_ratio_2 = [(i) ** (-GAMMA) + A * h for i in pressure_1_2]


plt.plot(volume_1_2, pressure_1_2)
plt.show()











# DELTA_P_RATIO = 1
#
# # 1-2
# p_ratio_1 = [i * DELTA_P_RATIO for i in range(1, P_RATIO_MAX)]
# v_ratio_1 = [i ** (-GAMMA) for i in p_ratio_1]
#
# plt.plot(v_ratio_1, p_ratio_1)
#
# # 3-4
# p_ratio_2 = [i * DELTA_P_RATIO for i in range(1, P_RATIO_MAX)]
# v_ratio_2 = [(i) ** (-GAMMA) + A * h for i in p_ratio_2]
#
# plt.plot(v_ratio_2, p_ratio_2, 'red')
#
# plt.show()



