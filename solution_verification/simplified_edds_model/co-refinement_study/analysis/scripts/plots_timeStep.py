import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import sys,os
sys.path.append(os.getcwd())
pd.options.display.float_format = '{:.2e}'.format
plt.rcParams['font.family'] ='serif'
plt.rcParams['font.size']=20

#### Functions 
def data_process(directory,data_input_file,data_input_file_names):
#     data=pd.read_csv(directory+'/'+data_input_file,names = data_input_file_names,skiprows=1, sep='\\s+')
    data=pd.read_csv(directory+'/'+data_input_file,names = data_input_file_names,skiprows=1,comment='#', sep='\\s+',header=None)
    model_fit_statistics=pd.read_pickle(directory+'/output/model_fit_statistics.pkl')
    model_fits=pd.read_pickle(directory+'/output/model_fits.pkl') 
    return data,model_fit_statistics,model_fits

### Convergence Plots Mesh & Timestep
def convergence_plots_dxdt(data,model_fit_statistics,model_fits,dx,dt,label,figDir):
    tmp=model_fits.loc[var]
    plt.figure(figsize=(12,8))
    for irow in range(len(tmp)):
        beta0,beta1,beta2,beta12,gamma1,gamma2,obj,pvalue=tmp.iloc[irow]
        fit=beta0+beta1*dx**gamma1+beta2*dt**gamma2+beta12*dx**gamma1*dt**gamma2
        plt.plot(dx,fit,color='grey',alpha=0.1)
    plt.scatter(data.dx,data[var],marker='o',color='blue')
    plt.scatter(data.dt,data[var],marker='o',color='red')
    tmp=model_fit_statistics.loc[(var,0,'beta0')]
    plt.plot([0],[tmp['median']],'o',color='k')
    plt.plot([0,0],[tmp['lower bound'],tmp['upper bound']],'-x',color='k')
    plt.grid()
    plt.xscale('log')
#     plt.ylim([295,310])
    plt.xlabel('dx')
    plt.ylabel(f'Temperature K')
    plt.title(f'{label} Study \n')
    plt.tight_layout()
    plt.savefig(f'../figures/{figDir}/streeq_convergence_{var[0]}_{label}.png',dpi=300)
    plt.close()

### Convergence Plots 
def convergence_plots(data,model_fit_statistics,model_fits,dxt,dxORdt,label,figDir):
    plt.figure(figsize=(12,8))
    tmp=model_fits.loc[var]
    for irow in range(len(tmp)):
        beta0,beta1,gamma1,obj,pvalue=tmp.iloc[irow]
        fit=beta0+beta1*dxt**gamma1
        plt.plot(dxt,fit,color='grey',alpha=0.1)
    tmp=model_fit_statistics.loc[(var,0,'beta0')]
    plt.plot([0],[tmp['median']],'o',color='k')
    plt.plot([0,0],[tmp['lower bound'],tmp['upper bound']],'-x',color='k')
    plt.grid()
    plt.xscale('log')
#     plt.ylim([295,310])
    plt.xlabel(f'{dxORdt}')
    plt.ylabel(f'Temperature K')
    plt.title(f'{label} Study \n')
    plt.tight_layout()
    plt.savefig(f'../figures/figDir/streeq_convergence_{var[0]}_{label}.png',dpi=300)
    plt.close()
    
# Error Plots
def error_plots(data,model_fit_statistics,dxORdt,label,figDir): 
    plt.figure(figsize=(12,8))
    tmp=model_fit_statistics.loc[(var,0,'beta0')]
    median=tmp['median']
    err = np.array((data[var]-median).abs()/median)
    plt.title(f'{label} \n')
    plt.ylabel('Error')    
    plt.grid(True,which='both',linestyle='--',alpha=0.6)
    plt.tight_layout()
    #plt.xlim([0,0.022])
 #   plt.title(f'{title}: {var} (scaled)')
    plt.savefig(f'../figures/{figDir}/streeq_error_{var[0]}_{label}.png',dpi=300)
    plt.close()
    return err 

