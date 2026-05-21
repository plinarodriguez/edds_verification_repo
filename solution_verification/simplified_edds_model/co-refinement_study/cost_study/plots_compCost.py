import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import sys,os
sys.path.append(os.getcwd())
pd.options.display.float_format = '{:.2e}'.format
plt.rcParams['font.family'] ='serif'
plt.rcParams['font.size']=20

dataM = pd.read_csv('computeTime/statsMesh.dat',sep='\\s+')
dataT = pd.read_csv('computeTime/statsTime.dat',sep='\\s+')
dataMT = pd.read_csv('computeTime/statsMeshTime.dat',sep='\\s+')

def comCostTotal(data):
    totalSec =  ((data['CT'] * data['Processors'])/60)/60
    return totalSec

dx = [3.72e-01,2.87e-01,2.28e-01,1.84e-01,1.44e-01,1.14e-01,9.09e-02]
dt = [4.00e-03,3.50e-03,2.50e-03,2.00e-03,1.60e-03,1.40e-03,1.00e-03]
dx_Mesh = [0.37151132884054006,0.2871904662373521,0.22840836479998242,0.1841001150019505,0.14418897770893674,0.11370645671722239,0.0909313534093646]
dt_TimeStep = [0.0060,0.0042,0.0030,0.0021,0.0015,0.0011,0.0007,0.0005,0.0004,0.0003]

plt.figure(figsize=(12,8))
err = comCostTotal(dataMT)
errT = comCostTotal(dataT)
errM = comCostTotal(dataM)
plt.title('Computational Cost by $\Delta x$ vs. $\Delta t$')
plt.xscale('log')
plt.yscale('log')  
dt_const = 0.005*np.ones_like(dx_Mesh)
plt.axhline(y=0.005, color='gray', linestyle='--', linewidth=2,label='Const Time',zorder=1)
im= plt.scatter (dx_Mesh,dt_const,norm=colors.LogNorm(vmin=err.min(),vmax=err.max()),c=errM,cmap='viridis',s=200,zorder=5,clim=[errM.min(),errM.max()])
dx_const = 0.22840836*np.ones_like(dt_TimeStep)
plt.axvline(x=0.22840836, color='gray', linestyle=':', linewidth=2,label='Const Mesh',zorder=1)
im= plt.scatter (dx_const,dt_TimeStep,norm=colors.LogNorm(vmin=err.min(),vmax=err.max()),c=errT,cmap='viridis',s=200,zorder=5,clim=[errM.min(),errM.max()])
plt.loglog(dx,dt, label='Mesh & Time',linestyle='-',color='black',zorder=1)
im= plt.scatter (dx,dt,norm=colors.LogNorm(vmin=err.min(),vmax=err.max()),c=err,cmap='viridis',s=200,zorder=5, clim=[errM.min(),errM.max()])
cbar = plt.colorbar(im)
plt.xticks(ticks=[0.22840836],labels=[f'{val:.1e}' for val in [0.22840836]],rotation=45)
plt.yticks(ticks=[1e-4,1e-3,0.005,1e-2],labels=['$10^{-4}$','$10^{-3}$','5.0e-03','$10^{-2}$'],rotation=0)  
plt.ylim([1e-4,1e-2])
plt.xlabel('$\Delta x$ (m)')
plt.ylabel('$\Delta t$ (sec)')  
plt.legend(reverse=True)
cbar.set_label('Computational Cost (hrs)', labelpad=10) #labelpad adjusts the padding between the label and the colorbar
plt.grid(True,which='both',linestyle='--',alpha=0.6)
#   plt.title(f'{title}: {var} (scaled)')
plt.tight_layout()
plt.savefig(f'../figures/comCost/scatter_dxdt_comCost_all.png',dpi=300)

resultsMesh = pd.DataFrame({'dx':dx_Mesh, 'CompCost':errM})
resultsMesh.to_csv('data/results_compCost_Mesh.dat',index=False)

resultsTime = pd.DataFrame({'dt':dt_TimeStep, 'CompCost':errT})
resultsTime.to_csv('data/results_compCost_Time.dat',index=False)

resultsMeshTime = pd.DataFrame({'dt':dt,'dx':dx, 'CompCost':err})
resultsMeshTime.to_csv('data/results_compCost_MeshTime.dat',index=False)


