import numpy as np 
import pandas as pd
import pyvista as pv 
import re 
import glob
import os
import matplotlib.pyplot as plt

pd.set_option('display.float_format','{:.12e}'.format)

########################################################################################
# ---------------- Test for Temperature continuity
#######################################################################################
vtk_path = "workdir.1/VTK"
times_cont = [1500] #,500,1000,1500,2000,2500]
df_temps = pd.DataFrame(columns=["time","type","mean [K]","min [K]","max [K]","max abs [K]"])
for t in times_cont:
    fluid_all  = pv.read(f"{vtk_path}/pipeFluid/allPatches/allPatches_{t}.vtk")
    pid_fluid_if = 4 #matching interface, patch id 
    pid = fluid_all.cell_data["patchID"]
    cells = np.where(pid == pid_fluid_if)[0]
    fluid_if = fluid_all.extract_cells(cells)

    solid_all  = pv.read(f"{vtk_path}/caseSolid/allPatches/allPatches_{t}.vtk")
    pid_solid_if = 3 #matching interface, patch id 
    pid = solid_all.cell_data["patchID"]
    cells = np.where(pid == pid_solid_if)[0]
    solid_if = solid_all.extract_cells(cells)
    
    print("solid:", fluid_all.n_cells, fluid_all.n_points, fluid_all.cell_data.keys(), fluid_all.point_data.keys())
    print("Cell data arrays:", fluid_if.cell_data.keys())
    print("Point data arrays:", fluid_if.point_data.keys())
    print("Field data arrays:", fluid_if.field_data.keys())
    print("n_cells, n_points:", fluid_if.n_cells, fluid_if.n_points)

    #####################################
    # fid = fluid_all.cell_data["patchID"]
    # areas = fluid_all.compute_cell_sizes(length=False, area=True, volume=False).cell_data["Area"]
    # print(f'Fluid \n')
    # # this gets all the patches to find the matching interface
    # for u in np.unique(fid):
    #     A = float(areas[fid == u].sum())
    #     n = int(np.sum(fid == u))
    #     print(f"patchID={int(u):4d}  nFaces={n:8d}  Area={A:.6e}")

    # sid = solid_all.cell_data["patchID"]
    # areas = solid_all.compute_cell_sizes(length=False, area=True, volume=False).cell_data["Area"]
    # print(f'solid \n')
    # # this gets all the patches to find the matching interface
    # for u in np.unique(sid):
    #     A = float(areas[sid == u].sum())
    #     n = int(np.sum(sid == u))
    #     print(f"patchID={int(u):4d}  nFaces={n:8d}  Area={A:.6e}")

    # # this checks the patches since 2 or 3 could be the patches. but now we see that patch 2 is constant. 
    # # Get T as cell data for easy averaging on each patch
    # if "T" in fluid_all.point_data and "T" not in fluid_all.cell_data:
    #     fluid_all = fluid_all.cell_data_from_point_data(pass_point_data=False)
    # T = fluid_all.cell_data["T"]
    # for u in np.unique(fid):
    #     Tu = T[fid == u]
    #     print(f"patchID={int(u)}  Tmean={Tu.mean():.6g}  Tmin={Tu.min():.6g}  Tmax={Tu.max():.6g}")
        
    # # ### Conclusion patch id = 3 is the matching patch. 
    # ################################
    Tf = fluid_if.cell_data["T"]
    Ts = solid_if.cell_data["T"]

    Xf = fluid_if.cell_centers().points
    Xs = solid_if.cell_centers().points
    # map each fluid interface point to nearest solid interface point
    solid_pts = pv.PolyData(Xs)
    idx = np.empty(len(Xf), dtype=int)
    for i, p in enumerate(Xf):
        idx[i] = solid_pts.find_closest_point(p)

    dT = Tf - Ts[idx]
    df_temps_t = pd.DataFrame({
    "time":[t,t,t] ,
    "type": ['Tf','Ts','deltaT'],
    "mean [K]":[float(Tf.mean()),float(Tf.mean()),float(dT.mean())],
    "min [K]": [float(Tf.min()),float(Ts.min()),float(dT.min())],
    "max [K]": [float(Tf.max()),float(Ts.max()),float(dT.max())],
    "max abs [K]": [float(np.max(np.abs(Tf))),float(np.max(np.abs(Ts))),float(np.max(np.abs(dT)))]})
    df_temps = pd.concat([df_temps,df_temps_t])
# print(df_temps)

#Area weighted metric
Af = fluid_if.compute_cell_sizes(length=False, area=True, volume=False).cell_data["Area"]
mean_abs = float(np.sum(np.abs(dT) * Af) / np.sum(Af))
# print("Area-weighted mean |deltaT| [K]:", mean_abs)

