# first cell starts at 50 and rest at 20 but no heat bath

import numpy as np
import matplotlib.pyplot as plt

# in mm
RODLENGTH = 3000
RADIUS = 20
# in Celcius
HIGHTEMP = 50
ROOMTEMP = 20

# Constants
HEATCAPACITY = 0.9  # c     0.900 J/g K
DENSITY = 0.0027*1000**3 # p in m now g/m3 --> p g/mm3 ----->    2.70 g/cm3
CONDUCTIVITY = 0.237*1000  # k in m now W/(m·K) ---> k  W/(mm·K) --->   237 W/(m·K)

POWERIN = 10 # W
EMISSIVITY = 1
CONVECTION = 5 # W/m^2/K

# in seconds
TIMESTEP = .005
SLICES = 40
SLICESIZE = RODLENGTH / SLICES

# set up arrays
rodTempArray = np.ones(SLICES) * ROOMTEMP
my_new_list = [i * SLICESIZE for i in range(0, SLICES)]

# add heated segment
rodTempArray[0] = 50


time = 0
while time < 100:  # rodTempArray[2]!=40)
    # reset index
    sliceindex = 0

    while sliceindex < SLICES:

        # create the double diff
        if sliceindex == 0:
            # print "start--------------------------------------------------"
            doublediff = (-rodTempArray[sliceindex] + rodTempArray[sliceindex + 1]) / SLICESIZE

        elif sliceindex == SLICES - 1:
            # print "end-----------------------------------------------------------------"
            doublediff = (-rodTempArray[sliceindex] + rodTempArray[sliceindex - 1]) / SLICESIZE

        else:
            doublediff = (rodTempArray[sliceindex - 1] - 2 * rodTempArray[sliceindex] + rodTempArray[
                sliceindex + 1]) / (SLICESIZE ** 2)

        # apply change to current segment of array
        rodTempArray[sliceindex] += CONDUCTIVITY * TIMESTEP * doublediff / (HEATCAPACITY * DENSITY)

        # Sanity checker for temperature
        # averageTemp=sum(rodTempArray)/SLICES
        # if time%10 == 0:
        # print averageTemp


        sliceindex += 1

    time += TIMESTEP

plt.plot(my_new_list, rodTempArray)
plt.show()