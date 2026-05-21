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
    data=pd.read_csv(directory+'/'+data_input_file,names = data_input_file_names,skiprows=1,comment='#', sep='\\s+',header=None)
    model_fit_statistics=pd.read_pickle(directory+'/output/model_fit_statistics.pkl')
    model_fits=pd.read_pickle(directory+'/output/model_fits.pkl') 
    return data,model_fit_statistics,model_fits

### Convergence Plots Mesh & Timestep
def convergence_plots_dxdt(data,model_fit_statistics,model_fits,dx,dt,label):
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
    plt.title(f'{label} Study')
    plt.tight_layout()
    plt.savefig(f'../figures/streeq_convergence_{var[0]}_{label}.png',dpi=300)
    plt.close()

### Convergence Plots 
def convergence_plots(data,model_fit_statistics,model_fits,dxt,dxORdt,label):
    plt.figure(figsize=(12,8))
    tmp=model_fits.loc[var]
    for irow in range(len(tmp)):
        beta0,beta1,gamma1,obj,pvalue=tmp.iloc[irow]
        fit=beta0+beta1*dxt**gamma1
        plt.plot(dxt,fit,color='grey',alpha=0.1)
    if dxORdt == 'dx':
        plt.scatter(data.dx,data[var],marker='o',color='blue')
    if dxORdt == 'dt':
        plt.scatter(data.dt,data[var],marker='o',color='blue')
    if dxORdt == 'ds':
        plt.scatter(data.ds,data[var],marker='o',color='blue')
    tmp=model_fit_statistics.loc[(var,0,'beta0')]
    plt.plot([0],[tmp['median']],'o',color='k')
    plt.plot([0,0],[tmp['lower bound'],tmp['upper bound']],'-x',color='k')
    plt.grid()
    plt.xscale('log')
#     plt.ylim([295,310])
    plt.xlabel(f'{dxORdt}')
    plt.ylabel(f'Temperature K')
    plt.title(f'{label} Study')
    plt.tight_layout()
    plt.savefig(f'../figures/streeq_convergence_{var[0]}_{label}.png',dpi=300)
    plt.close()
    
# Error Plots
def error_plots(data,model_fit_statistics,dxORdt,label): 
    plt.figure(figsize=(12,8))
    tmp=model_fit_statistics.loc[(var[0],0,'beta0')]
    median=tmp['median']
    err = np.array((data[var]-median).abs()/median)
    if dxORdt == 'dx':
        plt.loglog(data.dx, err,'o',lw=3)
        plt.xlabel('dx')
    if dxORdt == 'dt':
        plt.loglog(data.dt, err,'o',lw=3)
        plt.xlabel('dt')
    if dxORdt == 'ds':
        plt.loglog(data.ds, err,'o',lw=3)
        plt.xlabel('Solver Tolerance')
    if label=='Solver_tol':
        plt.ylim([1e-7,1e-3])
    if label=='mesh':
        plt.ylim([1e-7,1e-3])
    if label=='time':
        plt.ylim([1e-6,1e-3])
    if label=='mesh_Tdiff':
        plt.ylim([1e-6,1e-1])
    if label=='time_Tdiff':
        plt.ylim([1e-5,1e-2])
    plt.title(f'{label}')
    plt.ylabel('Error')    
    plt.grid(True,which='both',linestyle='--',alpha=0.6)
    plt.tight_layout()
    #plt.xlim([0,0.022])
 #   plt.title(f'{title}: {var} (scaled)')
    plt.savefig(f'../figures/streeq_error_{var[0]}_{label}.png',dpi=300)
    plt.close()
    return err 

# Scatter dx vs dy - color = error  
#cmap='coolwarm'
def  scatter_err_dxdy(data,model_fit_statistics,dataM,errM,dataT,errT,label,numCurves):
    plt.figure(figsize=(12,8))
    tmp=model_fit_statistics.loc[(var[0],0,'beta0')]
    median=tmp['median']
    err = np.array((data[var[0]]-median).abs()/median)
    plt.title('Error by $\Delta x$ vs. $\Delta t$')
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
        plt.savefig(f'../figures/streeq_scatter_error_{var[0]}_{label}_all.png',dpi=300)
    if numCurves == 1: 
        plt.savefig(f'../figures/streeq_scatter_error_{var[0]}_{label}.png',dpi=300)
    plt.close()
    return err

# Order of Convergence Plots
def order_p(err,h,dxORdt,label): 
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
    plt.loglog(h,err,'-ok',label=f'Observed (p={p_observed[0]:.2f})')
