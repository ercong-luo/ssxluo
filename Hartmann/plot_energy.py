import sys
import pathlib
import h5py
import matplotlib.pyplot as plt

basedir = pathlib.Path(sys.argv[-1])
dfile = basedir / 'timeseries/timeseries_s1.h5'

data = h5py.File(str(dfile), "r")

t = data['scales/sim_time'][:]
KE = data['tasks/Ekin'][:,0,0]
ME = data['tasks/Emag'][:,0,0]
plt.subplot(121)
plt.semilogy(t, KE)
plt.xlabel("time")
plt.ylabel("Kinetic energy")
plt.subplot(122)
plt.semilogy(t, ME, 'x-')
plt.xlabel("time")
plt.ylabel("Magnetic energy")

# plt.plot(t, sigma)
# plt.xlabel("time")
# plt.ylabel(r"$\Sigma$")

plt.savefig('energy.png')

