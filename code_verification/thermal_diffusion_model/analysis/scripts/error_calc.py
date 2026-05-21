import numpy as np
import pandas as pd
from scipy.special import j0, j1, jn_zeros
import matplotlib.pyplot as plt

# Set the font family and size to use for Matplotlib figures.
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 20
# -----------------------------
# Inputs
# -----------------------------
kf = 0.0259
rho_f = 1.225
cp_f = 1004.5

alpha_f = kf / (rho_f * cp_f)
R = 0.00227      # m, fluid radius / interface radius
T0 = 293.15      # K, initial fluid temperature
Ts = 303.15      # K, prescribed interface temperature
r_plot = np.linspace(0, R, 300)
# print(f"alpha_f = {alpha_f:.6e} m^2/s")

# -----------------------------
# Analytical solution
# -----------------------------
n_terms=100

def T_fluid_transient(r, t, R, T0, Ts, alpha, n_terms):
    """
    Transient radial conduction in a full cylinder using Bessel functions 
    T(r,0) = T0
    dT/dr at r=0 = 0
    T(R,t) = Ts
    """
    r = np.asarray(r, dtype=float)
    lambdas = jn_zeros(0, n_terms)  # roots of J0(lambda)=0
    theta = np.zeros_like(r, dtype=float)
    for lam in lambdas:
        theta += (2.0* j0(lam * r / R)/ (lam * j1(lam))* np.exp(-(lam**2) * alpha * t / R**2))
    return Ts + (T0 - Ts) * theta

# -----------------------------
# Analytical solution - Plot
# -----------------------------
def analytic_radialTemp_by_times(times,r_plot,R,T0, Ts, alpha_f,label, n_terms):
    plt.figure(figsize=(12,8))
    for t in times:
        plt.plot(r_plot, T_fluid_transient(r_plot, t, R, T0, Ts, alpha_f,n_terms), label=f"t={t:g} s")

    plt.xlabel("Radius, r [m]")
    plt.ylabel("Temperature, T [K]")
    plt.legend()
    plt.savefig(f"../figures/Tanalytic_vs_radius_{label}.png", dpi=300, bbox_inches="tight")
    plt.close()

# -----------------------------
# Temperature vs. Radius - Temp Plot - Single time step 
# -----------------------------
def radial_Temp_plot_singletimestep(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms):
    fluid["time"] = fluid["time"].astype(float)
    fluid = fluid.sort_values(["time", "r"])
    t_compare = t 
    df_t = fluid[np.isclose(fluid["time"], t_compare)].copy()
    df_t["T_exact"] = T_fluid_transient(df_t["r"].values,t_compare,R,T0,Ts,alpha_f,n_terms)
    df_t["error"] = df_t["T"] - df_t["T_exact"]
    r_plot = np.linspace(0, R, 300)
    plt.figure(figsize=(12,8))
    plt.plot(r_plot,T_fluid_transient(r_plot, t_compare, R, T0, Ts, alpha_f, n_terms),label="Analytical",color='black')
    plt.scatter(df_t.loc[df_t["Mesh"]==2,"r"], df_t.loc[df_t["Mesh"]==2, "T"], s=10, label="M2 ")
    plt.scatter(df_t.loc[df_t["Mesh"]==1,"r"], df_t.loc[df_t["Mesh"]==1, "T"], s=10, label="M1 ")
    plt.scatter(df_t.loc[df_t["Mesh"]==0,"r"], df_t.loc[df_t["Mesh"]==0, "T"], s=10, label="M0 ")
    plt.xlabel("Radius, r [m]")
    plt.ylabel("Temperature, T [K]")
    plt.title(f"t = {t_compare:g} s")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"../figures/T_vs_r_meshAll_analytic_t{t}.png", dpi=300, bbox_inches="tight")
    plt.close()


