#!/usr/bin/env python

import dakota.interfacing as di
import os 
import time 

params, results = di.read_parameters_file()

di.dprepro('template.sbatch.bash',
           parameters=params,
           results=results,
           inline='{ }',
           output='sbatch.bash')

di.dprepro('template.decompose',
           parameters=params,
           results=results,
           inline='{{ }}',
           output='template/system/decomposeParDict')

di.dprepro('template.controlDict',
           parameters=params,
           results=results,
           inline='{ }',
           output='template/system/controlDict')

di.dprepro('template.fvSolution_caseSolid',
           parameters=params,
           results=results,
           inline='{ }',
           output='template/system/caseSolid/fvSolution')


di.dprepro('template.fvSolution_pipeFluid',
           parameters=params,
           results=results,
           inline='{ }',
           output='template/system/pipeFluid/fvSolution')


mesh_size = int(params['mesh_size'])
os.system(f'cp ../meshes/mesh{mesh_size}.msh .');

os.system('sbatch sbatch.bash')

open('done.txt','w').close()
counter = 0    
while os.path.getsize('done.txt')==0 and counter < 14500:
    os.system('grep "End" log.reconstructPar > done.txt')
    time.sleep(300)
    counter += 300

import qoi_temperature_data

vtk_directory = 'VTK'
points =[[0,0,0.001],[0,0,0.006],[0,0.0,0.030],[0,0.000,0.045],[0,0.000,0.0517],[0,0.001,0.006],[0,0.002,0.006],[0,0.00225,0.006],[0,0.001,0.030],[0,0.002,0.030],[0,0.00225,0.030],[0,0.001,0.0517],[0,0.002,0.0517],[0,0.00225,0.0517],[0,0.001,0.0],[0,0.002,0.0],[0,0.00225,0.0]]
#target_times = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
target_times = [0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5]

qois = qoi_temperature_data.data_qoi(target_times,vtk_directory,points)

###### Z = 30 mm
#results['t0.01_r0'   ].function = qois[0,2]
#results['t0.01_r1'   ].function = qois[0,8]
results['t0.5_r2'   ].function = qois[0,9]
#results['t0.01_r2.25'].function = qois[0,10]

# results['t0.02_r0'   ].function = qois[1,2]
# results['t0.02_r1'   ].function = qois[1,8]
results['t1_r2'   ].function = qois[1,9]
# results['t0.02_r2.25'].function = qois[1,10]

# results['t0.03_r0'   ].function = qois[2,2]
# results['t0.03_r1'   ].function = qois[2,8]
results['t1.5_r2'   ].function = qois[2,9]
# results['t0.03_r2.25'].function = qois[2,10]

# results['t0.04_r0'   ].function = qois[3,2]
# results['t0.04_r1'   ].function = qois[3,8]
results['t2_r2'   ].function = qois[3,9]
# results['t0.04_r2.25'].function = qois[3,10]

# results['t0.05_r0'   ].function = qois[4,2]
# results['t0.05_r1'   ].function = qois[4,8]
results['t2.5_r2'   ].function = qois[4,9]
# results['t0.05_r2.25'].function = qois[4,10]

# results['t0.06_r0'   ].function = qois[5,2]
# results['t0.06_r1'   ].function = qois[5,8]
results['t3_r2'   ].function = qois[5,9]
# results['t0.06_r2.25'].function = qois[5,10]

# results['t0.07_r0'   ].function = qois[6,2]
# results['t0.07_r1'   ].function = qois[6,8]
results['t3.5_r2'   ].function = qois[6,9]
# results['t0.07_r2.25'].function = qois[6,10]

# results['t0.08_r0'   ].function = qois[7,2]
# results['t0.08_r1'   ].function = qois[7,8]
results['t4_r2'   ].function = qois[7,9]
# results['t0.08_r2.25'].function = qois[7,10]

# results['t0.09_r0'   ].function = qois[8,2]
# results['t0.09_r1'   ].function = qois[8,8]
results['t4.5_r2'   ].function = qois[8,9]
# results['t0.09_r2.25'].function = qois[8,10]

# results['t0.1_r0']   .function = qois[9,2]
# results['t0.1_r1']   .function = qois[9,8]
results['t5_r2']   .function = qois[9,9]
# results['t0.1_r2.25'].function = qois[9,10]

# results['t0.11_r0']   .function = qois[10,2]
# results['t0.11_r1']   .function = qois[10,8]
#results['t0.11_r2']   .function = qois[10,9]
# results['t0.11_r2.25'].function = qois[10,10]


results.write()

os.system('echo $PWD > direc.txt')