################################################################################
#------------------------ Test for heatflux and gradT quantities ---------------------------
################################################################################
############## To generate wallheatflux
# 0) source /OpenFOAM/OpenFOAM-9/etc/bashrc
# 1) Add a file in system
#      1.1) system/wallQ_pipeFluid that includes
#         type        wallHeatFlux;
#         libs        ("libfieldFunctionObjects.so");
#         region      pipeFluid;
#         patches     (pipeFluid_to_caseSolid);
#      1.2) system/wallQ_caseSolid that includes
#         type        wallHeatFlux;
#         libs        ("libfieldFunctionObjects.so");
#         region      caseSolid;
#         patches     (caseSolid_to_pipeFluid);
# 2a) Generate wall heat flux with `chtMultiRegionFoam -postProcess -func wallQ_pipeFluid -time '0:'`
# 2b) Generate wall heat flux with `chtMultiRegionFoam -postProcess -func wallQ_caseSolid -time '0:'`
# 3) Generate vtk files: 
#        foamToVTK -region pipeFluid -fields '(T wallHeatFlux)' -allPatches -time '0:'
#        foamToVTK -region caseSolid -fields '(T wallHeatFlux)' -allPatches -time '0:'


# vtk_path = "../study_pipe_steady_refine-mesh-radialconv/study_m1/VTK"
vtk_path = "workdir.1/VTK"
k_f = 0.0259  # air W/m/K
k_s = 91.0    # nickel W/m/K
time_scale = 1 # scale filename index 
################  find the matching patches (patchID) to compare for the interface (pipeFluid_to_caseSolid)
time_test = 125
file_vtk =  f"{vtk_path}/pipeFluid/allPatches/allPatches_{time_test}.vtk"
m = pv.read(file_vtk)
pid = np.asarray(m.cell_data["patchID"])
q   = np.asarray(m.cell_data["wallHeatFlux"])
print("unique patchIDs:", np.unique(pid))
for u in np.unique(pid):
    qu = q[pid == u]
    print(f"ID: {u}, nCells: {qu.size}, q(min/mean/max): {qu.min()}, {qu.mean()}, {qu.max()}")
iface_id = 4  # interface patch id, this is the only non zero q 
#########################

def integrate_Q_allPatches(allPatches_vtk,iface_id):
    m = pv.read(allPatches_vtk) #data is in cell arrays
    iface = m.threshold(
        value=(iface_id - 0.1, iface_id + 0.1),
        scalars="patchID"
        ) 
    q_iface = np.asarray(iface.cell_data["wallHeatFlux"])
    iface2 = iface.triangulate().compute_cell_sizes(length=False, area=True, volume=False)
    A = np.asarray(iface2.cell_data["Area"])
    q = np.asarray(iface2.cell_data["wallHeatFlux"])
    Q = np.sum(q * A)                 # W
    q_areaMean = Q / np.sum(A)        # W/m^2
    return np.sum(A),q_iface,iface.n_cells, Q,q_areaMean
    # print("iface cell arrays:", list(iface.cell_data.keys()))
    # print("iface nCells:", iface.n_cells)
    # print("iface q min/mean/max:", q_iface.min(), q_iface.mean(), q_iface.max())
    # print(f'q_iface = {q_iface}')
    # print("Interface area:", np.sum(A))
    # print("Integrated heat rate Q:", Q)
    # print("Area-mean wallHeatFlux:", q_areaMean)

def time_from_allpatches(path):
    m = re.search(r'allPatches_(\d+(?:\.\d+)?)\.vtk$', os.path.basename(path))
    m_time =  int(m.group(1))
    return m_time

# d = 0.00454 # pipe diameter in m 
# R = d/2    
# l_fdf = 0.045  #fully developed flow regime in m 
# r_caseOut = 0.00257 # m
# volPipe   = np.pi*R**2*l_fdf*2 # 1456.948 mm^3
# volCase   = np.pi*(r_caseOut - R)**2 * l_fdf # 12.723 mm^3
# volTotal  =  (volPipe + volCase)
# mesh_elem = [121508, 980652,7852900] 
# mesh_node = [128438,1008081,7961978] 
# len_rep   = (volTotal/ np.array(mesh_elem))**(1/3)

