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
