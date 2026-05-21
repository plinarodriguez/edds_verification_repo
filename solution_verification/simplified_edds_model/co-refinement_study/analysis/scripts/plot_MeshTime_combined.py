import pandas as pd 
import matplotlib.pyplot as plt

plt.rcParams['font.family'] ='serif'
plt.rcParams['font.size']=20

data = pd.read_csv('../data/results_MeshTimestep_Err.dat')

# Create the figure
plt.figure(figsize=(12,8))

# Plot error vs  rep length - x-axis
line1, = plt.loglog(data['Representative Length'], data['Error'], 'o-', label='Error vs Representative Length', lw=2, color='blue')
plt.xticks(ticks=data['Representative Length'],labels=[f'{val:.1e}    ' for val in data['Representative Length']],rotation=30)
plt.tick_params(axis='x', labelcolor='blue') 
plt.xlabel('Spatial Discretization ($\Delta x$)',color='blue')
plt.ylabel('Relative Error')
plt.ylim([6e-5,6e-3])
plt.grid(True, which='both', linestyle='--', linewidth=0.5)


# Create a secondary 
ax_top = plt.gca().twiny()  # Get the current axis and add a twin x-axis
line2, = ax_top.loglog(data['Representative Time'], data['Error'], 's-', label='Error vs Representative Timestep', lw=2, color='orange')
ax_top.set_xticks(data['Representative Time'])
ax_top.set_xticklabels([f'     {val:.1e} ' for val in data['Representative Time']],rotation=30,color='orange')
ax_top.set_xlabel('Temporal Discretization ($\Delta t$)',color='orange')

plt.legend([line1,line2],['p$_{\Delta x}$ = 2.07 ','p$_{\Delta t}$ = 2.10'], loc='best', title='Observed Order of Convergence',fontsize=20)

# # Add a title
# plt.title('Error by $\Delta x$ vs. $\Delta t$ \n')

# Save and show the plot
plt.savefig('../data/figures/meshTimestepStudy/relative_err_observedP_meshANDtimestep.png', dpi=150, bbox_inches='tight')
plt.show()