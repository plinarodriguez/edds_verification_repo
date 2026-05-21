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
target_times = [0,1.0,2.0,3.0,4.0,5,6,7,8,9,10,11,12]

qois = qoi_temperature_data.data_qoi(target_times,vtk_directory,points)

###### Z = 30 mm
results['t1_r2'   ].function = qois[0,9]
results['t2_r2'   ].function = qois[1,9]
results['t3_r2'   ].function = qois[2,9]
results['t4_r2'   ].function = qois[3,9]
results['t5_r2'   ].function = qois[4,9]
results['t6_r2'   ].function = qois[5,9]
results['t7_r2'   ].function = qois[6,9]
results['t8_r2'   ].function = qois[7,9]
results['t9_r2'   ].function = qois[8,9]
results['t10_r2'  ].function = qois[9,9]
results['t11_r2'  ].function = qois[10,9]
results['t12_r2'  ].function = qois[11,9]

results.write()

os.system('echo $PWD > direc.txt')

