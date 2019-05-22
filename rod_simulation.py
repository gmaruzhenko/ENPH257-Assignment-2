#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

import numpy as np
import matplotlib.pyplot as plt
import math as math

# Constants
RODLENGTH = .3     # meters
RADIUS = .01         # meters
HIGHTEMP = 50 + 273.15   # Kelvin
ROOMTEMP = 20 + 273.15   # Kelvin
TIME_LIMIT = 600

HEAT_CAPACITY = 921.096   # c  J/kg K
DENSITY = 2830          # p kg/m^3
CONDUCTIVITY = 205.0  # k W/(m K)

POWERIN = 10        # W
EMISSIVITY = 1
BOLTZ = 5.67*10**(-8)   # W/m^2/k^4
CONVECTION = 5      # kc W/m^2/K

TIME_STEP = .05     # in seconds
SLICES = 40
SLICE_SIZE = RODLENGTH / SLICES

END_OF_BAR_SURFACE_AREA = math.pi * RADIUS ** 2
CYLINDER_SURFACE_AREA = 2 * math.pi * RADIUS * SLICE_SIZE

DENOMINATOR = HEAT_CAPACITY * DENSITY * math.pi * RADIUS**2 * SLICE_SIZE

# Helper functions


def temp_change_convection(slice_temp, index):
    if index == SLICES-1:
        return -CONVECTION * (slice_temp - ROOMTEMP) / (HEAT_CAPACITY * DENSITY)
    else:
        return -2 * CONVECTION * (slice_temp - ROOMTEMP) / (HEAT_CAPACITY * DENSITY * RADIUS)


def temp_change_radiative(slice_temp, index):
    if index == SLICES-1:
        power_loss = (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * EMISSIVITY * BOLTZ * (slice_temp ** 4 - ROOMTEMP ** 4)
    else:
        power_loss = CYLINDER_SURFACE_AREA * EMISSIVITY * BOLTZ * (currentTemp ** 4 - ROOMTEMP ** 4)
    return -power_loss / DENOMINATOR


def double_differential_conduction(array, index):
    if index == 0:
        doublediff = (-array[index] + array[index + 1]) / (SLICE_SIZE ** 2)
    elif index == SLICES - 1:
        doublediff = (-array[index] + array[index - 1]) / (SLICE_SIZE ** 2)
    else:
        doublediff = (array[index - 1] - 2 * array[index] + array[index + 1]) / (SLICE_SIZE ** 2)
    return doublediff


def temp_change_power_in(index):
    if index == 0:
        temp_change = POWERIN * TIME_STEP / DENOMINATOR
    else:
        temp_change = 0
    return temp_change


# set up arrays
rodTempArray = np.ones(SLICES) * ROOMTEMP
x_axis_for_plot = [i * SLICE_SIZE for i in range(0, SLICES)]


time = 0
while time < TIME_LIMIT:
    slice_index = 0
    previous_itteration = rodTempArray
    while slice_index < SLICES:
        currentTemp = rodTempArray[slice_index]
        temperatureChangeConduction = CONDUCTIVITY * TIME_STEP * double_differential_conduction(rodTempArray,
                                                                                                slice_index) / (
                                                  HEAT_CAPACITY * DENSITY)
        # apply change to current segment of array
        dt = temperatureChangeConduction + temp_change_power_in(slice_index) + temp_change_convection(currentTemp, slice_index) + temp_change_radiative(currentTemp, slice_index)
        rodTempArray[slice_index] += dt

        slice_index += 1

    # if abs(sum(rodTempArray) - sum(previous_itteration)) < 0.0001:
    #     print(float(sum(rodTempArray)) - float(sum(previous_itteration)))
    #     print("steady state reached")
    #     print(time)
    time += TIME_STEP

plt.plot(x_axis_for_plot, rodTempArray)
plt.title('AL Rod Heat Transfer Simulation')
plt.xlabel('Position (meters)')
plt.ylabel('Temperature (kelvin)')
plt.show()









