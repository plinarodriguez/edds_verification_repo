# Reproducible Verification Studies for a Multiphysics EDDS Model

This repository contains reproducible code and solution verification studies for a simplified electronic drug delivery system (EDDS) modeled using OpenFOAM.

The project includes:

* Code verification using analytical solutions
* Solution verification using StREEQ
* Automated HPC workflows using SLURM and Dakota
* Parallel OpenFOAM simulations using MPI
* Python-based post-processing and verification analysis

The workflows are designed to support transparent and reproducible computational modeling and simulation (CM&S) studies for credibility assessment.

---

# Scientific Motivation

The full EDDS multiphysics system does not have an analytical solution. To build credibility in the computational model, verification studies were performed using simplified geometries and isolated physics.

The verification strategy follows a modular approach:

1. Isolate individual physics
2. Compare against analytical solutions when possible
3. Quantify discretization error
4. Assess convergence behavior
5. Evaluate coupled multiphysics behavior

This repository supports reproducible verification workflows aligned with risk-informed credibility assessment approaches for computational modeling and simulation.

---

# Computational Model

## Physical System

A physics-based computational model was developed for an electronic drug delivery system (EDDS). The system consists of:

* Fluid flow through a pipe
* Heat transfer through a surrounding solid casing
* Conjugate heat transfer between the fluid and solid regions
* Transient thermal behavior

Fluid enters through the inlet region, passes through a heated casing section, and exits through the outlet region.

## Governing Physics

The model includes:

* Incompressible laminar fluid flow
* Heat conduction within the solid casing
* Conjugate heat transfer at the fluid-solid interface
* Transient thermal diffusion

## Numerical Solver

The simulations use:

* OpenFOAM v9
* `chtMultiRegionFoam`
* MPI-based parallelization
* SLURM job scheduling on HPC systems

## Mesh Generation

Meshes were generated using Cubit and exported as Fluent `.msh` files before conversion to OpenFOAM format.

Meshes are not included directly in the repository. Instead, Cubit journal files are provided to support reproducible mesh generation.

---

# Repository Organization

```text
├── code_verification/
│   ├── hydrodynamic_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   ├── radial_conduction_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   └── thermal_diffusion_model/
│       ├── analysis/
│       ├── mesh/
│       └── simulation_setup/
│
├── solution_verification/
│   ├── coupled_pipe_model/
│   │   ├── analysis/
│   │   ├── mesh/
│   │   └── simulation_setup/
│   │
│   └── simplified_edds_model/
│       ├── co_refinement_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   ├── cost_study/
│       │   └── simulation_setup/
│       │
│       ├── interface_energy_consistency/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       ├── solver_tolerance_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       ├── spatial_refinement_only_study/
│       │   ├── analysis/
│       │   ├── mesh/
│       │   └── simulation_setup/
│       │
│       └── temporal_refinement_only_study/
│           ├── analysis/
│           ├── mesh/
│           └── simulation_setup/
```

---

# Software Requirements

## Required Software

* OpenFOAM v9
* Python 3.x
* MPI
* SLURM
* Cubit
* Dakota
* StREEQ

## Python Packages

* numpy
* pandas
* matplotlib
* pyvista

## HPC Assumptions

The workflows assume:

* Access to a SLURM-managed HPC cluster
* MPI-enabled OpenFOAM installation
* Parallel job submission capability

---

# Reproducibility Notes

This repository is designed to support reproducible computational modeling and simulation workflows.

Reproducibility considerations include:

* Version-controlled simulation setup files
* Automated workflow execution
* Scripted mesh generation
* Automated post-processing
* Explicit software dependency tracking
* Structured verification studies

Meshes are generated using Cubit journal files to allow reproducible reconstruction of the computational domains.

Large simulation outputs are reduced through extraction of quantities of interest (QoIs) into CSV files for lightweight post-processing and analysis.

---

# Running the Workflows

## Single Simulation Studies

Single simulation studies include:

* Hydrodynamic model
* Radial conduction model
* Thermal diffusion model
* Coupled pipe model

These workflows:

* Run a single OpenFOAM simulation
* Use MPI mesh decomposition for parallel execution
* Reconstruct decomposed solutions after simulation completion

### Example Execution

```bash
sbatch sbatch.batch
```

### Workflow Summary

1. Generate mesh
2. Decompose domain
3. Run OpenFOAM simulation
4. Reconstruct solution
5. Extract quantities of interest from VTK files 
6. Run verification post-processing

---

## Multiple Simulation Studies

Multiple simulation studies include:

* Co-refinement study
* Solver tolerance study
* Spatial refinement study
* Temporal refinement study
* Interface consistency study

These workflows:

* Run multiple simulations simultaneously
* Use Dakota for workflow orchestration
* Use StREEQ for extrapolation and convergence analysis

### Workflow Summary

1. Generate parameterized simulation inputs using dakota input file
2. Submit multiple simulations to run in parallel
3. Extract QoIs from VTK files 
4. Generate extrapolated solutions using StREEQ
5. Compute discretization errors
6. Generate convergence plots

---

# Quantities of Interest (QoIs)

The verification studies use extracted quantities of interest (QoIs) from simulation outputs to reduce storage requirements and simplify post-processing. Stored as CSV files for post-processing.

QoIs include: Teperature and Velocity Profiles

---

# Error Metrics

The repository includes verification analyses using:

* $L_2$ norm error
* Relative error comparisons with extrapolated quantities (using StREEQ)
* Observed order of convergence

---

# HPC Workflow

## MPI Parallelization

OpenFOAM simulations are parallelized using MPI decomposition.

Typical workflow:

1. Decompose mesh
2. Run parallel simulation
3. Reconstruct decomposed results

## Dakota Workflow Management

Dakota is used to:

* Generate parameterized studies
* Manage multiple simulations
* Automate job submission
* Coordinate refinement studies

## StREEQ Integration

StREEQ is used for:

* Extrapolated solution estimation
* Observed order of convergence
* Relative error analysis

Repository:
[https://github.com/sandialabs/StREEQ](https://github.com/sandialabs/StREEQ)

---

# References

## Software

* OpenFOAM
* Dakota
* StREEQ
* Cubit

## Standards and Methodology

* ASME V&V 20
* ASME V&V 40
* NASEM Reproducibility and Replicability in Science

## Related Repositories

* StREEQ: [https://github.com/sandialabs/StREEQ](https://github.com/sandialabs/StREEQ)
* EDDS Credibility Plan: [https://github.com/plinarodriguez/edds-credibility-plan](https://github.com/plinarodriguez/edds-credibility-plan)

---

# Citation

If you use this repository in published work, please cite the associated publications and repositories.


