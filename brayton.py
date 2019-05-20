import numpy as np
import matplotlib.pyplot as plt
import math as math


P_RATIO_MAX = 20        # P1/P2
GAMMA = 1.4
# Ambient
T0 = 273.15 + 10        # KELVIN
T_max = 273.15 + 1000   # KELVIN
P0 = 1  # atm
V0 = 1   # L
A = 1   # m^2
h = 1   #m
DELTA_P_RATIO = 1

# 1-2
p_ratio_1 = [i * DELTA_P_RATIO for i in range(1, P_RATIO_MAX)]
v_ratio_1 = [i ** (-GAMMA) for i in p_ratio_1]

plt.plot(v_ratio_1, p_ratio_1)

# 3-4
p_ratio_2 = [i * DELTA_P_RATIO for i in range(1, P_RATIO_MAX)]
v_ratio_2 = [(i) ** (-GAMMA) + A * h for i in p_ratio_2]

plt.plot(v_ratio_2, p_ratio_2, 'red')

plt.show()