# Scatter dx vs dy - color = error  
#cmap='coolwarm'
def  scatter_err_dxdy(data,model_fit_statistics,dataM,errM,dataT,errT,label,numCurves,figDir):
    plt.figure(figsize=(12,8))
    tmp=model_fit_statistics.loc[(var,0,'beta0')]
    median=tmp['median']
    err = np.array((data[var[0]]-median).abs()/median)
    plt.title('Error by $\Delta x$ vs. $\Delta t$ \n')
    plt.xscale('log')
    plt.yscale('log')  
    if numCurves == 3: 
        dt_const = 0.005*np.ones_like(dataM.dx)
        plt.axhline(y=0.005, color='gray', linestyle='--', linewidth=2,label='Const Time',zorder=1)
        im= plt.scatter (dataM.dx,dt_const, norm=colors.LogNorm(vmin=err.min(), vmax=err.max()),c=errM,cmap='viridis',s=200,zorder=5)
        dx_const = 0.22840836*np.ones_like(dataT.dt)
        plt.axvline(x=0.22840836, color='gray', linestyle=':', linewidth=2,label='Const Mesh',zorder=1)
        im= plt.scatter (dx_const,dataT.dt, norm=colors.LogNorm(vmin=err.min(), vmax=err.max()),c=errT,cmap='viridis',s=200,zorder=5)
        
    plt.loglog(data.dx,data.dt, label='Mesh & Time',linestyle='-',color='black',zorder=1)
    im= plt.scatter (data.dx,data.dt, norm=colors.LogNorm(vmin=1e-4, vmax=5e-5),c=err,cmap='viridis',s=200,zorder=5)
    cbar = plt.colorbar(im)
    if numCurves == 3:
        plt.xticks(ticks=[0.22840836],labels=[f'{val:.1e}' for val in [0.22840836]],rotation=45)
        plt.yticks(ticks=[1e-4,1e-3,0.005,1e-2],labels=['$10^{-4}$','$10^{-4}$','5.0e-03','$10^{-2}$'],rotation=0)  
    plt.ylim([1e-4,1e-2])
    plt.xlabel('$\Delta x$ (m)')
    plt.ylabel('$\Delta t$ (sec)')  
    plt.legend()
    cbar.set_label('Error', labelpad=10) #labelpad adjusts the padding between the label and the colorbar
    plt.grid(True,which='both',linestyle='--',alpha=0.6)
 #   plt.title(f'{title}: {var} (scaled)')
    plt.tight_layout()
    if numCurves == 3:
        plt.savefig(f'../figures/{figDir}/streeq_scatter_error_{var[0]}_{label}_all.png',dpi=300)
    if numCurves == 1: 
        plt.savefig(f'../figures/{figDir}/streeq_scatter_error_{var[0]}_{label}.png',dpi=300)
    plt.close()
    return err

# Order of Convergence Plots
def order_p(err,h,dxORdt,label,figDir): 
    p_observed = (np.log(err[-1])-np.log(err[0]))/(np.log(h[-1])-np.log(h[0]))
#     print(f'p_observed: {p_observed}')
    h_anchor = h[0]
    u_err_anchor = err[0]
    offset = 2
    h_ref = np.logspace(np.log10(h[0]),np.log10(h[-1]),100)
    ref_slope1 = u_err_anchor*(h_ref/h_anchor)**1 * offset*0.75
    ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
    ref_slopeP = u_err_anchor*(h_ref/h_anchor)**p_observed
    plt.figure(figsize=(12,8))
    plt.loglog(h,err,'-ok',label=f'Observed (p={p_observed:.2f})')
#     plt.loglog(h_ref,ref_slopeP,'--',color='gray',label=f'Observed (p={p_observed[0]:.2f})')
    plt.loglog(h_ref,ref_slope1,'--',label='p=1')
#     plt.loglog(h_ref,ref_slope2,'--',label='p=2')
    plt.ylabel('Relative Error')
    if dxORdt=='$\Delta t$':
        plt.xlabel(f'{dxORdt} (sec)')
    ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
    plt.loglog(h_ref,ref_slope2,'--',label='p=2')
    plt.legend(loc='lower right')
    plt.xticks(ticks=h,labels=[f'{val:.1e}' for val in h],rotation=45)
    plt.grid(True,which='both',linestyle='--',alpha=0.6)
    plt.title(f'{var} \n ')
    plt.tight_layout()
    plt.savefig(f'../figures/{figDir}/relative_err_observedP_{label}.png',dpi=300,bbox_inches='tight')    

