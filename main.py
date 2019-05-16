import numpy as np
import matplotlib.pyplot as plt
import math as math

RODLENGTH = .3     # meters
RADIUS = .02         # meters
HIGHTEMP = 50 + 273.15   # Kelvin
ROOMTEMP = 20 + 273.15   # Kelvin

# Constants
HEATCAPACITY = 921.096   # c  J/kg K
DENSITY = 2830          # p kg/m^3
CONDUCTIVITY = 205.0  # k W/(m K)

POWERIN = 10        # W
EMISSIVITY = 1
BOLTZ = 5.67*10**(-8)   # W/m^2/k^4
CONVECTION = 5      # kc W/m^2/K

TIMESTEP = .05     # in seconds
SLICES = 40
SLICESIZE = RODLENGTH / SLICES

END_OF_BAR_SURFACE_AREA = math.pi * RADIUS ** 2
CYLINDER_SURFACE_AREA = 2 * math.pi * RADIUS * SLICESIZE

# set up arrays
rodTempArray = np.ones(SLICES) * ROOMTEMP
x_axis_for_plot = [i * SLICESIZE for i in range(0, SLICES)]

denominator = (HEATCAPACITY * DENSITY * math.pi * RADIUS * SLICESIZE)


def convection_power_loss(slice_temp, is_end):
    if is_end:
        return (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * CONVECTION * (slice_temp - ROOMTEMP)
    else:
        return CYLINDER_SURFACE_AREA * CONVECTION * (slice_temp - ROOMTEMP)


def radiative_power_loss(slice_temp, is_end):
    if is_end:
        return (CYLINDER_SURFACE_AREA + END_OF_BAR_SURFACE_AREA) * EMISSIVITY * BOLTZ * (slice_temp ** 4 - ROOMTEMP ** 4)
    else:
        return CYLINDER_SURFACE_AREA * EMISSIVITY * BOLTZ * (currentTemp ** 4 - ROOMTEMP ** 4)


def temperature_change_for_slice_temp(slice):
    return


time = 0
while time < 500:  # rodTempArray[2]!=40)
    # reset index
    sliceindex = 0

    while sliceindex < SLICES:
        tempChangePowerIn = 0
        # Temperature of current slice
        currentTemp = rodTempArray[sliceindex]
        # create the double diff
        if sliceindex == 0:
            # heat first segment
            doublediff = (-rodTempArray[sliceindex] + rodTempArray[sliceindex + 1]) / SLICESIZE
            tempChangePowerIn = POWERIN * TIMESTEP / denominator
            radiativePowerLoss = radiative_power_loss(currentTemp, False)
            convectionPowerLoss = convection_power_loss(currentTemp, False)

        elif sliceindex == SLICES - 1:
            doublediff = (-rodTempArray[sliceindex] + rodTempArray[sliceindex - 1]) / SLICESIZE
            radiativePowerLoss = radiative_power_loss(currentTemp, True)
            convectionPowerLoss = convection_power_loss(currentTemp, True)

        else:
            doublediff = (rodTempArray[sliceindex - 1] - 2 * rodTempArray[sliceindex] + rodTempArray[sliceindex + 1]) / (SLICESIZE ** 2)
            radiativePowerLoss = radiative_power_loss(currentTemp, False)
            convectionPowerLoss = convection_power_loss(currentTemp, False)
        print(currentTemp)

        # power in and out
        totalTempChangePowerLoss = (convectionPowerLoss + radiativePowerLoss) * TIMESTEP / denominator
        # heat traveling between segments
        temperatureChangeConduction = CONDUCTIVITY * TIMESTEP * doublediff / (HEATCAPACITY * DENSITY)

        # apply change to current segment of array
        rodTempArray[sliceindex] += temperatureChangeConduction + tempChangePowerIn #- totalTempChangePowerLoss +

        sliceindex += 1

    time += TIMESTEP

plt.plot(x_axis_for_plot, rodTempArray)
plt.show()






