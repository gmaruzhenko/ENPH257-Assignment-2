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
TIME_LIMIT = 2000

HEAT_CAPACITY = 921.096   # c  J/kg K
DENSITY = 2830.0          # p kg/m^3
CONDUCTIVITY = 205.0  # k W/(m K)

POWERIN = 10.0        # W
EMISSIVITY = 0.89
BOLTZ = 5.67*10**(-8)   # W/m^2/k^4
CONVECTION = 9.      # kc W/m^2/K

TIME_STEP = 0.5    # in seconds
SLICES = 40
SLICE_SIZE = RODLENGTH / SLICES

END_OF_BAR_SURFACE_AREA = math.pi * RADIUS ** 2
CYLINDER_SURFACE_AREA = 2 * math.pi * RADIUS * SLICE_SIZE

DENOMINATOR = HEAT_CAPACITY * DENSITY * math.pi * RADIUS**2 * SLICE_SIZE

# Helper functions


def temp_change_convection(slice_temp, index):
    # update arrays
    power_loss_convection(slice_temp, index)
    if index == SLICES-1 or index == 0:
        return -CONVECTION * (slice_temp - ROOMTEMP) / (HEAT_CAPACITY * DENSITY)
    else:
        return -2 * CONVECTION * (slice_temp - ROOMTEMP) / (HEAT_CAPACITY * DENSITY * RADIUS)


def power_loss_convection(slice_temp, index):
    if index == SLICES-1:
        power_loss_c = -CONVECTION * (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * (slice_temp - ROOMTEMP)
    else:
        power_loss_c = -CONVECTION * CYLINDER_SURFACE_AREA * (slice_temp - ROOMTEMP)
    convection_one_timestep_array[index] = - power_loss_c
    return power_loss_c


def power_loss_radiative(slice_temp, index):
    if index == SLICES-1:
        power_loss = (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * EMISSIVITY * BOLTZ * (slice_temp ** 4 - ROOMTEMP ** 4)
    else:
        power_loss = CYLINDER_SURFACE_AREA * EMISSIVITY * BOLTZ * (currentTemp ** 4 - ROOMTEMP ** 4)
    radiative_one_timestep_array[index] = power_loss
    return -power_loss


def update_heating_array(index):
    heating_one_timestep_array[index] = POWERIN - radiative_one_timestep_array[index] - convection_one_timestep_array[index]


def temp_change_radiative(slice_temp, index):
    return power_loss_radiative(slice_temp, index) / DENOMINATOR


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


def update_power_budget_arrays(time):
    convectionArray_total[int(time / TIME_STEP)] = sum(convection_one_timestep_array)
    radiationArray_total[int(time / TIME_STEP)] = sum(radiative_one_timestep_array)
    heatingArray_total[int(time / TIME_STEP)] = POWERIN - radiationArray_total[int(time / TIME_STEP)] - \
                                                convectionArray_total[int(time / TIME_STEP)]


def plot_power_budget():
    plt.plot(time_scale, convectionArray_total)
    plt.plot(time_scale, radiationArray_total)
    plt.plot(time_scale, heatingArray_total)
    plt.title('Power Budget')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.legend(['Convection', 'Radiation', 'Heating'])
    plt.show()


def plot_temp_sim():
    plt.plot(x_location_on_rod, rodTempArray)
    plt.title('AL Rod Heat Transfer Simulation')
    plt.xlabel('Position (meters)')
    plt.ylabel('Temperature (kelvin)')
    plt.show()


# set up arrays
rodTempArray = np.ones(SLICES) * ROOMTEMP
x_location_on_rod = [i * SLICE_SIZE for i in range(0, SLICES)]
time_scale = [i * TIME_STEP for i in range(0, int(TIME_LIMIT/TIME_STEP))]
heating_one_timestep_array = np.ones(SLICES)
radiative_one_timestep_array = np.ones(SLICES)
convection_one_timestep_array = np.ones(SLICES)
convectionArray_total = np.ones(int(TIME_LIMIT/TIME_STEP))
radiationArray_total = np.ones(int(TIME_LIMIT/TIME_STEP))
heatingArray_total = np.ones(int(TIME_LIMIT/TIME_STEP))

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

        update_heating_array(slice_index)

        slice_index += 1

    update_power_budget_arrays(time)
    time += TIME_STEP

plot_temp_sim()

plot_power_budget()








