import sys
import numpy as np
import pathlib
import h5py
import matplotlib.pyplot as plt
import scipy.optimize
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
# import newHmann as hmann
import csv
import os
from mpi4py import MPI

basedir = os.path.dirname(os.path.realpath(__file__))


def chi_squared(y_data, y_fit, y_unc=None):
    '''Given two input arrays of equal length, calculate and
    return the chi_squared value.  Use uncertainties if they
    are given.
    
    INPUTS:
    Y_DATA is an array object representing the actual data points
    Y_FIT is an array object representing the fit values at the same x-locations as the data points
    
    OUTPUTS:
    CHI_S is the chi squared statistic, weighted by uncertainties if they are provided.'''
    
    if y_unc is not None:
        chi_s = np.sum( (y_data-y_fit)**2/y_unc**2 )
    else:
        chi_s = np.sum( (y_data-y_fit)**2)
        
    return chi_s

def hartmann_z(z, Ha, u):
    return (u*(1- (np.cosh(Ha*z)/np.cosh(Ha))))

def hartmann_b_z(z, Ha, u):
    #print("Ha = {} and u = {}", Ha, u)
    return (-(z/Ha) + (u*(np.sinh(Ha*z)/np.cosh(Ha))))
    
def hartmann_y(y, Ha, u):
	return (u*(1- (np.cosh(Ha*y)/np.cosh(Ha))))	

def poiseuille_flow_fit(y, u):
	return (u*(1- y**2))	
	
# vxxx = hartmann(z, 1, 1)
# plt.semilogy(z, vxxx, 'r.')
# plt.xlabel("z")
# plt.ylabel(r"$<v_x>$")
# plt.savefig('vx_zprof.png')

def plot_fit_z(func, x_array, y_array, i):
    u = (1/i**2)
    popt, pcov = scipy.optimize.curve_fit(func, x_array, y_array, p0 = [i, u])
    print(popt[0])
    print(popt[1])
    plt.semilogy(x_array, y_array, 'g.', label = "simulation data")
    #plt.semilogy(x_array, func(x_array, popt[0] , popt[1]), 'r-')
    plt.semilogy(x_array, func(x_array, i , u), 'r-', label = "analytical solution")
    plt.title("Hartmann profile for conducting walls")
    plt.legend(loc='lower center')
    plt.xlabel("z")
    plt.ylabel(r"$u_x$")
    chi_square = (chi_squared(y_array, func(x_array, i, u)))
    R_squared = (r2_score(y_array, func(x_array, i, u)))
    Root_mean_squared_error = (np.sqrt(mean_squared_error(y_array, func(x_array, i, u))))
    plt.savefig('vx_curvefit_z'+str(i)+'.png')
    plt.clf()
    return popt[0], popt[1], chi_square, R_squared, Root_mean_squared_error

def plot_fit_b_z(func, x_array, y_array, i):
    print("xarray", x_array)
    print("yarray", y_array*i)
    u = (1/i**2)
    print(u)
    print(i)
    print("anylitical soln ",func(x_array, i, u))
    popt, pcov = scipy.optimize.curve_fit(func, x_array, y_array*i, p0 = [i, u])
    print(popt[0])
    print(popt[1])
    plt.plot(x_array, y_array*i, 'g.', label = "simulation data")
    #plt.plot(x_array, func(x_array, popt[0] , popt[1]), 'r-')
    plt.plot(x_array, func(x_array, i , u), 'r-', label = "analytical solution")
    plt.title("Induced magnetic field for Hartmann flow")
    plt.legend(loc='lower center')
    plt.xlabel("z")
    plt.ylabel(r"$b*Ha$")
    chi_square = (chi_squared(y_array, func(x_array, i, u)))
    R_squared = (r2_score(y_array, func(x_array, i, u)))
    Root_mean_squared_error = (np.sqrt(mean_squared_error(y_array, func(x_array, i, u))))
    plt.savefig('vx_curvefit_z'+str(i)+'b.png')
    plt.clf()
    return popt[0], popt[1], chi_square, R_squared, Root_mean_squared_error
		
    popt, pcov = scipy.optimize.curve_fit(func, x_array, y_array)
    print(popt[0])
    plt.semilogy(x_array, y_array, 'g.')
    plt.semilogy(x_array, func(x_array, *popt), 'r-')
    plt.xlabel("y")
    plt.ylabel(r"$<v_x>$")    
    plt.savefig('vx_curvefit_y_pois.png')

def hartmann_erors():
    csvData = [['i', 'ha', 'u', 'chi squared', 'R squared', 'Mean squared error']]
    for i in range (1,2):
        #hmann.hartmann_flaw (i*2)
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == 0:
            dfile = basedir+'/scratch/integrals/integrals.h5'
            data = h5py.File(str(dfile), "r")

            y = data['scales/y/1'][:]
            z = data['scales/z/1'][:]
            x= data['tasks/<vx>_x'][:]
            bz = data['tasks/<Bx>_x'][-1,0,-1,:]
            vxz = data['tasks/<vx>_x'][-1,0,-1,:]
            
            ha, u, chi_square, R_squared, Root_mean_squared_error = plot_fit_z(hartmann_z, z, vxz, i)
            
            print(ha)
            print(chi_square)
            print(R_squared)
            print(Root_mean_squared_error)
            
            plot_fit_b_z(hartmann_b_z, z, bz, i)
            #popt, pcov = scipy.optimize.curve_fit(hartmann_z, y, vxy)
            csvData1 = [i, ha, u, chi_square, R_squared, Root_mean_squared_error]
            csvData.append(csvData1)
            with open('errorData.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerows(csvData)
            csvFile.close()
        MPI.COMM_WORLD.Barrier()
hartmann_erors()
