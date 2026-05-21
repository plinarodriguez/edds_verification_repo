#!/bin/bash

#############################################################
# Set cluster specific configurations here for job submission
#############################################################

FOAM_BIN=/qscratch/prodrig/OpenFOAM/OpenFOAM-9/platforms/linux64GccDPInt32Opt/bin/
OPENFOAM=$FOAM_BIN/chtMultiRegionFoam
DECOMPOSEPAR=$FOAM_BIN/decomposePar
source /qscratch/prodrig/OpenFOAM/OpenFOAM-9/etc/bashrc
. ${WM_PROJECT_DIR}/bin/tools/RunFunctions

# Create necessary Openfoam directories
mkdir {0,constant,system}

# Copy primary control file for OpenFoam simulation
cp template/system/controlDict system/

# convert mesh bes sure to set the mesh file name here
fluent3DMeshToFoam mesh_file_name_here.msh

# Copy finite volume scheme and solution
cp template/system/{fvSchemes,fvSolution} system/

# Split into multiple regions
splitMeshRegions -cellZones -overwrite

# Run Toposet
#cp template/system/caseSolid/topoSetDict system/caseSolid/topoSetDict
#runApplication topoSet -region caseSolid

# Copy initial and boundary conditions
cp template/0/caseSolid/T 0/caseSolid/
cp template/0/pipeFluid/{T,p,p_rgh,U} 0/pipeFluid/

# Copy Fluid and Thermal Properties
cp template/constant/caseSolid/{fvModels,radiationProperties,thermophysicalProperties} constant/caseSolid/
cp template/constant/pipeFluid/{radiationProperties,thermophysicalProperties,momentumTransport,g,turbulenceProperties} constant/pipeFluid/

# Copy Additional Config Files
cp template/system/decomposeParDict system/
cp template/system/caseSolid/decomposeParDict system/caseSolid
cp template/system/pipeFluid/decomposeParDict system/pipeFluid
cp template/constant/regionProperties constant/

# Copy finite volume scheme and solution for each region
cp template/system/caseSolid/{fvSchemes,fvSolution} system/caseSolid
cp template/system/pipeFluid/{fvSchemes,fvSolution} system/pipeFluid

# pre-process, partition mesh
runApplication decomposePar -allRegions

# run
runParallel $(getApplication)

# post-process
runApplication reconstructPar -allRegions

# ParaView Visualization
paraFoam -touchAll

# convert to VTK
$FOAM_BIN/foamToVTK -region pipeFluid -fields '(T U)'
$FOAM_BIN/foamToVTK -region caseSolid -fields '(T U)'

