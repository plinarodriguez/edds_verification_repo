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

## required for analytic solution
re_D = all_functions.reynoldsNum(params.u,params.d,params.nu20)
f = 64/re_D
dP = f*params.l_pipe*1*params.u**2/(2*params.R*2)
pressureGrad = dP/0.042  #params.l_pipe

# Import simulation data from data processing and combine
dataSim = pd.read_csv('../data/data_mAll.csv')  

# Collect Mesh Specific Temperature Data
dataM0_Sim = dataSim[dataSim['Mesh']==0]
dataM1_Sim = dataSim[dataSim['Mesh']==1]
dataM2_Sim = dataSim[dataSim['Mesh']==2]
dataM22_Sim = dataSim[dataSim['Mesh']==2.2]
dataMall_Sim = [dataM0_Sim,dataM1_Sim,dataM2_Sim,dataM22_Sim]

# Velocity Scatter Plots for z position at all mesh resolutions 
k, mesh = 0,['M0','M1','M2','M2.2']
for zs in np.arange(1,8,1):#params.z:
    m = 0
    while m < len(mesh):
        data = dataMall_Sim[m]
        data_z = data[data['z']==zs]
        plt.figure(figsize=(12,5))
        plt.subplot(1,2,1)
        plt.scatter(data_z['x']*1e3,data_z['y']*1e3,facecolors='none', edgecolors='black')
        sc = plt.scatter(data_z['x']*1e3,data_z['y']*1e3,c=data_z['U'], cmap='viridis', s=50) # data_T[-1][:])
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.grid(True,which='both',linestyle='-',color='gray')        
        plt.subplot(1,2,2)
        sc = plt.scatter(data_z['r']*1000,data_z['U'], c =data_z['U'],cmap='viridis',s=50 )
        plt.scatter(data_z['r']*1000,all_functions.analytic_hagenPoiseuille(data_z['r'],params.R,pressureGrad,params.nu20), color='black', s=10, label='analytic')
        maxT = np.max(data_z['U'])
        cbar = plt.colorbar(sc)
        cbar.set_label('\n Velocity [m/s]')
        plt.xlabel('Radius [mm]')
        plt.xticks([0,0.5,1,1.5,2,2.5])
        plt.grid(True,which='both',linestyle='-',color='gray')
        plt.suptitle(f'Cross-Sectional Velocity Profile (z = {params.z[zs-1]*1000:.1f}mm), Mesh {mesh[m]} \n')
        plt.savefig(f'../figures/U_scatter_radial_z{round(params.z[zs-1]*1000)}mm_{mesh[m]}.png', dpi=300, bbox_inches='tight')
        m +=1
    k+=1

# Error Estimation
dataM0= dataM0_Sim[dataM0_Sim['z']==4.0]
dataM1= dataM1_Sim[dataM1_Sim['z']==4.0]
dataM2= dataM2_Sim[dataM2_Sim['z']==4.0]
dataM22= dataM22_Sim[dataM22_Sim['z']==4.0]
l2_errorsM0,radiusM0 = all_functions.l2_norm_calc(dataM0['U'],dataM0['r'],dataM0['Vol'],params.R, pressureGrad,params.nu20)
l2_errorsM1,radiusM1 = all_functions.l2_norm_calc(dataM1['U'],dataM1['r'],dataM1['Vol'],params.R, pressureGrad,params.nu20)
l2_errorsM2,radiusM2 = all_functions.l2_norm_calc(dataM2['U'],dataM2['r'],dataM2['Vol'],params.R, pressureGrad,params.nu20)
l2_errorsM22,radiusM22 = all_functions.l2_norm_calc(dataM22['U'],dataM22['r'],dataM22['Vol'],params.R, pressureGrad,params.nu20)

# Calculate Order of Convergence
h = [params.len_rep[0],params.len_rep[1],params.len_rep[2],params.len_rep[3]]
errU = [l2_errorsM0,l2_errorsM1,l2_errorsM2,l2_errorsM22]
p_observed = (np.log(errU[-1])-np.log(errU[0]))/(np.log(h[-1])-np.log(h[0]))
h_anchor = h[1]
u_err_anchor = errU[1]
offset = 2
h_ref = np.logspace(np.log10(h[0]),np.log10(h[3]),100)
ref_slope1 = u_err_anchor*(h_ref/h_anchor)**1 * (offset*2)
ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
plt.figure(figsize=(12,8))
plt.loglog(h,errU,'o-k',label=f'Observed (p ={abs(p_observed):.2f})', markersize=8)
plt.loglog(h_ref,ref_slope1,'--',label='p = 1')
plt.loglog(h_ref,ref_slope2,'--',label='p = 2')
plt.title('Velocity \n')
plt.xlabel('Representative Length [m]')
plt.ylabel('L2 Norm')
plt.ylim(1e-5,1e-0)
plt.xticks(ticks=h,labels=['4.4e-4   ','2.2e-4   ','1.1e-4   ','8.8e-5   '],rotation=30)
plt.legend()
plt.grid(True,which='both',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.savefig(f'../figures/U_L2Norm_Observed_p.png', dpi=300, bbox_inches='tight')
