import numpy as np

####################
# Global Parameters
####################
u = 0.5 # average velocity m/s
d = 0.00454 # pipe diameter in m 
R = d/2
l_pipe = 0.042 # m length of pipe measurement for Hagen Poiseuille flow study
length =  0.0486411 # m distance along fluid flow direction, fully developed flow starts here 0.0394m
l_fdf = 0.045  #fully developed flow regime in m 
viscosity50 = 1.7947e-5 #1.69e-5 # kinematic viscosity of air m^2/s @ 50C
viscosity20 = 1.5111e-5 #1.48e-5 # kinematic viscosity of air m^2/s @ 20C
nu20 = viscosity20
nu50 = viscosity50
density =  1.09 # @ 50C of temperature at heated wall 100 C [kg/m^3] = 0.9467
rho = density
Pr = 0.709     # prandtl number for air at room temp
thmCond = 0.0270# thermal conductivity of fluid at room temp 0.0270 W/mK
specific_heat = 1007 # J/kgK
T_wall = 50 # C
T_inlet = 20 #C, bulk temp
x = length - l_fdf # this is the length starting at the casing where heating is applied
z1,z2,z3,z4,z5,z6,z7 = 0.015,0.030,0.045,0.042,0.01,0.005,0.014
z = np.array([z1,z2,z3,z4,z5,z6,z7])
####################
### Mesh Stats #####
####################
r_caseOut = 0.00257 # m
volPipe   = np.pi*R**2*l_fdf*2 # 1456.948 mm^3
volCase   = np.pi*(r_caseOut - R)**2 * l_fdf # 12.723 mm^3
volTotal  =  (volPipe + volCase)
mesh_elem = [17910,132460,1083821,2142932]
mesh_node = [20930,144186,1131119,2217453]
len_rep   = (volTotal/ np.array(mesh_elem))**(1/3)
