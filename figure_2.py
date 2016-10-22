# -*- coding: utf-8 -*-
# MIT License (c) 2016 Ethan Nelson

import matplotlib.pyplot
import matplotlib.colors
import numpy

##  We first define a few constants for our drop size distribution.
n_0 = 8.0E3  # [m^-3 mm^-1]
R_0 = 1  # [mm h^-1]
lambda_R = 4.1 # [mm^-1]

##  We now define the array of droplet diameters.
dD = 0.005
drop_diameter = numpy.arange(0, 12 + dD, dD)  # [mm]

##  The z-R relationship is calculated.
effective_reflectivity = numpy.arange(0,66)  # [dBZ]
reflectivity = 10.0 ** (effective_reflectivity / 10.0)  # [mm^6 m^-3]
rain_rate = (reflectivity / 200.0) ** (1 / 1.6)  # [mm h^-1]

##  Next we calculate drop size distribution.
number_concentration = numpy.zeros([len(drop_diameter), len(rain_rate)])

for ix,diameter in enumerate(drop_diameter):
    for iy,rate in enumerate(rain_rate):
        number_concentration[ix,iy] = n_0 * numpy.exp(-1.0 * lambda_R * (rate / R_0) ** 0.21 * diameter)  # [m^-3 mm^-1]

fall_velocity = 386.6 * (drop_diameter / 10.0) ** 0.67  # [cm s^-1]

# Convert units
rain_rate /= 25.4  # [mm h^-1] to [in h^-1] 
fall_velocity *= (3600.0 / 160934.4)  # [cm s^-1] to [mi h^-1]
drop_diameter /= 25.4  # [mm] to [in]
number_concentration *= (2.54 ** 4.0 / 1E5)  # [m^-3 mm^-1] to [in^-3 in^-1]

fig = matplotlib.pyplot.figure(figsize=(10,6))

# Plotting the z-R relationship
plot = matplotlib.pyplot.plot(effective_reflectivity, rain_rate, linewidth=5, color='black')

matplotlib.pyplot.xlim([-0.75,64])
matplotlib.pyplot.ylim([-0.25,15])

matplotlib.pyplot.xlabel('Reflectivity [dBZ]',fontsize=18)
matplotlib.pyplot.ylabel('Rain Rate [in hr$^{-1}$]', fontsize=18)
matplotlib.pyplot.title('Remotely Sensing Rain Rates with Radar', fontsize=20)

# Plotting the DSD
subfig1 = matplotlib.pyplot.axes([0.525, 0.5, 0.25, 0.3])
matplotlib.pyplot.pcolormesh(drop_diameter, rain_rate, numpy.rot90(number_concentration), cmap=matplotlib.pyplot.get_cmap('gist_earth_r'), vmax=3.1)

matplotlib.pyplot.xlim([0, 0.06])
matplotlib.pyplot.ylim([0, 5])

matplotlib.pyplot.xticks(numpy.arange(0,0.08,0.02))

matplotlib.pyplot.xlabel('Diameter [in]', fontsize=14)
matplotlib.pyplot.ylabel('Rain Rate [in hr$^{-1}$]', fontsize=14)
matplotlib.pyplot.title('Drop Size Distribution', fontsize=16)

cbar_ax = matplotlib.pyplot.axes([0.8, 0.5, 0.03, 0.3])
tick_locs = numpy.arange(0,3.5,0.5)
cbar = matplotlib.pyplot.colorbar(orientation='vertical', cax=cbar_ax, ticks=tick_locs)
cbar.set_label('Drop Concentration [in$^{-4}$]', fontsize=12)

# Plotting the fall speeds
subfig2 = matplotlib.pyplot.axes([0.1625, 0.5, 0.25, 0.3])
matplotlib.pyplot.plot(drop_diameter, fall_velocity, linewidth=3, color='#d95f0e')

matplotlib.pyplot.xlim([0, 0.06])
matplotlib.pyplot.ylim([0, 2.5])

matplotlib.pyplot.xticks(numpy.arange(0,0.08,0.02))
matplotlib.pyplot.yticks(numpy.arange(0,3.0,0.5))

matplotlib.pyplot.xlabel('Diameter [in]', fontsize=14)
matplotlib.pyplot.ylabel('Speed [mph]', fontsize=14)
matplotlib.pyplot.title('Fall Speed', fontsize=16)

matplotlib.pyplot.tight_layout()

matplotlib.pyplot.savefig('/home/enelson/figures/physics_today_fig3.png', dpi=450)
matplotlib.pyplot.show()
