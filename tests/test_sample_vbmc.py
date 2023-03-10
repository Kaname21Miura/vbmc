from vbmc import vbmc
from vbmc import angularyResolved,spatiallyResolved
import numpy as np
import matplotlib.pyplot as plt


# This is sample code for vbmc.
#
# vbmc can compute diffuse light transport
# for any voxel model. The voxel model is
# a 3-dimensional array, and integer voxel
# values from 0 to 255 are allowed. The voxel
# values must match the array number of the
# optical properties, and the optical properties
# of the model can be set with the set_params
# function.
#
# This sample file shows an example calculation
# for a multilayered medium with the following
# optical properties.
#
# | Layer | µ_a [/cm] |  µ_s [/cm] |  g  |   n   |   d   |
# |   1   |    1.     |     100    | 0.9 |  1.37 |  0.1  |
# |   2   |    1.     |     10     | 0.  |  1.37 |  0.1  |
# |   3   |    1.     |     10     | 0.7 |  1.37 |  0.2  |
#
# Here, the refractive index of air is assumed to be 1.
# and the medium size in the x-y direction is assumed
# to be semi-infinite.　The photon number was set to 1e6.
#
# Please refer to the "docs/mcml_result_multilayer_rdr_tdr.csv"
# or the following paper for the MCML results of the calculations.
#
# Reference
# Wang and Jacques,"Monte Carlo Modeling of Light Transport
# in Multi-layered Tissues in Standard C Lihong",(1992)
# URL: https://omlc.org/software/mc/mcml/MCman.pdf

nPh = 1e6
model = vbmc(nPh = nPh)
params = {
        'n':[1.37,1.37,1.37],
        'n_air':1.,
        'ma':[1,1,2],
        'ms':[100,10,10],
        'g':[0.9,0.,0.7],
        'end_point':False,
        'voxel_space':0.1,
}
voxel_model = np.zeros((1001,1001,4))
voxel_model[:,:,1] = 1
voxel_model[:,:,2:] = 2

# Voxel model setting
model.set_model(voxel_model)
# optical properties setting
model.set_params(**params)
# model build
model.build()

# start vbmc calculation
model.start()

# get_result()
#
# The result is in dictionary format with keys "p", "v",
# and "w", where p is a position vector, v is a direction
# vector, and w is a photon weight.
#
# The shape of p and v is (number of photons, 3), and the
# one-dimensional elements of the array are the xyz
# components of the vector. For example, p[:,0] is the x
# component of p, p[:,1] is the y component of p, and p[:,2]
# is the z component of p.
# On the other hand, the shape of w is a one-dimensional
# array of (number of photons).
res = model.get_result()

# Separation of diffuse reflection and transmission
# For a medium with a semi-infinite size in the xy direction,
# the direction vector in the final result implies reflection
# if it is in the negative z direction and transmission if it
# is in the positive z direction.

Rd_index = np.where(res['v'][:,2] < 0)[0] # Index of diffuse reflected photons
Td_index = np.where(res['v'][:,2] > 0)[0] # Index of diffuse transmitted photons

##### View Results #####
#
# Spatially resolved diffuse reflectance and transmittance
#
dr = 0.005
nn = 100
r,Rd_r = spatiallyResolved(
    res['p'][Rd_index],res['w'][Rd_index],nPh,nn,dr
)
r,Td_r = spatiallyResolved(
    res['p'][Td_index],res['w'][Td_index],nPh,nn,dr
)

plt.plot(r,Td_r,'-', c = 'k')
plt.yscale('log')
plt.title('Spatially resolved diffuse transmittance')
plt.xlabel('r [cm]')
plt.ylabel('$T_d(r)$ $[cm^{-2}]$')
plt.show()

plt.plot(r,Rd_r,'-', c = 'k')
plt.yscale('log')
plt.title('Spatially resolved diffuse reflectance')
plt.xlabel('r [cm]')
plt.ylabel('$R_d(r)$ $[cm^{-2}]$')
plt.show()

#
# Angulary resolved diffuse reflectance and transmittance
#
nn = 30
alpha,Rd_a = angularyResolved(
    res['v'][Rd_index],res['w'][Rd_index],nPh,nn
)
alpha,Td_a = angularyResolved(
    res['v'][Td_index],res['w'][Td_index],nPh,nn
)

plt.plot(alpha,Rd_a,'.',c = 'k')
plt.title('Angulary resolved diffuse reflectance')
plt.xlabel('Exit angle α [rad]')
plt.ylabel('$R_d(α)$ $[sr^{-1}]$')
plt.show()

plt.plot(alpha,Td_a,'.', c = 'k')
plt.title('Angulary resolved diffuse transmittance')
plt.xlabel('Exit angle α [rad]')
plt.ylabel('$T_d(α)$ $[sr^{-1}]$')
plt.show()