# -----------------------------
# Tdiff Plot - Single time step  - All meshes
# -----------------------------
def radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms):
    fluid["time"] = fluid["time"].astype(float)
    fluid = fluid.sort_values(["time", "r"])
    ##### Radial Temperatures (Analytical and Simulation) for a single timestep 
    t_compare = t 
    df_t_m0 = fluid[(fluid["Mesh"] == 0) & np.isclose(fluid["time"], t_compare)].copy()
    df_t_m1 = fluid[(fluid["Mesh"] == 1) & np.isclose(fluid["time"], t_compare)].copy()
    df_t_m2 = fluid[(fluid["Mesh"] == 2) & np.isclose(fluid["time"], t_compare)].copy()
    df_t_m0["T_exact"] = T_fluid_transient(df_t_m0["r"].values,t_compare,R,T0,Ts,alpha_f,n_terms)
    df_t_m1["T_exact"] = T_fluid_transient(df_t_m1["r"].values,t_compare,R,T0,Ts,alpha_f,n_terms)
    df_t_m2["T_exact"] = T_fluid_transient(df_t_m2["r"].values,t_compare,R,T0,Ts,alpha_f,n_terms)
    df_t_m0["error"] = df_t_m0["T"] - df_t_m0["T_exact"]
    df_t_m1["error"] = df_t_m1["T"] - df_t_m1["T_exact"]
    df_t_m2["error"] = df_t_m2["T"] - df_t_m2["T_exact"]
    # print("time =", t_compare)
    r_plot = np.linspace(0, R, 300)
    plt.figure(figsize=(12,8))
    plt.scatter(df_t_m0["r"], df_t_m0["error"], s=8, label="Sim-M0 ")
    plt.scatter(df_t_m1["r"], df_t_m1["error"], s=10, label="Sim-M1 ")
    plt.scatter(df_t_m2["r"], df_t_m2["error"], s=10, label="Sim-M2 ")
    plt.xlabel("Radius, r [m]")
    plt.ylabel('Temperature difference')
    plt.title(f"t = {t_compare:g} s")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"../figures/Tdiff_meshAll_t{t}.png", dpi=300, bbox_inches="tight")
    plt.close()


