import sys
import pathlib
import h5py
import os
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import axes3d
import numpy as np

basedir = os.path.dirname(os.path.realpath(__file__))
dfile = basedir + '/scratch/integrals/integrals.h5'

data = h5py.File(str(dfile), "r")

# print(data['scales'])

x = data['scales/x/1'][:]
y = data['scales/y/1'][:]
z = data['scales/z/1'][:]
print("z", z.shape, z)
print('x', x.shape, x)


vx = data['tasks/<vx>_x'][-1,:,:,:]
vy = data['tasks/<vy>_x'][-1,:,:,:]
vz = data['tasks/<vz>_x'][-1,:,:,:]
# print("vx", vx.shape, vx)


fig = plt.figure()
ax = fig.gca(projection='3d')

ax.quiver(x, y, z, vx, vy, vz, length=0.1)

plt.show()