meshes = [1,2,3,4,5,6,7] 
df = pd.DataFrame(columns = ["Mesh","time","region","iface nCells","iface area","qMin","qMean","qMax","Q(W)","Q(W/m^2)"])
for m in meshes:
    vtk_path = f"workdir.{m}/VTK"
    files = glob.glob(f"{vtk_path}/pipeFluid/allPatches/allPatches_*.vtk")
    times = sorted(time_from_allpatches(f) for f in files)
    print(times)
    # for t in times: 
    for t in times[-2:]: #[:2]:
        print(f't = {t} & mesh = {m}')
        allPatchesvtk_fluid = f"{vtk_path}/pipeFluid/allPatches/allPatches_{t}.vtk"
        allPatchesvtk_solid = f"{vtk_path}/caseSolid/allPatches/allPatches_{t}.vtk"
        farea_if,fq_iface,fncells_if,fQ,fqareaMean = integrate_Q_allPatches(allPatchesvtk_fluid,iface_id=4)
        sarea_if,sq_iface,sncells_if,sQ,sqareaMean = integrate_Q_allPatches(allPatchesvtk_solid,iface_id=3)
        row_fluid = {"Mesh":m,"time": t,"region": "pipeFluid","iface nCells": fncells_if,"iface area": farea_if,"qMin": fq_iface.min(),"qMean": fq_iface.mean(),"qMax": fq_iface.max(),"Q(W)": fQ,"Q(W/m^2)": fqareaMean}
        row_solid = {"Mesh":m,"time": t,"region": "caseSolid","iface nCells": sncells_if,"iface area": sarea_if,"qMin": sq_iface.min(),"qMean": sq_iface.mean(),"qMax": sq_iface.max(),"Q(W)": sQ,"Q(W/m^2)": sqareaMean}
        df = pd.concat([df, pd.DataFrame([row_fluid, row_solid])], ignore_index=True)
print(f'df =\n{df}')
df.to_csv('../figures/integratedQ_heatflux.dat',index=False)


### analysis 
# 1) drop the initial time (assumes the initial is the minimum time per mesh)
df2 = df.copy()
t0 = df2.groupby("Mesh")["time"].transform("min")
df2 = df2[df2["time"] != t0].copy()

# 2) pick the steady time per mesh = earliest remaining time for that mesh
tss = df2.groupby("Mesh")["time"].transform("min")
steady = df2[df2["time"] == tss].copy()

# 3) build fluid/solid paired table and imbalance metrics
f = steady[steady["region"]=="pipeFluid"][["Mesh","time","iface nCells","iface area","Q(W)","Q(W/m^2)"]].rename(
    columns={"Q(W)":"Qf_W","Q(W/m^2)":"qf_mean"}
)
s = steady[steady["region"]=="caseSolid"][["Mesh","time","Q(W)","Q(W/m^2)"]].rename(
    columns={"Q(W)":"Qs_W","Q(W/m^2)":"qs_mean"}
)
r_in = 0.00257 # m
r_out = 0.00227 # m
caselength = 0.0072 # m
vol_case = (np.pi*(r_in**2-r_out**2)*caselength)
case_q = 7e7
Q_heatsource = vol_case * case_q
print(f'Qheatsource = {Q_heatsource}')
tab = f.merge(s, on=["Mesh","time"])
tab["dQ_W"] = tab["Qf_W"] + tab["Qs_W"]
# tab["relImb"] = np.abs(tab["dQ_W"]) / np.maximum(np.abs(tab["Qf_W"]), np.abs(tab["Qs_W"]))
tab["relImb"] = np.abs(tab["dQ_W"]) / Q_heatsource #np.mean(np.abs(tab[["Qf_W","Qs_W"]]),axis=1)

#np.mean(np.abs(tab[["Qf_W","Qs_W"]]),axis=1)
Q_meanfs = np.mean(np.abs(tab[["Qf_W","Qs_W"]]),axis=1)
print(f'Q_meanfs = {Q_meanfs}')
print(tab[["Mesh","time","iface nCells","iface area","Qf_W","Qs_W","dQ_W","relImb"]])

# 4) plot imbalance vs mesh resolution
x = tab["iface nCells"]  # or use Mesh index
plt.figure(figsize=(9,6))
plt.loglog(x, np.abs(tab["dQ_W"]), "o-")
plt.xlabel("Number of interface cells, $N_{iface}$")
plt.ylabel("Qf + Qs (W)")
plt.title("Interface Flux Comparison")
plt.ylim(1e-4,1e-2)
plt.tight_layout()
plt.grid(True, which='both',ls='--',linewidth='0.5')
plt.savefig("../figures/imbalance_abs_vs_nCells_t6.0.png", dpi=300, bbox_inches="tight")
plt.close()

plt.figure(figsize=(9,6))
plt.loglog(x, tab["relImb"], "o-")
# plt.xticks(x)
plt.xlabel("Number of interface cells, $N_{iface}$")
plt.ylabel("Qf + Qs (W)/$N_{iface}$")
plt.title("Normalized Interface Flux Comparison")
plt.tight_layout()
plt.grid(True, which='both',ls='--',linewidth='0.5')
plt.savefig("../figures/imbalance_rel_vs_nCells_t6.0.png", dpi=300, bbox_inches="tight")
plt.close()