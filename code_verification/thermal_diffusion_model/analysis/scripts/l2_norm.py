import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

# Set the font family and size to use for Matplotlib figures.
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 20

# import volumes and number of cells
import geometry_specs

# Compute representative lengths
def rep_len(volume_region,num_cells):
    rep_cell = volume_region/num_cells
    rep_len = (rep_cell)**(1/3)
    return rep_len

l2_errs = pd.read_csv('../data/Errors_timesAll_meshAll.csv')
vol_fluid = geometry_specs.len_fluid *np.pi*(geometry_specs.diam_fluid/2)**2 
vol_case  = geometry_specs.len_solid*np.pi*((geometry_specs.diam_case/2)**2 - (geometry_specs.diam_fluid/2)**2)
replen_M0 = rep_len(vol_fluid,geometry_specs.num_cells_fluid_M0)
replen_M1 = rep_len(vol_fluid,geometry_specs.num_cells_fluid_M1)
replen_M2 = rep_len(vol_fluid,geometry_specs.num_cells_fluid_M2)
h = [replen_M0,replen_M1,replen_M2] # representative lengths
# h = [5e-3,5e-4,5e-5]              # time steps (delta_t)
# print(f'h={h}')
times = [0.015,0.020,0.025]
colors = ['r','b','g']
plt.figure(figsize=(12,8))
for t,c in zip(times,colors): 
    eM0= l2_errs.loc[(l2_errs["time"] == t) & (l2_errs["Mesh"] == 0), "l2_rmse_error"].iloc[0]
    eM1= l2_errs.loc[(l2_errs["time"] == t) & (l2_errs["Mesh"] == 1), "l2_rmse_error"].iloc[0]
    eM2= l2_errs.loc[(l2_errs["time"] == t) & (l2_errs["Mesh"] == 2), "l2_rmse_error"].iloc[0]
    err_t01 = [eM0,eM1,eM2] # l2 norm errors 
    # print(f'err_t01={err_t01}')
    p01 = np.log(err_t01[1]/err_t01[0]) / np.log(h[1]/h[0])
    p12 = np.log(err_t01[2]/err_t01[1]) / np.log(h[2]/h[1])
    p02 = np.log(err_t01[2]/err_t01[0]) / np.log(h[2]/h[0])
    p_observed = (np.log(err_t01[-1])-np.log(err_t01[0]))/(np.log(h[-1])-np.log(h[0]))
    plt.loglog(h,err_t01,'-o',label=f"t={t}s (p={np.abs(p_observed):.2f})", markersize=8,color=f'{c}')  
    # print(f'p_observed={p_observed}')
# print(f'p01 = {p01} \n p12 = {p12} \n p02 = {p02}')
h_anchor = h[1]
u_err_anchor = err_t01[1]
offset = 4
h_ref = np.logspace(np.log10(h[0]),np.log10(h[2]),100)
ref_slope1 = u_err_anchor*(h_ref/h_anchor)**1 * (offset*2)
ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
plt.loglog(h_ref,ref_slope1,'--',label='p = 1')
plt.loglog(h_ref,ref_slope2,'--',label='p = 2')
plt.title('Temperature \n')
plt.xlabel('Representative Length [m]')
plt.ylabel('L2 Norm')
plt.ylim(1e-7,1e-2) #plt.ylim(1e-10,1e-7)
h_labels = [f"{val:.1e}" for val in h]
plt.xticks(ticks=h,labels=h_labels,rotation=30)
plt.tick_params(axis='x',pad=15)
plt.legend(loc='lower right')
plt.grid(True,which='both',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.savefig(f'../figures/T_L2Norm_Observed_p.png', dpi=300, bbox_inches='tight')
