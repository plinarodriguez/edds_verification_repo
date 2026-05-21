# Geometry & Mesh Quantities

mesh_label = 'shortPipelongCase_m0_caseht.msh'
localtion_Cubit_Journal_file = 'ascldap/users/prodrig/Focuments/cubitJournals/code_verification_m0-2_shortpipelongcase_ht.jou'

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

### Number of cells (Fluid ONLY geometries)
num_cells_fluid_M0 = 103508
num_cells_fluid_M1 = 836652
num_cells_fluid_M2 = 6700900

### Number of cells (Fluid ONLY geometries)
num_cells_fluid_M0f = 17910
num_cells_fluid_M1f = 132460
num_cells_fluid_M2f = 1083821

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

#### Density and Heat Capacity for study_m1_dcp studies Note nickel density is 444 and cp is 8900
m1_d0  =  0.089     # this is the density that's used for the heat source study with  m0 m1 m2
m1_cp0 =  0.00444   # this is the density that's used for the heat source study with  m0 m1 m2

m1_d1  = 0.01
m1_cp1 = 0.10

m1_d2  = 0.10
m1_cp2 = 1.00

m1_d3  = 1.00
m1_cp3 = 10.0

m1_d4  = 10.0
m1_cp4 = 100.0

# The above are too small!!!!!! They result in no changes in the outputs: 
# 1.0,1,0.00230692996410653,-3.62401497113744e-05,0.00230721459941282,293.316009521484,1.35896081068379e-12
# 1.1,1,0.00230692996410653,-3.62401497113744e-05,0.00230721459941282,293.316009521484,1.35896081068379e-12
# 1.2,1,0.00230692996410653,-3.62401497113744e-05,0.00230721459941282,293.316009521484,1.35896081068379e-12
# 1.3,1,0.00230692996410653,-3.62401497113744e-05,0.00230721459941282,293.316009521484,1.35896081068379e-12
# 1.4,1,0.00230692996410653,-3.62401497113744e-05,0.00230721459941282,293.316009521484,1.35896081068379e-12

# Instead Try: 
m1_d5  = 9
m1_cp5 = 151

m1_d6  = 27  
m1_cp6 = 606

m1_d7  = 111
m1_cp7 = 2425

m1_d8  = 444
m1_cp8 = 8900
