import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

# import functions and parameters
import params
import all_functions

# Set the font family and size to use for Matplotlib figures.
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 20

# Calculate Thermal Entrance Region & Hydrodynamic Entrance Region
x_entryThermo, x_entryHydro = all_functions.entry_Region(params.u,params.d,params.Pr,params.viscosity50,params.viscosity20)
print(f'x_entryThermo = {x_entryThermo:.3f} mm, x_entryHydro = {x_entryHydro:.3f} mm')

# Collect Variables
# z,u,d,viscosity,Pr,thmCond,specific_heat,T_inlet,density,T_wall= params.z,params.u,params.d,params.viscosity50,params.Pr,params.thmCond,params.specific_heat,params.T_inlet,params.density,params.T_wall

# Import data from data processing and combine
dataT_012 = pd.read_csv('../data/data_m012_T50.csv')  # M0,M1,M2 
dataTbulk_012 = pd.read_csv('../data/data_m012_Tbulk_T50.csv')  # M0,M1,M2 
dataT_22 = pd.read_csv('../data/data_m2_2_T50.csv') # M2.2
dataTbulk_22 = pd.read_csv('../data/data_Tbulk_m2_2_T50.csv')   # M2.2 
dataT = pd.concat([dataT_012,dataT_22],ignore_index=True)
dataTbulk = pd.concat([dataTbulk_012,dataTbulk_22],ignore_index=True)

# Collect Mesh Specific Temperature Data for scatter plots
dataM0_Sim = dataT[dataT['Mesh']==0]
dataM1_Sim = dataT[dataT['Mesh']==1]
dataM2_Sim = dataT[dataT['Mesh']==2]
dataM22_Sim = dataT[dataT['Mesh']==2.2]
dataMall_Sim = [dataM0_Sim,dataM1_Sim,dataM2_Sim,dataM22_Sim]

# Collect Mesh Specific Bulk Temperature Data for extrapolation studies
dataTbulkM0_Sim = np.array(dataTbulk[dataTbulk['Mesh']==0]['Tbulk_sim']-273.15)
dataTbulkM1_Sim = np.array(dataTbulk[dataTbulk['Mesh']==1]['Tbulk_sim']-273.15)
dataTbulkM2_Sim = np.array(dataTbulk[dataTbulk['Mesh']==2]['Tbulk_sim']-273.15)
dataTbulkM22_Sim = np.array(dataTbulk[dataTbulk['Mesh']==2.2]['Tbulk_sim']-273.15)

# Data Prep for StREEQ processing (Mesh Resolution Study w/ Extrapolation)
Tlabels = ['Tbulk_z'+str(int(params.z[0]*1000)),'Tbulk_z'+str(int(params.z[1]*1000)),'Tbulk_z'+str(int(params.z[2]*1000)),
           'Tbulk_z'+str(int(params.z[3]*1000)),'Tbulk_z'+str(int(params.z[4]*1000)),'Tbulk_z'+str(int(params.z[5]*1000)),
           'Tbulk_z'+str(int(params.z[6]*1000))]
data_streeq = pd.DataFrame(np.array([dataTbulkM0_Sim,dataTbulkM1_Sim,dataTbulkM2_Sim,dataTbulkM22_Sim]),columns=Tlabels)
data_streeq.insert(0,'#representativeLength',params.len_rep)
data_streeq.to_csv('../data/dataTbulk_streeq.dat',index=False,sep=' ') 

# Temperature Scatter Plots for z positions at all mesh resolutions
k, mesh = 0,['M0','M1','M2','M2.2']
for zs in np.arange(1,8,1):#params.z:
    m = 0
    while m < len(mesh):
        data = dataMall_Sim[m]
        data_z = data[data['z']==zs]
        plt.figure(figsize=(12,5))
        plt.subplot(1,2,1)
        plt.scatter(data_z['x']*1e3,data_z['y']*1e3,facecolors='none', edgecolors='black')
        sc = plt.scatter(data_z['x']*1e3,data_z['y']*1e3,c=data_z['T']-273.15, cmap='coolwarm', s=50) # data_T[-1][:])
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.grid(True,which='both',linestyle='-',color='gray')        
        plt.subplot(1,2,2)
        sc = plt.scatter(data_z['r']*1000,data_z['T']-273.15, c =data_z['T']-273.15,cmap='coolwarm',s=50 )
        maxT = np.max(data_z['T'])-273.15
        cbar = plt.colorbar(sc)
        cbar.set_label('\n Temperature [C]')
        plt.xlabel('Radius [mm]')
        plt.xticks([0,0.5,1,1.5,2,2.5])
        plt.grid(True,which='both',linestyle='-',color='gray')
        plt.suptitle(f'Cross-Sectional Temperature Profile (z = {params.z[zs-1]*1000:.1f}mm), Mesh {mesh[m]}\n')
        plt.savefig(f'../figures/T_scatter_radial_z{round(params.z[zs-1]*1000)}mm_{mesh[m]}.png', dpi=300, bbox_inches='tight')
        m +=1
    k+=1