# -----------------------------
# Temperature vs. Radius  - All times - single mesh
# -----------------------------
def radial_Temp_plot_timesAll(fluid,r_plot,R,T0,Ts,alpha_f,label, n_terms):
    error_rows = []
    plt.figure(figsize=(12,8))
    for t in sorted(fluid["time"].unique()):
        df_t = fluid[np.isclose(fluid["time"], t)].copy()
        df_t["T_exact"] = T_fluid_transient(df_t["r"].values,t,R,T0,Ts,alpha_f,n_terms)
        df_t = df_t.sort_values("r")
        # OpenFOAM points
        plt.scatter(df_t["r"], df_t["T"], s=8, alpha=0.6, label=f"OF t={t:g}")
        # Analytical curve
        plt.plot(r_plot,T_fluid_transient(r_plot, t, R, T0, Ts, alpha_f, n_terms),linewidth=1.5,label=f"Anly t={t:g}")
    plt.xlabel("r [m]")
    plt.ylabel("T [K]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"../figures/T_vs_r_timesAll_{label}.png", dpi=300, bbox_inches="tight")
    plt.close()

# -----------------------------
# Computes the L2 Norm  
# -----------------------------
def weighted_l2_rel_error(T_sim, T_exact, vol,T_scale):
    diff = T_sim - T_exact       
    l2_abs = np.sqrt(np.sum(diff**2 *vol))
    l2_rel = l2_abs/T_scale  # normalized by the solid temperature Ts=303.15
    rms_abs = np.sqrt(np.sum(diff**2*vol)/len(vol))   
    rms_abs = np.sqrt(np.sum(diff**2*vol))/np.sqrt(np.sum(T_exact**2*(vol))) 
    return l2_rel, l2_abs,rms_abs

# -----------------------------
# Errors - L2 Norms - Temp Plots & Errs & Errs Plots - All Time Steps 
# -----------------------------
def errs_plots_allTimes_allMeshes(fluid,r_plot,R,T0,Ts,alpha_f, n_terms):
    meshes = [0,1,2]
    error_rows = []
    for t in  sorted(fluid.loc[fluid["Mesh"] == 2, "time"].unique()): #sorted(fluid["time"].unique()):
        for m in meshes:
            df_tm = fluid[(fluid["Mesh"] == m) & np.isclose(fluid["time"], t)].copy()
            df_tm = df_tm.sort_values("r")
            T_exact = T_fluid_transient(df_tm["r"],t,R,T0,Ts,alpha_f,n_terms)
            T_sim = df_tm['T']
            vol = df_tm['Vol']
            T_scale = Ts
            l2_rel, l2_abs,l2_rms = weighted_l2_rel_error(T_sim, T_exact, vol,T_scale)
            diff = T_sim - T_exact
            error_rows.append({
                "time": t,
                "Mesh": m,
                "max_abs_diff": np.max(np.abs(diff)),
                "l2_abs_error":l2_abs ,
                "l2_rel_error": l2_rel,
                "l2_rmse_error": l2_rms,
                "num_cells": len(df_tm['T'])
            })
        errors = pd.DataFrame(error_rows).sort_values(["Mesh", "time"])
        errors.to_csv(f'../data/Errors_timesAll_meshAll.csv',index=False)

        plt.figure(figsize=(12,8))
        for m in meshes: 
            em = errors[errors["Mesh"] == m]
            plt.semilogy(em["time"], em["l2_abs_error"], "-o", label=f"m{m}")
        # plt.ylim(1e-6,1e-2)
        plt.xlabel("Time [s]")
        plt.ylabel("$L_2$ Norm")
        plt.title('Volume Weighted differences \n')
        plt.legend()
        plt.grid(True,which='both',linestyle='--',alpha=0.6)
        plt.tight_layout()
        plt.savefig(f"../figures/Errors_timesAll_meshAll_l2abs.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        plt.figure(figsize=(12,8))
        for m in meshes: 
            em = errors[errors["Mesh"] == m]
            plt.semilogy(em["time"][1:], em["l2_rel_error"][1:], "-o", label=f"m{m}")
        # plt.ylim(1e-7,1e-5)
        plt.xlabel("Time [s]")
        plt.ylabel("$L_2$ Norm")
        plt.title('Normalized by the Analytical Temperature \n')
        plt.legend()
        plt.grid(True,which='both',linestyle='--',alpha=0.6)
        plt.tight_layout()
        plt.savefig(f"../figures/Errors_timesAll_meshAll_l2rel.png", dpi=300, bbox_inches="tight")
        plt.close()

        plt.figure(figsize=(12,8))
        for m in meshes: 
            em = errors[errors["Mesh"] == m]
            plt.semilogy(em["time"][1:], em["l2_rmse_error"][1:], "-o", label=f"m{m}")
        plt.ylim(1e-5,1e-2)
        plt.xlabel("Time [s]")
        plt.ylabel("$L_2$ Norm")
        plt.title("Temperature \n") 
        plt.legend()
        plt.grid(True,which='both',linestyle='--',alpha=0.6)
        plt.tight_layout()
        plt.savefig(f"../figures/Errors_timesAll_meshAll_l2rmse.png", dpi=300, bbox_inches="tight")
        plt.close()

######################################################################################################
###### Run Functions

# Plot the analytic solutions for selected times
times = [0.005,0.015,0.025,0.05]
label = 't0.005-0.05'
analytic_radialTemp_by_times(times,r_plot,R,T0, Ts, alpha_f,label, n_terms)

# Plots Temperature vs radius meshesAll & analytic - single time  
df1 = pd.read_csv("../data/dataT_m01_pipeFluid.csv")
df2 = pd.read_csv("../data/dataT_m2_pipeFluid.csv")
fluid = pd.concat([df1, df2], axis=0, ignore_index=True)  # ignore_index renumbers rows
t = 0.025
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)
t = 0.020
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)
t = 0.015
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)
t = 0.010
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)
t = 0.005
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)
t = 0.0
radial_Temp_plot_singletimestep(fluid,t,r_plot, R, T0, Ts, alpha_f, n_terms)

# Plot Sim vs. Analytic solutions (Temp & Errs) for all time steps & Errs dataframe  
fluid = pd.read_csv("../data/dataT_m2_pipeFluid.csv")
label='M2'
radial_Temp_plot_timesAll(fluid,r_plot,R,T0,Ts,alpha_f,label, n_terms)

# Plot Sim vs. Analytic solutions (Temp) for one time step - All meshes 
df1 = pd.read_csv("../data/dataT_m01_pipeFluid.csv")
df2 = pd.read_csv("../data/dataT_m2_pipeFluid.csv")
fluid = pd.concat([df1, df2], axis=0, ignore_index=True)  
t = 0.025
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)
t = 0.020
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)
t = 0.015
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)
t = 0.010
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)
t = 0.005
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)
t = 0.0
radial_Temp_plot_singletimestep_meshes(fluid,t,r_plot,R, T0, Ts, alpha_f, n_terms)

# Plot Sim vs. Analytic solutions (Temp & Errs) for all time steps & Errs dataframe  
df1 = pd.read_csv("../data/dataT_m01_pipeFluid.csv")
df2 = pd.read_csv("../data/dataT_m2_pipeFluid.csv")
fluid = pd.concat([df1, df2], axis=0, ignore_index=True) 
errs_plots_allTimes_allMeshes(fluid,r_plot,R,T0,Ts,alpha_f, n_terms)