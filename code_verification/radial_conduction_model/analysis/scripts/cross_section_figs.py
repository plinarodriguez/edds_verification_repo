import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

# function to compute analytic solution by radius
def analyticbyradius(r):
        # r = (np.linspace(0.00227,0.00257,100)) # m
        r_w = 0.00257 # wall radius ( C, outer wall temperature)
        r_i = 0.00227 # radius of interface
        S = 35e7  # W/m^3, heat source 
        k =  91   #  90 W/mK should be thermal conductivity; 0.3e-4 m²/s for nickel(0.2 to 0.3 x 10⁻⁴ m²/s),thermal diffusivity
        T_w = 293.15  # Wall Temperature 
        ### Analytic Solution - Matt
        # temp_analytic = T_w - (r**2-r_w**2)*S/(4*k) - (S*r_w**2/2*k)*np.log(r/r_w)
        ### Analytic Solution - Derrivation
        T_analytic = T_w - (S/(4*k))*(r**2-r_w**2)+(S/(2*k))*(r_i**2)*np.log(r/r_w)
        return T_analytic


# Import data from data processing and combine
data = pd.read_csv('../data/dataT_mAll.csv')
# dataT = pd.read_csv('../data/data_case_t0.3_test.dat', delimiter=' ')

# Collect Mesh Specific Temperature Data
dataM0_Sim = data[data['Mesh']==0]
dataM1_Sim = data[data['Mesh']==1]
dataM2_Sim = data[data['Mesh']==2]

# dataM0_SimT = dataT[dataT['Mesh']==0]
# dataM1_SimT = dataT[dataT['Mesh']==1]
# dataM2_SimT = dataT[dataT['Mesh']==2]
dataMall_Sim = [dataM0_Sim,dataM1_Sim,dataM2_Sim]
# dataMall_SimT = [dataM0_SimT,dataM1_SimT,dataM2_SimT]

# Temperature Scatter Plots for z cros section
mesh = ['M0','M1','M2']
m = 0
while m < len(mesh):
    data = dataMall_Sim[m]
    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.scatter(data['x']*1e3,data['y']*1e3,facecolors='none', edgecolors='black')
    sc = plt.scatter(data['x']*1e3,data['y']*1e3,c=data['T']-273.15, cmap='coolwarm', s=50) # data_T[-1][:])
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.xlim(0,3)
    plt.ylim(0,3)
    plt.grid(True,which='both',linestyle='-',color='gray')

    plt.subplot(1,2,2)
    sc = plt.scatter(data['r']*1000,data['T']-273.15, c=data['T'],cmap='coolwarm',s=50,label='model')
    maxT = np.max(data['T'])-273.15
    cbar = plt.colorbar(sc)
    cbar.set_label('\n Temperature [C]')
    plt.scatter(data['r']*1000, analyticbyradius(data['r'])-273.15, color='black',label='analytic')
    plt.xlabel('Radius [mm]')
    plt.xlim(2.2, 2.60)
    plt.legend()
    plt.grid(True,which='both',linestyle='-',color='gray')
    plt.suptitle(f'Cross-Sectional Temperature Profile (z = {0.0675*1000:.1f}mm), Mesh {m}')
    plt.savefig(f'../figures/T_scatter_radial_z{0.0675*1000}mm_M{m}.png', dpi=300, bbox_inches='tight')
    plt.close
    m +=1    

