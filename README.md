# ssxluo
This repository contains python code that are used to simulate 3 magnetohydrodynamic (MHD) experiments. The python code utilizes an open-source environment called [dedalus](https://dedalus-project.readthedocs.io/en/latest/index.html). All python code is run on the [PSC-Bridges](https://www.psc.edu/bridges) supercomputing cluster.
 ![example merging image](images/Field_Temperature_Images.jpg)

The directory "Hartmann" contains python code used to simulate the MHD Hartmann flow problem. It is a problem with well known analytical soluations. A typical simulation costs around 5 CPU-hours.

<insert Hartmann flow image>
![Hartmann Rendered](images/Hartmann_v_B_fields.jpg)

The directory ssxluo contains python code that were used to simulate 
(1) the relaxation of a spheromak into a B-force-free equilibrium named the Taylor state (see original paper)
<insert Taylor State image>
![example merging image](images/spheromak1.jpg)
  
(2) the merging of two Taylor state plasmas due to pressure gradient (magnetic reconnection takes place in this experiment). 
![example merging image](images/Field_Temperature_Images1.jpg)
  
A taypical simulation run costs around 5,000-10,000 CPU-hours with a resolution of 28x24x360. The x and y axis of the solution domain can be distributively solved.
