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

vol_fluid = geometry_specs.len_fluid *np.pi*(geometry_specs.diam_fluid*1e3/2)**2 
vol_case  = geometry_specs.len_solid*np.pi*((geometry_specs.diam_case/2)**2 - (geometry_specs.diam_fluid/2)**2)
replen_M0 = rep_len(vol_case,geometry_specs.num_cells_case_M0)
replen_M1 = rep_len(vol_case,geometry_specs.num_cells_case_M1)
replen_M2 = rep_len(vol_case,geometry_specs.num_cells_case_M2)

# Compute 
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

# Import data from data processing converting VTK to CSV and combine
data = pd.read_csv('../data/dataT_mAll.csv')
# Collect Mesh Specific Temperature Data
dataM0 = data[data['Mesh']==0]
dataM1 = data[data['Mesh']==1]
dataM2 = data[data['Mesh']==2]

rM0, volM0 = dataM0['r'],dataM0['Vol']
rM1, volM1 = dataM1['r'],dataM1['Vol']
rM2, volM2 = dataM2['r'],dataM2['Vol']

def l2_norm_calc(T_sim,r,volumes):    
    T_analytic = analyticbyradius(r)
    diff_squared = (T_sim - T_analytic)**2
    weighted_sum = np.sum(diff_squared*volumes)
    numerator = np.sqrt(weighted_sum)
    denominator = np.sqrt(np.sum(T_analytic**2 * volumes))
    l2_error = numerator/denominator
    return l2_error, r

# Computer L2 Norm
l2_errorsM0,radiusM0 = l2_norm_calc(dataM0['T'],rM0,volM0)
l2_errorsM1,radiusM1 = l2_norm_calc(dataM1['T'],rM1,volM1)
l2_errorsM2,radiusM2 = l2_norm_calc(dataM2['T'],rM2,volM2)
# Calculate Order of Convergence
h = [replen_M0,replen_M1,replen_M2] # representative lengths
errU = [l2_errorsM0,l2_errorsM1,l2_errorsM2] # l2 norm errors 
# print(f'errU= {errU}')
p_observed = (np.log(errU[-1])-np.log(errU[0]))/(np.log(h[-1])-np.log(h[0]))
# print(f'p_observed={p_observed}')
h_anchor = h[1]
u_err_anchor = errU[1]
offset = 2
h_ref = np.logspace(np.log10(h[0]),np.log10(h[2]),100)
ref_slope1 = u_err_anchor*(h_ref/h_anchor)**1 * (offset*2)
ref_slope2 = u_err_anchor*(h_ref/h_anchor)**2 / offset
plt.figure(figsize=(12,8))
plt.loglog(h,errU,'o-k',label=f'Observed (p ={np.abs(p_observed):.2f})', markersize=8)
plt.loglog(h_ref,ref_slope1,'--',label='p = 1')
plt.loglog(h_ref,ref_slope2,'--',label='p = 2')
plt.title('Temperature \n')
plt.xlabel('Representative Length [m]')
plt.ylabel('L2 Norm')
plt.ylim(1e-7,1e-2)
h_labels = [f"{val:.1e}" for val in h]
plt.xticks(ticks=h,labels=h_labels,rotation=30)
plt.tick_params(axis='x',pad=15)
plt.legend()
plt.grid(True,which='both',linestyle='--',alpha=0.6)
plt.tight_layout()
plt.savefig(f'../figures/T_L2Norm_Observed_p.png', dpi=300, bbox_inches='tight')