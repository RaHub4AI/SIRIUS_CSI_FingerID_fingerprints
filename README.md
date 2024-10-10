# SMILES2SIRIUS6_fp

## Description

`SMILES2SIRIUS6_fp` is a Nextflow pipeline designed to compute chemical fingerprints using **SIRIUS+CSI:FingerID (version 6)** for chemicals based on their **SMILES** representations. The pipeline automates the process of calculating these fingerprints, which are useful for chemical structure elucidation and computational chemistry applications.

## Features

- Automatically processes chemical SMILES data to generate SIRIUS+CSI:FingerID fingerprints.
- Handles large datasets by dividing input SMILES into manageable batches.
- Uses Docker containers to ensure reproducibility and ease of setup.
- Outputs results in TSV format, ready for further analysis.
  
## Requirements

- **Nextflow** version 24.04.3 or higher
- **Docker** or **Apptainer/Singularity** (for containerized execution)
- **Python 3.x**

## Pipeline Structure

### Main Components:

- `nextflow.config`: Defines pipeline parameters, including input data paths, batch sizes, and Docker container configuration.
- `base.config`: Sets resource management policies for memory, CPUs, and retry strategies.
- `main.nf`: Main pipeline script that ties together the modules for data batching and fingerprint calculation.
- `modules/data2batch.nf`: Processes input SMILES data and divides it into smaller batches.
- `modules/smiles2sirius_fp.nf`: Runs the SIRIUS+CSI:FingerID fingerprint calculation.
- `bin/SMILES2SIRIUS6_fp.py`: Python script that calculates binary fingerprints that correspond to the SIRIUS+CSI:FingerID (v6) probabilistic fingerprints based on the input SMILES.

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/RaHub4AI/SIRIUS_CSI_FingerID_fingerprints.git
cd SIRIUS_CSI_FingerID_fingerprints
```

### 2. Install Nextflow

Follow the instructions on the [Nextflow website](https://www.nextflow.io/) to install the required version (24.04.3 or higher).

### 3. Prepare Input Data

The input file should be a TSV file containing a column labeled **'SMILES'** with the SMILES strings of the chemicals to be processed.

Example of the input file format:
ID    SMILES
1     CC(C)OC(=O)N1CCN(C2CCOCC2)CC1
2     CCOC(=O)N1CCN(C2CCOCC2)CC1

### 4. Set Configuration

Edit the `nextflow.config` file to specify the input data path, batch size, and output directory.

```groovy
params.data = 'path/to/your/input_data.tsv'
params.batch_size = 10000 // Number of SMILES entries to process in one batch
params.results = 'path/to/output_directory'
params.sirius6_fingerid = './data/fingerid_data.txt' // File from SIRIUS API SDK
```

### 5. Run the Pipeline
To execute the pipeline with Apptainer:
```bash
nextflow run main.nf -with-apptainer quay.io/ida_rahu/sirius6_fp:v1.0.1
```
### 6. Output
The pipeline outputs fingerprint data in TSV format, saved to the directory specified in `params.results`. Each batch will produce a file with binary fingerprints that correspond to SIRIUS+CSI:FingerID (v6) fingerprints.

## Configuration Parameters

- **`params.data`**: Path to the input TSV file containing SMILES strings.
- **`params.batch_size`**: Number of SMILES entries to process per batch.
- **`params.sirius6_fingerid`**: Path to the fingerprint feature mapping file obtained via the [SIRIUS API SDK](https://github.com/sirius-ms/sirius-client-openAPI).
- **`params.results`**: Output directory where the results will be stored.
- **`process.container`**: Docker container used for running the processes.
- **`params.max_memory`**: Maximum memory allocation for the processes (default is 128 GB).
- **`params.max_cpus`**: Maximum number of CPUs to be used (default is 32).
- **`params.max_time`**: Maximum time allowed for a task to run (default is 120 hours).

## Customization

The pipeline is modular, allowing easy customization of individual steps:

- Modify the `base.config` file to adjust memory, CPU, and retry configurations.
- Customize the batch size to fit the computational resources or dataset size.

## References

- [SIRIUS API SDK](https://github.com/sirius-ms/sirius-client-openAPI) - Used to retrieve fingerprint feature data.
- [Nextflow Documentation](https://www.nextflow.io/docs/latest/index.html) - Nextflow official documentation for pipeline management.
- [SIRIUS](https://bio.informatik.uni-jena.de/software/sirius/) - Tool for analysing LC/HRMS data.

