import numpy as np
import matplotlib.pyplot as plt
import pyromat as pyro
import math as math


P_RATIO_MAX = 20        # P1/P2
GAMMA = 1.4
# Ambient
T0 = 273.15 + 10        # KELVIN
T_max = 273.15 + 1000   # KELVIN
P0 = 101 * 1000  # Pa
DELTA_P_RATIO = 1
p_ratio_1 = [i * DELTA_P_RATIO for i in range(1, P_RATIO_MAX)]
v_ratio_1 = [i ** (-GAMMA) for i in p_ratio_1]

plt.plot(v_ratio_1, p_ratio_1)
plt.show()



