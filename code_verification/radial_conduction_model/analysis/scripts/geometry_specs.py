# Geometry & Mesh Quantities

mesh_label = 'shortPipelongCase_m0_caseht.msh'

### Lengths 
len_fluid = (45 + (45*0.25))*1e-3
len_solid = (45)*1e-3

### Diameters (m)
diam_fluid = 2.27 *1e-3
diam_case = 2.57 *1e-3
case_thickness = 0.3 *1e-3 # m 

### Number of Elements @ the cross section 0.0675m 67.5mm of the Solid case ONLY
num_elem_crosssection_m0 = 200 
num_elem_crosssection_m1 = 800 
num_elem_crosssection_m2 = 3200

### Number of nodes/points (All geometries)
num_nodes_allgeom_M0 = 128438
num_nodes_allgeom_M1 = 1008081 
num_nodes_allgeom_M2 = 7961978

### Number of cells/elements (All geometries)
num_cells_allgeom_M0 = 121508
num_cells_allgeom_M1 = 980652
num_cells_allgeom_M2 = 7852900

### Number of nodes AKA points (Solid ONLY geometries)
num_nodes_case_M0 = 27300
num_nodes_case_M1 = 181000
num_nodes_case_M2 = 1299600

### Number of cells (Solid ONLY geometries)
num_cells_case_M0 = 18000 
num_cells_case_M1 = 144000
num_cells_case_M2 = 1152000

# import numpy as np
# ### Calculate Volumes
# vol_fluid = len_fluid *np.pi*(diam_fluid*1e3/2)**2 
# print(f'vol_fluid= {vol_fluid}')
# vol_case  = len_solid*np.pi*((diam_case/2)**2 - (diam_fluid/2)**2)
# print(f'vol_case= {vol_case}')

# # Calculate the representative lengths
# def rep_len(volume_region,num_cells):
#     rep_cell = volume_region/num_cells
#     rep_len = (rep_cell)**(1/3)
#     return rep_len

# replen_M0 = rep_len(vol_case,num_cells_case_M0)
# replen_M1 = rep_len(vol_case,num_cells_case_M1)
# replen_M2 = rep_len(vol_case,num_cells_case_M2)

# print(f'replen_M0 = {replen_M0:.3e}')
# print(f'replen_M1 = {replen_M1:.3e}')
# print(f'replen_M2 = {replen_M2:.3e}')

# print(f'***************************')
### Calculate Areas
# areas_fluid = np.pi*(diam_fluid*1e3/2)**2 
# print(f'vol_fluid= {areas_fluid}')
# areas_case  = np.pi*((diam_case/2)**2 - (diam_fluid/2)**2)
# print(f'vol_case= {areas_case}')


# replen_M0 = rep_len(areas_case,num_elem_crosssection_m0)
# replen_M1 = rep_len(areas_case,num_elem_crosssection_m1)
# replen_M2 = rep_len(areas_case,num_elem_crosssection_m2)

# print(f'replen_M0 = {replen_M0:.3e}')
# print(f'replen_M1 = {replen_M1:.3e}')
# print(f'replen_M2 = {replen_M2:.3e}')