#     plt.loglog(h_ref,ref_slopeP,'--',color='gray',label=f'Observed (p={p_observed[0]:.2f})')
    plt.loglog(h_ref,ref_slope1,'--',label='p=1')
#     plt.loglog(h_ref,ref_slope2,'--',label='p=2')
    plt.ylabel('Relative Error')
    if dxORdt=='Solver_Tol':
        plt.xlabel(f'{dxORdt}')
    if dxORdt=='$\Delta t$':
        plt.xlabel(f'{dxORdt} (sec)')
    if dxORdt=='$\Delta x$':
        plt.xlabel(f'{dxORdt} (m)')
    if label == 'Solver_Tol':
        plt.ylim(1e-15,1e-2)
        plt.title('Solver Tolerance Study')
    if label == 'mesh':
        plt.ylim(1e-7,1e-2)
        plt.title('Mesh Resolution')
        offset = offset/0.45
    if label == 'time':
        plt.ylim(1e-7,1e-2)
        plt.title('Time Step Resolution')
        offset = offset/0.35
    if label == 'time17':
        plt.ylim(1e-4,1e-1)#1e-10,1e-4)
        plt.title('Time Step Resolution')
        offset = offset
    if label == 'timeAll':
        plt.ylim(1e-7,1e-2)
        plt.title('Time Step Resolution')
        offset = offset/0.1
    if label in ['time_Tbulk', 'mesh_Tbulk']:
        plt.ylim(1e-7, 1e-2)
        plt.title('Bulk Temperature Error')
    ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
    plt.loglog(h_ref,ref_slope2,'--',label='p=2')
    plt.legend(loc='lower right')
    plt.xticks(ticks=h,labels=[f'{val:.1e}' for val in h],rotation=45)
    plt.grid(True,which='both',linestyle='--',alpha=0.6)
    plt.tight_layout()
    plt.savefig(f'../figures/relative_err_observedP_{label}.png',dpi=300,bbox_inches='tight')    
####################################
   
# QOI
var=['Temperature'] 

########  Mesh T_bulk - Code Verification
directory_Tbulk_M = '../streeq_studies/Tbulk_mesh'
data_input_file_Tbulk_M = 'df_sim_Tbulk_all_mesh.dat' 
data_input_file_names_Tbulk_M = ['dx','Temperature']
data_Tbulk_M, model_fit_statistics_Tbulk_M, model_fits_Tbulk_M = data_process(directory_Tbulk_M,data_input_file_Tbulk_M,data_input_file_names_Tbulk_M)
dx_Tbulk_M=np.linspace(0,0.0005,101)
#convergence_plots(data_Tbulk_M,model_fit_statistics_Tbulk_M,model_fits_Tbulk_M,dx_Tbulk_M,'dx',label='mesh_Tbulk')
err_Tbulk_mesh = error_plots(data_Tbulk_M,model_fit_statistics_Tbulk_M,'dx',label='mesh_Tbulk')
err_mesh_Tbulk, h_mesh_Tbulk = np.array(err_Tbulk_mesh), np.array(data_Tbulk_M['dx'])
order_p(err_mesh_Tbulk,h_mesh_Tbulk,dxORdt='$\Delta x$',label='mesh_Tbulk')

######## Time T_bulk - Code Verification
directory_Tbulk_T = '../streeq_studies/Tbulk_time'
data_input_file_Tbulk_T = 'df_sim_Tbulk_all_time.dat'  
data_input_file_names_Tbulk_T = ['dt','Temperature']
data_Tbulk_T, model_fit_statistics_Tbulk_T, model_fits_Tbulk_T = data_process(directory_Tbulk_T,data_input_file_Tbulk_T,data_input_file_names_Tbulk_T)
dt_Tbulk_T=np.linspace(0,0.005,101) 
#convergence_plots(data_Tbulk_T,model_fit_statistics_Tbulk_T,model_fits_Tbulk_T,dt_Tbulk_T,'dt',label='time_Tbulk')
err_Tbulk_time = error_plots(data_Tbulk_T,model_fit_statistics_Tbulk_T,'dt',label='time_Tbulk')
err_time_Tbulk, h_time_Tbulk = np.array(err_Tbulk_time), np.array(data_Tbulk_T['dt'])
order_p(err_time_Tbulk,h_time_Tbulk,dxORdt='$\Delta t$',label='time_Tbulk')
# print(f'data: {data_Tbulk_T}')


    




