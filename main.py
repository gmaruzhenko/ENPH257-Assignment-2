import numpy as np
import matplotlib.pyplot as plt
import math as math

RODLENGTH = .3     # meters
RADIUS = .02         # meters
HIGHTEMP = 50 + 273.15   # Kelvin
ROOMTEMP = 20 + 273.15   # Kelvin

# Constants
HEAT_CAPACITY = 921.096   # c  J/kg K
DENSITY = 2830          # p kg/m^3
CONDUCTIVITY = 205.0  # k W/(m K)

POWERIN = 10        # W
EMISSIVITY = 1
BOLTZ = 5.67*10**(-8)   # W/m^2/k^4
CONVECTION = 11      # kc W/m^2/K

TIME_STEP = .05     # in seconds
SLICES = 40
SLICE_SIZE = RODLENGTH / SLICES

END_OF_BAR_SURFACE_AREA = math.pi * RADIUS ** 2
CYLINDER_SURFACE_AREA = 2 * math.pi * RADIUS * SLICE_SIZE

driver()


def convection_power_loss(slice_temp, index):
    if index == SLICES-1:
        return (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * CONVECTION * (slice_temp - ROOMTEMP)
    else:
        return CYLINDER_SURFACE_AREA * CONVECTION * (slice_temp - ROOMTEMP)


def radiative_power_loss(slice_temp, index):
    if index == SLICES-1:
        return (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * EMISSIVITY * BOLTZ * (slice_temp ** 4 - ROOMTEMP ** 4)
    else:
        return CYLINDER_SURFACE_AREA * EMISSIVITY * BOLTZ * (currentTemp ** 4 - ROOMTEMP ** 4)


def double_conduction_differential(array, index):
    if index == 0:
        doublediff = (-array[index] + array[index + 1]) / (SLICE_SIZE ** 2)
    elif index == SLICES - 1:
        doublediff = (-array[index] + array[index - 1]) / (SLICE_SIZE ** 2)
    else:
        doublediff = (array[index - 1] - 2 * array[index] + array[index + 1]) / (SLICE_SIZE ** 2)
    return doublediff


def temp_change_power_in(index):
    if index == 0:
        temp_change = POWERIN * TIME_STEP / denominator
    else:
        temp_change = 0
    return temp_change

def driver():
    # set up arrays
    rodTempArray = np.ones(SLICES) * ROOMTEMP
    x_axis_for_plot = [i * SLICE_SIZE for i in range(0, SLICES)]

    denominator = (HEAT_CAPACITY * DENSITY * math.pi * RADIUS * SLICE_SIZE)

    time = 0
    while time < 16000:
        slice_index = 0
        previous_itteration = rodTempArray
        while slice_index < SLICES:
            currentTemp = rodTempArray[slice_index]
            totalTempChangePowerLoss = (convection_power_loss(currentTemp, slice_index) + radiative_power_loss(
                currentTemp, slice_index)) * TIME_STEP / denominator
            temperatureChangeConduction = CONDUCTIVITY * TIME_STEP * double_conduction_differential(rodTempArray,
                                                                                                    slice_index) / (
                                                      HEAT_CAPACITY * DENSITY)

            # apply change to current segment of array
            dt = temperatureChangeConduction + temp_change_power_in(slice_index) - totalTempChangePowerLoss
            rodTempArray[slice_index] += dt

            slice_index += 1

        if abs(sum(rodTempArray) / SLICES + sum(previous_itteration) / SLICES < 0.001):
            print("steady state reached")
            print(time)
        time += TIME_STEP

    plt.plot(x_axis_for_plot, rodTempArray)
    plt.show()









