#!/bin/bash

#############################################################
# Set cluster specific configurations here for job submission
#############################################################
ranks={num_processors}

FOAM_BIN=/OpenFOAM/OpenFOAM-9/platforms/linux64GccDPInt32Opt/bin/
OPENFOAM=$FOAM_BIN/chtMultiRegionFoam
DECOMPOSEPAR=$FOAM_BIN/decomposePar
source /OpenFOAM/OpenFOAM-9/etc/bashrc
source /OpenFOAM/OpenFOAM-9/bin/tools/RunFunctions

# Create necessary Openfoam directories
mkdir 0
mkdir constant
mkdir system

# Copy primary control file for OpenFoam simulation
cp template/system/controlDict system/

# convert mesh
fluent3DMeshToFoam mesh{mesh_size}.msh

# Copy finite volume scheme and solution
cp template/system/fvSolution system/
cp template/system/fvSchemes system/

# Split into multiple regions
splitMeshRegions -cellZones -overwrite

# Copy initial and boundary conditions
cp template/0/caseSolid/T 0/caseSolid/
cp template/0/pipeFluid/T 0/pipeFluid/
cp template/0/pipeFluid/p 0/pipeFluid/
cp template/0/pipeFluid/p_rgh 0/pipeFluid/
cp template/0/pipeFluid/U 0/pipeFluid/

# Copy Fluid and Thermal Properties
cp template/constant/caseSolid/fvModels constant/caseSolid/
cp template/constant/caseSolid/radiationProperties constant/caseSolid/
cp template/constant/caseSolid/thermophysicalProperties constant/caseSolid/
cp template/constant/pipeFluid/radiationProperties constant/pipeFluid/
cp template/constant/pipeFluid/thermophysicalProperties constant/pipeFluid/
cp template/constant/pipeFluid/momentumTransport constant/pipeFluid/
cp template/constant/pipeFluid/g constant/pipeFluid/
cp template/constant/pipeFluid/turbulenceProperties constant/pipeFluid/

# Copy Additional Config Files
cp template/system/decomposeParDict system/
cp template/system/decomposeParDict system/caseSolid/
cp template/system/decomposeParDict system/pipeFluid/
cp template/constant/regionProperties constant/

# Copy finite volume scheme and solution for each region
cp template/system/caseSolid/fvSchemes system/caseSolid/
cp template/system/caseSolid/fvSolution system/caseSolid/
cp template/system/pipeFluid/fvSchemes system/pipeFluid/
cp template/system/pipeFluid/fvSolution system/pipeFluid/

# pre-process, partition mesh
runApplication decomposePar -allRegions

# run
runParallel $(getApplication)

# post-process
runApplication reconstructPar -allRegions

# ParaView Visualization
paraFoam -touchAll

# convert to VTK
$FOAM_BIN/foamToVTK -region pipeFluid -fields '(T)'
$FOAM_BIN/foamToVTK -region caseSolid -fields '(T)'

