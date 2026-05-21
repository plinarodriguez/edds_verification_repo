# Cubit Journal Files

## Overview
This directory contains Cubit journal files used for mesh generation and geometry creation. These files are intended to automate the process of creating meshes for simulations and analyses wthout having to provide the very large mesh files.

## Contents
- `verification_heatsource.jou`: [Mesh with the fluid region x1.25 the length of the casing region. This is used for the heat source comparison analysis. ]
- [Add descriptions for additional files as needed]

## Requirements
To use these journal files, you will need:
- **Cubit Version**: [Cubit 17.06.0]

## Instructions
1. Open Cubit (ensure the correct version is installed).
2. Load the journal file:
   - In the Cubit GUI, go to `Tools > Journal Editor` and `Open` the desired `.jou` file.
3. Hit the play button and it will play the current file running all the commands to generate all meshes used in this study. 