def plot_TavgTimestep(timestep,Tavg,varLabel,figDir):
    plt.figure(figsize=(12,8))
    plt.plot(timestep,(Tavg-300),'-o',label=f'{varLabel})')
    plt.ylabel('Temperature Rise')
    plt.xlabel('Time Step (s)')
    plt.title(f'{varLabel} \n ')
    plt.tight_layout()
    plt.savefig(f'../figures/{figDir}/timestep_vs_Temp_{varLabel}.png',dpi=300,bbox_inches='tight')

####################################
###### Average Temperature 
##########################################   
# QOI
#var_all=['Tavg_z0.001_t1','Tavg_z0.001_t6', 'Tavg_z0.001_t12', 'Tavg_z0.006_t1', 'Tavg_z0.006_t6', 'Tavg_z0.006_t12', 'Tavg_z0.03_t1' ,'Tavg_z0.03_t6', 'Tavg_z0.03_t12', 'Tavg_z0.045_t1', 'Tavg_z0.045_t6', 'Tavg_z0.045_t12', 'Tavg_z0.0517_t1', 'Tavg_z0.0517_t6', 'Tavg_z0.0517_t12']
var_all = ['Tavg_z0.001_t1', 'Tavg_z0.001_t5', 'Tavg_z0.001_t6', 'Tavg_z0.001_t12', 'Tavg_z0.006_t1', 'Tavg_z0.006_t5', 'Tavg_z0.006_t6', 'Tavg_z0.006_t12', 'Tavg_z0.03_t1', 'Tavg_z0.03_t5', 'Tavg_z0.03_t6', 'Tavg_z0.03_t12', 'Tavg_z0.045_t1', 'Tavg_z0.045_t5', 'Tavg_z0.045_t6', 'Tavg_z0.045_t12', 'Tavg_z0.0517_t1', 'Tavg_z0.0517_t5', 'Tavg_z0.0517_t6', 'Tavg_z0.0517_t12']

######## Time 1 6 12 & m3 & tol 1e-8 
directoryT = '../streq_studies/verif_time'
data_input_fileT = 'data_t1-5-6-12_Tavg.dat'  
#data_input_file_namesT = ['dt','Tavg_z0.001_t1','Tavg_z0.001_t6', 'Tavg_z0.001_t12', 'Tavg_z0.006_t1', 'Tavg_z0.006_t6', 'Tavg_z0.006_t12', 'Tavg_z0.03_t1' ,'Tavg_z0.03_t6', 'Tavg_z0.03_t12', 'Tavg_z0.045_t1', 'Tavg_z0.045_t6', 'Tavg_z0.045_t12', 'Tavg_z0.0517_t1', 'Tavg_z0.0517_t6', 'Tavg_z0.0517_t12']
data_input_file_namesT = ['dt','Tavg_z0.001_t1', 'Tavg_z0.001_t5', 'Tavg_z0.001_t6', 'Tavg_z0.001_t12', 'Tavg_z0.006_t1', 'Tavg_z0.006_t5', 'Tavg_z0.006_t6', 'Tavg_z0.006_t12', 'Tavg_z0.03_t1', 'Tavg_z0.03_t5', 'Tavg_z0.03_t6', 'Tavg_z0.03_t12', 'Tavg_z0.045_t1', 'Tavg_z0.045_t5', 'Tavg_z0.045_t6', 'Tavg_z0.045_t12', 'Tavg_z0.0517_t1', 'Tavg_z0.0517_t5', 'Tavg_z0.0517_t6', 'Tavg_z0.0517_t12']
dataT, model_fit_statisticsT, model_fitsT = data_process(directoryT,data_input_fileT,data_input_file_namesT)
dt=np.linspace(0,0.0065,101)
####convergence_plots(dataT,model_fit_statisticsT,model_fitsT,dt,'dt',label='time')
figDir = 'study_timestep'
dxORdt='$\Delta t$'
for var in var_all:
    err_time = error_plots(dataT,model_fit_statisticsT,'dt',var,figDir)
    err_time, h_time = np.array(err_time), np.array(dataT['dt'])
    order_p(err_time,h_time,dxORdt,var,figDir)
    plot_TavgTimestep(dataT['dt'],dataT[var],var,figDir)
    #err_time,h_time = [item for sublist in err_time for item in sublist], h_time.tolist()
    err_time,h_time = err_time.tolist(), h_time.tolist()
    resultsTime = pd.DataFrame({'Representative Time Step':h_time, 'Error':err_time})
    resultsTime.to_csv(f'../data/results_Time_Err_{var}.dat',index=False)

